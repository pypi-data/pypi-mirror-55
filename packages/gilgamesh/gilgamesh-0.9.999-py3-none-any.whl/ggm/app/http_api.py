"""
    Copyright (c) 2019 Contributors as noted in the AUTHORS file
    This file is part of ggm, the GILGAMESH core engine in Python.
    ggm is free software; you can redistribute it and/or modify it under
    the terms of the GNU Lesser General Public License (GPL) as published
    by the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.
    As a special exception, the Contributors give you permission to link
    this library with independent modules to produce an executable,
    regardless of the license terms of these independent modules, and to
    copy and distribute the resulting executable under terms of your choice,
    provided that you also meet, for each linked independent module, the
    terms and conditions of the license of that module. An independent
    module is a module which is not derived from or based on this library.
    If you modify this library, you must extend this exception to your
    version of the library.
    ggm is distributed in the hope that it will be useful, but WITHOUT
    ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
    FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public
    License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import zmq
import time
import json
import asyncio
from zmq.utils.strtypes import asbytes
from ..lib.kontext import Kontext
from ..lib.kernel import GK
from datetime import datetime as dt

from aiohttp import web

from pprint import pprint

class HttpApi(GK):
    def __init__(self, *args, **kwargs):
        self.loop = kwargs['loop']
        self.ctx = kwargs['context']
        self.name = kwargs['name']

        self.api_sock = "ipc:///tmp/frontend"

        # POST handlers are only input -> only one socket
        self.post = self.ctx.socket(zmq.DEALER)
        self.post.connect(self.api_sock)
        self.post.setsockopt(zmq.LINGER, 0)

        GK.__init__(self, *args, **kwargs)

    async def handle_get(self, request):
        # chop chop
        call = request.path.split("/")
        params = dict(request.rel_url.query)
        call.pop(0)
        if call[-1] == '':
            call.pop(-1)
        request = ['http-get']
        if params:
            call.append(params)
        request.extend(call)

        reply = await asyncio.shield(self.get_job(request))

        return web.json_response(reply)

    async def get_job(self, request):
        req = self.ctx.socket(zmq.DEALER)
        req.connect(self.api_sock)
        req.setsockopt(zmq.LINGER, 0)

        # get the requested data
        await req.dsend(request)
        _, reply = await req.drecv()

        # close zmq connection
        req.close()

        return reply

    async def handle_post(self, request):
        # get POST data
        call = request.path.split("/")
        data = await request.json()

        # add timestamp to data if they don't have one
        time_keys = ['time']
        for k in time_keys:
            if k not in data:
                data['time'] = self.get_iso_timestamp()

        # chop chop
        call.pop(0)
        if call[-1] == '':
            call.pop(-1)
        request = ['http-post']
        if data:
            call.append(data)
        request.extend(call)

        reply = await asyncio.shield(self.post_job(request))

        return web.json_response(reply)

    async def post_job(self, request):
        await self.post.dsend(request)
        _, reply = await self.post.drecv()

        return reply

def http_api_process(kcfg):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    kcfg['context'] = Kontext()
    kcfg['loop'] = loop
    
    api = HttpApi(**kcfg)

    # not sure if this even works...
    handler_args = {
            "tcp_keepalive": False,
            "keepalive_timeout": 10,
            "lingering_time": 0
    }
    aioapp = web.Application(handler_args=handler_args)

    # catch all requests
    aioapp.router.add_get('/{tail:.*}', api.handle_get)
    aioapp.router.add_post('/{tail:.*}', api.handle_post)

    web.run_app(
            aioapp,
            host="0.0.0.0",
            port=kcfg["port"],
            access_log=api.glog
    )
    api.start()
