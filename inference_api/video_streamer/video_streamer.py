import cv2
import errno
import imagezmq
import os
import socket


def create_streamer(file, connect_to='tcp://0.0.0.0:5555', loop=True): #or run cmd terminal to get ip adress: ifconfig | grep "inet "
 
    """
    You can use this function to emulate an IP camera for the counting apps.

    Parameters
    ----------
    file : str
        Path to the video file you want to stream.
    connect_to : str, optional
        Where the video shall be streamed to.
        The default is 'tcp://127.0.0.1:5555'. if you're tunning it in a pc
    loop : bool, optional
        Whether the video shall be looped. The default is True.

    Returns
    -------
    None.

    """
    
    # check if file exists and open capture
    if os.path.isfile(file):
        cap = cv2.VideoCapture(file)
    else:
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)
    
    # prepare streaming
    sender = imagezmq.ImageSender(connect_to=connect_to)
    host_name = socket.gethostname()
    
    while True:
        ret, frame = cap.read()
        
        if ret:
            # if a frame was returned, send it
            sender.send_image(host_name, frame)
        else:
            # if no frame was returned, either restart or stop the stream
            if loop:
                cap = cv2.VideoCapture(file)
            else:
                break


if __name__ == '__main__':
   
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    video_path = os.path.join(BASE_DIR, "cars.mp4")
    streamer = create_streamer(video_path)
