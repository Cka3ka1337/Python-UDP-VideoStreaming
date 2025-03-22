import time
import logging
import threading

import mss
import numpy


log = logging.getLogger(__name__)


class Capture:
    def __init__(self, count, slices) -> None:
        self.frame = None
        self.work = True
        self.size = None
        
        self.__last = time.perf_counter()
        self.__history = []
        self.__fps = 0
        
        self.__count = count
        self.slices = slices

    
    def init(self) -> None:
        log.debug('Init capture method...')
        while self.frame is None: pass
        self.size = (len(self.frame[0]), len(self.frame))
        log.debug('Successful')

    
    def start(self, func) -> None:
        threading.Thread(target=func, daemon=False).start()
        
    
    def __thr(self) -> None:
        pass
    
    
    def get_size(self) -> tuple[int, int]:
        return self.size
    
    
    def get_fps(self) -> None:
        '''
        Метрика кадров в секунду, вычисляет среднюю задержку из self.__count замеров.
        '''
        if len(self.__history) < self.__count:
            self.__history.append(
                1 / (time.perf_counter() - self.__last)
            )
        else:
            self.__fps = int(sum(self.__history) / self.__count)
            self.__history = []
        
        self.__last = time.perf_counter()
        
        return self.__fps
    
    
    def get_frame(self) -> None:
        return self.frame
    
    
    def slice(self, matrix,w_step, h_step) -> None:
        out = []
        w, h = len(matrix[0]), len(matrix)
        
        for i in range(0, h, h_step):
            for j in range(0, w, w_step):
                out.append(matrix[i: i + h_step, j: j + w_step])
        
        return out


class MSS(Capture):
    def __init__(self) -> None:
        super().__init__(30, 10)
        self.start(self.__thr)
    
    
    def __thr(self) -> None:
        with mss.mss() as sct:
            mon = sct.monitors[0]
            while self.work:
                self.frame = numpy.array(sct.grab(mon), numpy.ubyte)
                
# Тут, по-идее, можно описать свои методы захвата экрана.
# К примеру, можно впихнуть захват через виртуальную камеру OBS.




# if __name__ == '__main__':
#     logging.basicConfig(format='[%(name)s] (%(asctime)s) - %(message)s', level=logging.NOTSET, datefmt='%H:%M:%S')

#     import pickle
    
#     cap = MSS()
#     cap.init()
    
#     frame = cap.get_frame()[:20]
#     frame_b = pickle.dumps(frame)
    
#     print(pickle.loads(frame_b))