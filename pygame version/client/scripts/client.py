import time
import zlib
import socket
import pickle
import logging
import threading

import pygame


log = logging.getLogger(__name__)


class Client:
    def __init__(self, addr: tuple[str, int]) -> None:
        log.debug('Init client...')
        
        self.w, self.h = 0, 0
        self.work = True
        self.addr = addr
        self.__connected = False
        
        self.frame = pygame.Surface((1920 // 2, 1200 // 2))
        self.frame.fill((255, 255, 255))
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        threading.Thread(target=self.__listener, daemon=False).start()

        log.debug('Successful')
    
    
    def __listener(self) -> None:
        while self.work:
            try:
                data, addr = self.client.recvfrom(65535)
            except OSError:
                continue
                
            # log.debug(f'{len(data), addr}')
            data = pickle.loads(zlib.decompress(data))
            
            if 'command' in data:
                if data['command'] == 'DISCONNECTION':
                    self.work = False
                    log.debug(f'Connnection closed - {addr}')
                
                
                elif data['command'] == 'CONNECTED':
                    self.__connected = True
                    log.debug(f'Connected - {self.addr}')
                
                
                elif data['command'] == 'setattr':
                    setattr(self, data['attr'], data['value'])
                    log.debug(f'Setattr {data['attr'], data['value']}')
                
                
                elif data['command'] == 'setslice':
                    frame = pygame.transform.flip(
                        pygame.transform.rotate(
                            pygame.surfarray.make_surface(data['frame']),
                            -90
                        ),
                        True,
                        False
                    )
                    self.frame.blit(
                        frame,
                        data['pos']
                    )
    
    
    def connect(self) -> None:
        log.debug(f'Try connect - {self.addr}')

        while not self.__connected:
            self.client.sendto(
                zlib.compress(
                    pickle.dumps(
                        {
                            'command': 'CONNECTION'
                        }
                    )
                ),
                self.addr
            )
            
            time.sleep(1)