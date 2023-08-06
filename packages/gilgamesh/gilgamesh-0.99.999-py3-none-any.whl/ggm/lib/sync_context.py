import zmq, ujson, blosc

class GSock(zmq.Socket):
    """A class with some extra serialization methods
    
    """
    BLOSC_ARGS = {
            'typesize': 1,
            'clevel': 5,
            'shuffle': blosc.SHUFFLE,
            'cname': 'blosclz'
    }
    def psend(self, msg, compression=False, raw=False):
        """
        """
        if not raw:
            msg = memoryview(ujson.dumps(msg).encode())
        if compression:
            msg = memoryview(blosc.compress(msg, **self.BLOSC_ARGS))

        ret = self.send(msg, copy=False)
        return ret

    def precv(self, compression=False, raw=False):
        """
        """
        msg = self.recv(copy=False)

        if compression:
            msg = memoryview(blosc.decompress(msg))
        if not raw:
            msg = ujson.loads(bytes(msg).decode())

        return msg

    def dsend(self, msg, z_route=None, compression=False, raw=False):
        """
        sending as dealer to dealer (resource worker/client/...)

        emtpy frame for compatibility with req/rep OR zmq internal route
        """
        p = z_route or [b'']

        if not raw:
            msg = memoryview(ujson.dumps(msg).encode())
        if compression:
            msg = memoryview(blosc.compress(msg, **self.BLOSC_ARGS))

        p.append(msg)

        ret = self.send_multipart(p, copy=False)
        return ret

    def drecv(self, compression=False, raw=False):
        """receiving as dealer from dealer(resource worker)
        compatible with req/rep
        """
        rawmsg = self.recv_multipart(copy=False)
        route = rawmsg[:-1]

        if compression:
            rawmsg[-1] = memoryview(blosc.decompress(rawmsg[-1]))
        if not raw:
            msg = ujson.loads(bytes(rawmsg[-1]).decode())
        else:
            msg = rawmsg[-1]

        return route, msg

class Kontext(zmq.Context):
    _socket_class = GSock
