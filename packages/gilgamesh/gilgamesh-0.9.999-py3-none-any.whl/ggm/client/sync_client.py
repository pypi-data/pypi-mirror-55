import sys, time, zmq
import pandas as pd
from .auth import AuthClient
from ..lib.sync_context import Kontext
from multiprocessing import Process

import datetime
from datetime import datetime as dt

from pprint import pprint
from time import sleep

class GClient(AuthClient):
    def __init__(self, ggm_host='local',*args, **kwargs):
        """GILGAMESH™
        
        class GGM(ggm_host='local')
        
        ggm_host: sting found as key in config.json
        """
        self.ggm_host = ggm_host
        super().__init__(ggm_host, *args, **kwargs)

        self.client = self.get_client()

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


    def get_measurement(self, dev_id, measurement, start=None, stop=None, cols=None, nproc=4, pipeline=10, chunk_size=5000, compression=True, progress=True, dataframe=True):
        params = dict()
        if not start:
            return 'error: start must be given'
        else:
            params['start'] = start
        params['stop'] = stop or self.get_tmst_now()
        if cols:
            params['cols'] = cols
        params['compression'] = compression

        try:
            count_cmd = ['series', 'count', dev_id, measurement, params]
            self.client.psend(count_cmd)
            raw = self.client.precv()
            count_all = raw.pop()
            total_chunks = count_all // chunk_size + (count_all % chunk_size > 0)

            put_work = self.ctx.socket(zmq.PUSH)
            put_work.setsockopt(zmq.LINGER, 0)
            put_work.bind('ipc://@work')

            res = self.ctx.socket(zmq.PULL)
            res.setsockopt(zmq.LINGER, 0)
            res.bind('ipc://@result')

            for proc in range(nproc):
                Process(target=GDownloader, args=(self.ggm_host, pipeline, chunk_size, dataframe)).start()

            # uncool
            sleep(1)

            print(f'-- {dev_id} {measurement} --')
            seg_td = (pd.to_datetime(params['stop'])-pd.to_datetime(params['start']))/nproc
            params['stop'] = (pd.to_datetime(params['start'])+seg_td).isoformat(sep=' ')
            data = []
            tic = time.time()

            for p in range(nproc):
                cmd = ['series', 'chunk', dev_id, measurement, params]
                put_work.psend(cmd)
                params['start'] = params['stop']
                params['stop'] = (pd.to_datetime(params['stop'])+seg_td).isoformat(sep=' ')


            chnk = 0
            while True:
                if chnk == total_chunks:
                    break
                tmp = res.precv()
                if dataframe:
                    tmp = pd.DataFrame.from_records(tmp, index='time')
                    tmp.index = pd.to_datetime(tmp.index)
                    data.append(tmp)
                else:
                    data.extend(tmp)
                chnk += 1
                if progress:
                    self.update_progress(chnk, total_chunks)

            if dataframe and data:
                data = pd.concat(data, sort=True)
                data.sort_index(inplace=True, ascending=False)
            toc = time.time()
            print(f'\n{len(data)} records received.')
            print(f'Time elapsed: {round(toc-tic, 2)} s')
        except Exception as e:
            print(f'Error while downloading {dev_id} {measurement} ({e})')
            data = self.clean_pipeline()
        except KeyboardInterrupt:
            data = self.clean_pipeline()
        finally:
            put_work.close()
            res.close()

        return data

    def get_tmst_now(self):
        return dt.utcnow().isoformat(sep=' ')

    def clean_pipeline(self):
        msg = []
        while len(dict(self.poller.poll(1000))) > 0:
            _, msg = self.client.drecv(raw=True)
        if isinstance(msg, dict):
            if 'Reason' in msg.keys():
                pprint(msg['Reason'])
        return True

    def update_progress(self, chunk, total):
        sys.stdout.write(f'\rDownloading chunk {chunk}/{total}')
        sys.stdout.flush()

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

