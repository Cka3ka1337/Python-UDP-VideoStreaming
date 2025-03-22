import logging

import cv2

from scripts.client import Client


def main():
    logging.basicConfig(format='[%(name)s] (%(asctime)s) - %(message)s', level=logging.NOTSET, datefmt='%H:%M:%S')
    
    
    client = Client(('127.0.0.1', 40000))
    client.connect()
    
    while True:
        frame = client.frame
        
        cv2.imshow(__name__, frame)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()