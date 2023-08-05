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
import zmq
import json
import asyncio
from zmq.utils.strtypes import asbytes
from datetime import datetime

from .logging import GLog
from .heart import GHeartt

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz

class GData(object):
    """
        TODO: write doc
    """
    def __init__(self, *args, **kwargs):

        self.DIN = "ipc:///tmp/data_in"
        #self.DOUT = "ipc:///tmp/data_out"

        self.sender = self.context.socket(zmq.PUSH)
        self.sender.connect(self.DIN)

        #self.receiver = self.context.socket(zmq.SUB)
        #self.receiver.connect(self.DOUT)

    async def send_data(self, dev_id, res_name, fields, tags, tmst=None):
        """
        dev_id: device id (most of the time self.dev_id)
        res_name: name of the resource
        fields: numeric values
        tags: string values, usually metadata
        tmst: optional, iso8601 timestamp
        """
        tmst = tmst or self.get_iso_timestamp()

        # internal 'route'
        msg = [dev_id, res_name]
        # always list of dicts so we can treat batch data the same 
        data = [
            {
                'time': tmst,
                'fields': fields or {},
                'tags': tags or {}
            }
        ]

        msg.append(data)
        #self.glog.debug(data)
        await self.sender.psnd(msg)

    async def send_batch(self, msg):
        await self.sender.psnd(msg)

    def iso_5min_ago(self):
        return dt.utcnow() - td(minutes=5)

    def get_iso_timestamp(self):
        return dt.utcnow().isoformat(sep=' ') # sep needed for better sqlite compatibility

    def flatten_points(self, data):
        """
        takes list of data dicts and flattens it
        if field and tag names are identical, tags wil get overwritten by fields
        """
        for d in data:
            d.update(d['tags'])
            d.update(d['fields'])
            if isinstance(d['tags'], dict):
                del d['tags']
            if isinstance(d['fields'], dict):
                del d['fields']
        return data