class GAbo(object):
    def __init__(self):
        self.ctx = Kontext()
        poller = zmq.Poller()

        self.local_frontend = self.ctx.socket(zmq.DEALER)
        self.local_frontend.setsockopt(zmq.LINGER, 0)
        self.local_frontend.connect('ipc:///tmp/frontend')

        poller.register(self.local_frontend, zmq.POLLIN)

        self.local_frontend.psend(['info'])
        socks = dict(poller.poll(100))
        if not socks.get(self.local_frontend) == zmq.POLLIN:
            self.local_frontend.close()
            raise Exception('is local gilgamesh instance running?')

        socks = dict(poller.poll(100))
        if socks.get(self.local_frontend) == zmq.POLLIN:
            raw = self.local_frontend.precv()
            fro_dev_id = raw['dev_id']

        poller.unregister(self.local_frontend)

        self.abo_query = self.ctx.socket(zmq.DEALER)
        self.abo_query.setsockopt(zmq.LINGER, 0)
        self.abo_query.connect('ipc:///tmp/abo_front')

        poller.register(self.abo_query, zmq.POLLIN)

        self.abo_query.psend(['device_id'])
        socks = dict(poller.poll(100))
        if not socks.get(self.abo_query) == zmq.POLLIN:
            raise Exception('is local abo running?')

        socks = dict(poller.poll(100))
        if socks.get(self.abo_query) == zmq.POLLIN:
            dev_id = self.abo_query.precv()

        poller.unregister(self.abo_query)

        if not dev_id == fro_dev_id:
            raise Exception(f'setup appears to be malicious: ggm dev_id: {fro_dev_id} vs abo dev_id: {dev_id}')

        self.dev_id = dev_id

    def show_abos(self):
        cmd = ['json', 'get',  'abo_db', self.dev_id, 'head']
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response['abo_db'][self.dev_id])

    def delete_abo(self, dev, table):
        cmd = ['json', 'delete',  'abo_db', self.dev_id, dev, table]
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response)

    def clear_abos(self):
        cmd = ['json', 'delete',  'abo_db', self.dev_id]
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response)

    def add_abo(self, abos):
        cmd = ['json', 'nupsert', 'abo_db', self.dev_id, abos]
        self.local_frontend.dsend(cmd)
        _, response = self.local_frontend.drecv()
        pprint(response)

    def get_local(self, dev_id, measurement, start=None, stop=None, cols=None):
        if not start:
            return 'error: start must be given'

        self.abo_query.dsend(['path', dev_id, measurement])
        _, path = self.abo_query.drecv()

        if not path:
            return 'does not exist, or is not yet downloaded -- please check abo'
        print(f'loading from: {path}')

        query = f"index >= '{start}' "
        if stop:
            query += "and index <= '{stop}'"
        with pd.HDFStore(path, mode='r') as store:
            df = store.select('', where=query)
        df.sort_index(inplace=True, ascending=False)
        return df

    def terminate(self):
        self.local_frontend.close()
        self.abo_query.close()
        self.ctx.term()
        print(f'Terminated Abo Client')

class GDownloader(AuthClient):
    def __init__(self, ggm_host, pipeline, chunk_size, dataframe, *args, **kwargs):
        super().__init__(ggm_host, *args, **kwargs)

        self.pipeline = pipeline
        self.chunk_size = chunk_size
        self.dataframe = dataframe

        self.client = self.get_client()

        self.get_work = self.ctx.socket(zmq.PULL)
        self.get_work.setsockopt(zmq.LINGER, 0)
        self.get_work.connect('ipc://@work')

        self.res = self.ctx.socket(zmq.PUSH)
        self.res.setsockopt(zmq.LINGER, 0)
        self.res.connect('ipc://@result')

        self.work_loop()

    def work_loop(self):
        try:
            fullcmd = self.get_work.precv()
            self.download(fullcmd[:-1], fullcmd[-1])
        finally:
            self.terminate()

    def download(self, cmd, params):

        CHUNK_SIZE = self.chunk_size
        PIPELINE = self.pipeline

        credit = PIPELINE   # Up to PIPELINE chunks in transit
        total = 0           # Total records received
        chunks = 0          # Total chunks received
        offset = 0          # Offset of next chunk request
        cmd.append(params)

        while True:
            while credit:
                params['offset'] = offset
                params['limit']= CHUNK_SIZE
                cmd[-1] = params
                self.client.dsend(cmd)
                offset += CHUNK_SIZE
                credit -= 1
            route, msg = self.client.drecv(compression=params['compression'])
            if len(msg) > 0:
                if self.dataframe:
                    msg = self.flatten_points(msg)
                self.res.psend(msg)
            chunks += 1
            credit += 1
            size = len(msg)
            if size < CHUNK_SIZE:
                break

        # 'empty' pipeline
        while credit < PIPELINE:
            route, msg = self.client.drecv(compression=params['compression'])
            credit += 1
            if len(msg) > 0:
                if self.dataframe:
                    msg = self.flatten_points(msg)
                self.res.psend(msg)

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

    def terminate(self):
        self.get_work.close()
        self.res.close()
        self.client.close()
        self.ctx.term()
        sys.exit(0)
