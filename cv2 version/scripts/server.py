import zlib
import socket
import pickle
import logging
import threading

import numpy


log = logging.getLogger(__name__)


class User:
    def __init__(self, s, addr) -> None:
        self.s = s
        self.addr = addr
        self.prev = None
        
        self.__send_connect_callback()
        
    
    def __send_connect_callback(self) -> None:
        self.s.sendto(
            zlib.compress(
                pickle.dumps({'command': 'CONNECTED'})
            ),
            self.addr
        )

    
    def __send_frame(self, slice, pos) -> None:
        self.s.sendto(
            zlib.compress(
                pickle.dumps({'command': 'setslice', 'frame': slice, 'pos': pos})
            ),
            self.addr
        )
    
    
    def send_frames(self, frames: list, w_step: int, h_step: int, slices: int) -> None:
        idx = 0
        
        for y in range(0, h_step * slices, h_step):
            for x in range(0, w_step * slices, w_step):
                if self.prev is not None:
                    if not numpy.array_equal(self.prev[idx], frames[idx]):
                        self.__send_frame(frames[idx], (x, y))
                    # else:
                    #     frame = numpy.zeros_like(frames[idx])
                    #     frame[:, :, 1] = 200
                    #     self.__send_frame(frame, (x, y))
                else:
                    self.__send_frame(frames[idx], (x, y))
                idx += 1

        self.prev = frames
                

class Server:
    def __init__(self, addr: tuple[str, int]) -> None:
        log.debug('Init server...')
        
        self.addr = addr
        self.work = True
        self.user = None
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind(addr)
        
        threading.Thread(target=self.__listener, daemon=False).start()
        log.debug('Successful')
        
    
    def __listener(self) -> None:
        while self.work:
            try:
                data, addr = self.s.recvfrom(4096)
            except:
                continue
            data = pickle.loads(zlib.decompress(data))
            log.debug(f'Data from - {addr}: {data}')
            
            if 'command' in data:
                if data['command'] == 'CONNECTION':
                    self.user = User(
                        self.s,
                        addr
                    )

                    log.debug(f'Connected - {addr}')

    
    def send_frames(self, frames: list, w_step: int, h_step: int, slices: int) -> None:
        if self.user is not None:
            self.user.send_frames(frames, w_step, h_step, slices)
    

# if __name__ == '__main__':
#     logging.basicConfig(format='[%(name)s] (%(asctime)s) - %(message)s', level=logging.NOTSET, datefmt='%H:%M:%S')

#     server = Server(('127.0.0.1', 40000))
#     while True:
#         pass