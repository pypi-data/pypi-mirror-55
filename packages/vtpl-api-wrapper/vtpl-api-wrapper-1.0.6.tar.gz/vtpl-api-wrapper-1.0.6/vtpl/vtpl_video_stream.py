# import the necessary packages
from threading import Thread, Event
import sys
import cv2
import time
from urllib.parse import urlparse

# import the Queue class from Python 3
if sys.version_info >= (3, 0):
    from queue import Queue, Full, Empty

# otherwise, import the Queue class for Python 2.7
else:
    from Queue import Queue


class VtplVideoStream:
    def __init__(self, path, stop_when_finished=True, transform=None, queue_size=25, suggested_fps=25):
        # initialize the file video stream along with the boolean
        # used to indicate if the thread should be stopped or not
        self.__stream_type = None
        self.__stream_url = None
        self.__reconnect_requested = False
        self.__stop_when_finished = stop_when_finished
        self.__stop_when_finished_flagged = False
        if path != '':
            url = urlparse(path)
            self.__stream_type = url.scheme
            self.__stream_url = url.geturl()
        self.__stream = None
        self.__is_stopped = Event()
        self.__file_fps = suggested_fps
        self.__transform = transform
        # initialize the queue used to store frames read from
        # the video file
        self.__Q = None
        self.__Q2 = Queue(maxsize=5)
        self.__thread = None
        if queue_size > 0:
            self.__Q = Queue(maxsize=queue_size)
            # intialize thread
            self.__thread = Thread(target=self.__do_task, args=())
            self.__thread.daemon = True

        self.__input_fps = 0
        self.__input_last_frame_time = 0
        self.__input_frame_count = 0
        self.__output_fps = 0
        self.__output_frame_count = 0
        self.__output_last_frame_time = 0

    def change_source_url(self, path):
        if path == '':
            return
        url = urlparse(path)
        new_stream_type = url.scheme
        new_stream_url = url.geturl()
        if (new_stream_type != self.__stream_type) or (new_stream_url != self.__stream_url):
            self.__stream_type = new_stream_type
            self.__stream_url = new_stream_url
            self.__reconnect_requested = True

    def start(self):
        # start a thread to read frames from the file video stream
        self.__reconnect_requested = True

        if self.__thread is not None:
            self.__thread.start()
        return self

    def __reconnect(self):
        print("Reconnect 1 {}".format(self.__stream_url))
        if self.__stop_when_finished:
            self.__stop_when_finished_flagged = True
        if self.__stream is not None:
            self.__stream.release()
            self.__stream = None
            time.sleep(1)
        if self.__stream_url is not None:
            if self.__stream_url != '':
                self.__stream = cv2.VideoCapture(self.__stream_url)
            else:
                print("Discarding reconnect")
        else:
            print("Discarding reconnect")

    def __do_task(self):
        #print("Do Task started")
        while not self.__is_stopped.is_set():
            if self.__reconnect_requested:
                self.__reconnect_requested = False
                self.__reconnect()
            if self.__stream is None:
                continue
            if (self.__stream_type == 'file'):
                if (self.__file_fps <= 0):
                    self.__file_fps = 10
                time.sleep(1.0 / self.__file_fps)
            else:
                pass
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Before READ **************************************")
            (grabbed, frame) = self.__stream.read()
            # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ After READ **************************************")
            # print(grabbed,frame)

            if grabbed == False or frame is None:
                if self.__stop_when_finished_flagged:
                    print(
                        "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ Breaking as no repeat requested ***********")
                    break
                else:
                    self.__reconnect()
                    continue
            else:
                try:
                    self.__Q.put(frame, block=True, timeout=0.0001)
                    self.__input_frame_count += 1
                    t = time.time()
                    if (self.__input_last_frame_time == 0):
                        self.__input_last_frame_time = t
                    diff = t - self.__input_last_frame_time
                    if (diff > 10.0):
                        self.__input_fps = (self.__input_frame_count/diff)
                        # print("input FPS is ::" + str(self.__input_fps))
                        self.__input_last_frame_time = t
                        self.__input_frame_count = 0

                except Full:
                    pass
                try:
                    self.__Q2.put(frame, block=True, timeout=0.0001)
                except Full:
                    pass

        self.__stream.release()

    def read_mjpeg(self, time_out_in_sec=1.0):
        frame = None
        entry_time = time.time()
        while not self.__is_stopped.is_set() and (time.time() < (entry_time + time_out_in_sec)):
            try:
                frame = self.__Q2.get(block=True, timeout=0.0001)
                break
            except Empty:
                continue
        return frame

    def read(self, time_out_in_sec=30.0):
        # return next frame in the queue
        frame = None
        if self.__Q is None:
            (grabbed, frame) = self.__stream.read()
            # return frame
        else:
            entry_time = time.time()
            while (not self.__is_stopped.is_set()) and (time.time() < (entry_time + time_out_in_sec)):
                try:
                    frame = self.__Q.get(block=True, timeout=0.0001)
                    break
                except Empty:
                    continue

            # print(entry_time)

        if frame is not None:
            self.__output_frame_count += 1

            t = time.time()
            if (self.__output_last_frame_time == 0):
                self.__output_last_frame_time = t
            diff = t-self.__output_last_frame_time
            if (diff > 10.0):
                self.__output_fps = (self.__output_frame_count/diff)
                self.__output_last_frame_time = t
                self.__output_frame_count = 0
                # print("output FPS is ::" + str(self.__output_fps))

        return frame

    # Insufficient to have consumer use while(more()) which does
    # not take into account if the producer has reached end of
    # file stream.
    def running(self):
        return self.__more() or not self.__is_stopped.is_set()

    def __more(self):
        # return True if there are still frames in the queue. If stream is not stopped, try to wait a moment
        tries = 0
        while self.__Q.qsize() == 0 and not self.__is_stopped.is_set() and tries < 5:
            time.sleep(0.1)
            tries += 1

        return self.__Q.qsize() > 0

    def stop(self):
        # indicate that the thread should be stopped
        self.__is_stopped.set()

        # wait until stream resources are released (producer thread might be still grabbing frame)
        if self.__thread is not None:
            self.__thread.join()

    def print_output_fps(self):

        return self.__output_fps

    def print_input_fps(self):

        return self.__input_fps

    def stopped(self):
        return self.__is_stopped.is_set()


if __name__ == "__main__":
    #source = "http://event.iot-videonetics.com/streaming/live/hls/00000000-0000-0000-0000-000ffc51510e-minor/play.m3u8"
    source = "http://192.168.1.166/192.168.1.166:8085/stream/EM-09546/00010010-0001-1020-8000-48ea63a6665c/clip/minor/2019/10/03/index.m3u8"
    #source = "https://content.jwplatform.com/manifests/yp34SRmf.m3u8"
    x = VtplVideoStream(source, False)

    x.start()
    while True:
        image1 = x.read(30.0)
        if image1 is not None:
            cv2.imshow("test", image1)
            cv2.waitKey(1)
        else:
            print("No images found breaking")
            break
    print("Came out of the loop")
    x.stop()
