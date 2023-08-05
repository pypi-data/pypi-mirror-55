import sys
import zlib
import json
import pickle
import asyncio
import zmq.auth
import time
import socket
from .auth import AuthClient

from pathlib import Path
from datetime import datetime as dt

from pprint import pprint

import pandas as pd
from pandas.io.json import json_normalize

class GClient(AuthClient):
    def __init__(self, ggm_host='local',*args, **kwargs):
        """GILGAMESH™
        
        class GGM(ggm_host='local')
        
        ggm_host: sting found as key in config.json
        """
        super().__init__(ggm_host, *args, **kwargs)

        self.poller = zmq.Poller()
        self.poller.register(self.client, zmq.POLLIN)

        assert self.check_conn()
        
        self.client.psend(['info'])
        reply = self.client.precv()
        self.remote_dev_id = reply['dev_id']
        
    def show_devices(self):
        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()
        devs = [d for d in reply['device_state_db'][self.remote_dev_id]['store'].keys()]
        devs.append(self.remote_dev_id)
        return devs

    def show_measurements(self, device):
        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()
        if device == self.remote_dev_id:
            return [d for d in reply['device_state_db'][self.remote_dev_id]['inventory'].keys()]
        else:
            return [d for d in reply['device_state_db'][self.remote_dev_id]['store'][device].keys()]
    
    def show_store(self):
        self.client.psend(['json', 'get', 'device_state_db', self.remote_dev_id, 'head'])
        reply = self.client.precv()
        store = reply['device_state_db'][self.remote_dev_id]['store']
        store[self.remote_dev_id] = reply['device_state_db'][self.remote_dev_id]['inventory']
        return store

    def get_measurement(self, dev_id, measurement, start=None, stop=None, chunk_size=5000, cols=None, pipeline=3, compression=True, progress=True, dataframe=True):
        params = dict()
        if not start:
            return 'error: start must be given'
        else:
            params['start'] = start

        params['stop'] = stop or self.get_tmst_now()
        if cols:
            params['cols'] = cols

        if progress:
            count_cmd = ['series', 'count', dev_id, measurement, params]
            self.client.psend(count_cmd)
            raw = self.client.precv()
            count_all = raw.pop()
            total_chunks = int(count_all/chunk_size)

        cmd = ['series', 'chunk', dev_id, measurement]
        try:
            start = time.time()
            if progress:
                data = self.download(cmd, params, chunk_size=chunk_size, pipeline=pipeline, compression=compression, total_chunks=total_chunks, dataframe=dataframe)
            else:
                data = self.download(cmd, params, chunk_size=chunk_size, pipeline=pipeline, compression=compression, dataframe=dataframe)
            stop = time.time()
            print('\n')
            print(f'-- {dev_id} {measurement} --')
            print(f'{len(data)} records received.')
            print(f'Time elapsed: {round(stop-start, 2)} s')
            print('\n')
        except Exception as e:
            print(f'Error while downloading {dev_id} {measurement} ({e})')
            data = self.clean_pipeline()
        except KeyboardInterrupt:
            data = self.clean_pipeline()

        return data

    def get_tmst_now(self):
        return dt.utcnow().isoformat(sep=' ')

    def clean_pipeline(self):
        msg = []
        while len(dict(self.poller.poll(1000))) > 0:
            _, msg = self.client.drecv()
        if isinstance(msg, dict):
            if 'Reason' in msg.keys():
                pprint(msg['Reason'])
        return True

    def update_progress(self, chunk, total):
        sys.stdout.write(f'\rDownloading chunk {chunk}/{total}')
        sys.stdout.flush()

    def download(self, cmd, params, chunk_size=5000, cols=None, pipeline=3, compression=True, dataframe=True, total_chunks=None):

        CHUNK_SIZE = chunk_size
        PIPELINE = pipeline

        credit = PIPELINE   # Up to PIPELINE chunks in transit
        total = 0           # Total records received
        chunks = 0          # Total chunks received
        offset = 0          # Offset of next chunk request
        thed = []           # zis is ze data
        cmd.append(params)

        while True:
            while credit:
                params['offset'] = offset
                params['limit']= CHUNK_SIZE
                cmd[-1] = params
                self.client.dsend(cmd)
                offset += CHUNK_SIZE
                credit -= 1
            route, msg = self.client.drecv(compression=compression)
            if len(msg) > 0:
                thed.extend(msg)
            if total_chunks:
                self.update_progress(chunks, total_chunks)
            chunks += 1
            credit += 1
            size = len(msg)
            if size < CHUNK_SIZE:
                break

        # 'empty' pipeline
        while credit < PIPELINE:
            route, msg = self.client.drecv(compression=compression)
            credit += 1
            if len(msg) > 0:
                thed.extend(msg)

        if dataframe:
            thed = self.flatten_points(thed)
            thed = pd.DataFrame.from_dict(thed)
            thed.set_index('time', inplace=True)
            thed.index = pd.to_datetime(thed.index)

        return thed

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

    def check_conn(self):        
        self.client.psend(['greetings'])
        while True:
            socks = dict(self.poller.poll(1000))
            if socks.get(self.client) == zmq.POLLIN:
                ret = self.client.precv()
                if ret == ['earthlings']:
                    print('Connecting to gilgamesh successful!')
                    return True
                elif not ret == ['earthlings']:
                    print(f'failed greeting(!) got: {ret}\nretrying...')
                    self.client.psend(['greetings'])
                    continue
            elif not socks.get(self.client):
                self.terminate()
                print(f'Failed connecting to server please check settings!\n')
                return False

    def terminate(self):
        self.client.set(zmq.LINGER, 0)
        self.client.close()
        self.ctx.term()
        print(f'Terminated gilgamesh Client')
