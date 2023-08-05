import zmq, ujson, blosc

class GSock(zmq.Socket):
    """A class with some extra serialization methods
    
    """
    def psend(self, msg, compression=False, raw=False):
        """
        """
        if not raw:
            msg = ujson.dumps(msg).encode()
        if compression:
            msg = blosc.compress(msg)

        ret = self.send(msg)
        return ret

    def precv(self, compression=False, raw=False):
        """
        """
        msg = self.recv()

        if compression:
            msg = blosc.decompress(msg)
        if not raw:
            msg = ujson.loads(msg.decode())

        return msg

    def dsend(self, msg, z_route=None, compression=False, raw=False):
        """
        sending as dealer to dealer (resource worker/client/...)

        emtpy frame for compatibility with req/rep OR zmq internal route
        """
        p = z_route or [b'']

        if not raw:
            msg = ujson.dumps(msg).encode()

        if compression:
            msg = blosc.compress(msg)

        p.append(msg)

        ret = self.send_multipart(p)
        return ret

    def drecv(self, compression=False, raw=False):
        """receiving as dealer from dealer(resource worker)
        compatible with req/rep
        """
        rawmsg = self.recv_multipart()
        route = rawmsg[:-1]

        if compression:
            rawmsg[-1] = blosc.decompress(rawmsg[-1])
        
        if not raw:
            msg = ujson.loads(rawmsg[-1].decode())
        else:
            msg = rawmsg[-1]

        #print(route, msg)
        return route, msg

class Kontext(zmq.Context):
    _socket_class = GSock
