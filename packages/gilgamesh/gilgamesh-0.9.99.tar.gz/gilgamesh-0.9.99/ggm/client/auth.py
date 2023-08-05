from pathlib import Path
import json, socket, zmq.auth
from ..lib.sync_context import Kontext

class AuthClient(object):
    def __init__(self, ggm_host, *args, **kwargs):
        """
        gna
        """

        cfg_file = Path.home()/'.gilgamesh'/'config'/'client_config.json'
        if not cfg_file.exists():
            raise FileNotFoundError(f'{cfg_file} does not exist.')
        
        with open(cfg_file, 'r') as raw:
            cfg = json.load(raw)
        
        if not ggm_host in cfg:
            raise ValueError(f'{ggm_host} not found in config.')

        cfg = cfg[ggm_host]
        
        self.ctx = Kontext()
        self.client = self.ctx.socket(zmq.DEALER)
        
        keys_path = Path.home()/'.gilgamesh'/'keys'
        client_secret_file = keys_path/'private_keys'/f'{cfg["client_key"]}.key_secret'
        server_public_file = keys_path/'public_keys'/f'{cfg["server_key"]}.key'
        
        client_public, client_secret = zmq.auth.load_certificate(client_secret_file)
        server_public, _ = zmq.auth.load_certificate(server_public_file)
        
        self.client.curve_secretkey = client_secret
        self.client.curve_publickey = client_public
        self.client.curve_serverkey = server_public
        
        if not 'ip' in cfg:
            try:
                ip = socket.gethostbyname(cfg['hostname'])
                cfg['ip'] = ip
            except:
                raise ConnectionError(f'Could not resolve {hostname}')

        self.client.connect(f'tcp://{cfg["ip"]}:{cfg["port"]}')

        self.ip = cfg['ip']
