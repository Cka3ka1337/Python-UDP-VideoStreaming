import logging

import cv2

from scripts.capture import MSS
from scripts.server import Server


def main():
    logging.basicConfig(format='[%(name)s] (%(asctime)s) - %(message)s', level=logging.NOTSET, datefmt='%H:%M:%S')

    cap = MSS()
    cap.init()
    
    w, h = cap.get_size()
    w //= 2
    h //= 2
    w_step, h_step = w // cap.slices, h // cap.slices
    
    server = Server(('127.0.0.1', 40000))
    
    
    while True:
        frame = cv2.cvtColor(
            cv2.resize(
                cap.get_frame(),
                (w, h)
            ),
            cv2.COLOR_RGBA2RGB
        )
        
        frames = cap.slice(frame, w_step, h_step)
        
        server.send_frames(frames, w_step, h_step, cap.slices)


if __name__ == '__main__':
    main()