# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

"""
simple media player based on opencv
support web camera / video file / live url
press ESC key to quit playing

Authors: etworker

usage example:
    # play with local camera
    python media_player.py --uri 0
    
    # play with local video file test.mp4, display in full screen
    python media_player.py --uri test.mp4 --full

    # play with live url rtmp://192.168.0.191:1935/live1/
    python media_player.py --uri rtmp://192.168.0.191:1935/live1/

    # play with live url rtmp://192.168.0.191:1935/live1/ and save to file out.avi
    python media_player.py --uri rtmp://192.168.0.191:1935/live1/ --output out.avi
"""

import cv2, os, sys, time, getopt

class media_player:
    def __init__(self):
        self.media_uri = 0
        self.is_full_screen = False
        self.is_save = False
        self.filename = "out.avi"

    def parse_args(self, argv):
        pyname = os.path.basename(argv[0])
        usage = "%s -i <media_uri> [-f] [-o xxx.avi]" % pyname
        
        try:
            opts, args = getopt.getopt(argv[1:],"hfso:i:",["help", "full", "output=", "uri="])
        except getopt.GetoptError:
            print usage
            return False

        for opt, arg in opts:
            if opt in ["-h", "--help"]:
                print usage
                return False
            elif opt in ["-f", "--full"]:
                self.is_full_screen = True
            elif opt in ("-i", "--uri"):
                if self.is_number(arg):
                    self.media_uri = int(arg)
                else:
                    self.media_uri = arg                    
            elif opt in ("-o", "--output"):
                self.is_save = True
                self.filename = arg
            else:
                pass
                
        return True

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def is_media_file(self, media_uri):
        uri = str(media_uri)

        return not (self.is_number(uri) or "://" in uri)
    
    def get_fps(self, cap):
        fps = 0
        try:
            fps = int(round(cap.get(5)))
        except Exception as e:
            print "can not read fps"

        return fps

    # get media info: w,h,fps
    def get_media_info(self, cap):
        w = int(round(cap.get(3)))     # CV_CAP_PROP_FRAME_WIDTH
        h = int(round(cap.get(4)))     # CV_CAP_PROP_FRAME_HEIGHT
        fps = self.get_fps(cap)

        return w,h,fps

    def play(self, uri=None):
        if uri is None:
            media_uri = self.media_uri
        else:
            media_uri = uri            
            
        # open media
        cap = cv2.VideoCapture(media_uri)
        if not cap.isOpened():
            print "open media", media_uri, "failed"
            return

        w,h,fps = self.get_media_info(cap)
        print "media info: w=%d, h=%d, fps=%d" % (w,h,fps)

        if self.is_save:
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')
            if fps == 0:
                out = cv2.VideoWriter(self.filename, fourcc, 15, (w,h))
            else:
                out = cv2.VideoWriter(self.filename, fourcc, fps, (w,h))

        # get fps
        sleep_time = 0
        if self.is_media_file(media_uri) and (fps > 0):
            sleep_time = 1.0/fps
            print "fps=%d, sleep_time=%.2f ms" % (round(fps), sleep_time*1000)
        
        # window name
        wn = str(media_uri)
        if self.is_full_screen:
            # cv2.namedWindow(wn, cv2.WND_PROP_FULLSCREEN)
            # cv2.setWindowProperty(wn, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.namedWindow(wn, 0)
            cv2.setWindowProperty(wn, 0, 1)

        # repeat read frame
        while(cap.isOpened()):
            t = time.time()

            # read video frame
            ret, frame = cap.read()
            if not ret:
                print "no frame available, break here"
                break

            # ESC Key to quit
            k = cv2.waitKey(1) & 0xff
            if k == 27:
                print "quit"
                break
            elif k == ord('f'):
                cv2.setWindowProperty(wn, 0, 1)

            # save to video file
            if self.is_save:
                out.write(frame)

            # show frame
            cv2.imshow(wn,frame)
            
            # sleep for media file
            t = sleep_time - time.time() + t
            if (sleep_time > 0) and (t > 0):
                time.sleep(t)
            
        # release opencv windows resources
        if self.is_save:
            out.release()
            
        cap.release()
        cv2.destroyAllWindows()
        
        print "all finished"
        
def unit_test():
    # uri = 0                                     # local camera
    # uri = "hand3.mp4"                           # local media file
    uri = "rtmp://192.168.0.25:1935/live1/10003"    # live uri

    player = media_player()
    player.is_full_screen = False
    player.play(uri)
    
def main():
    player = media_player()
    if player.parse_args(sys.argv):
        print "media_uri=%s" % player.media_uri
        player.play()

if __name__ == '__main__':
    # unit_test()
    main()