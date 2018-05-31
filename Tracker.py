from AbstractTracker import *
import dlib
from enum import Enum
import pdb
import cv2
import numpy as np
import sys

class TrackerType(Enum):
    DLIB = 1
    ROLO = 2
    DEEPSORT = 3
    TRACK2DETECT = 4
    KLT = 5
    GOTURN = 6



# class that handles tracking computation
class DLIBTracker(AbstractTracker):

    # Constuctor
    def __init__(self, tracker_type=TrackerType.DLIB): 
        # initializing the type of tracker to be used
        self.tracker_type = tracker_type
        self.tracker = None

    # initialize the tracker
    def start_tracking(self, rectangle,frame):
        """Initializes and starts the dlib tracker
        params: rectangle - a list [xmin, ymin, xmax, ymax]
                frame - np.array() initial image frame
        return: None"""
        if self.tracker_type == TrackerType.DLIB:
            self.tracker = dlib.correlation_tracker()
            dlib_rect = dlib.rectangle(*rectangle)
            self.tracker.start_track(frame, dlib_rect)
            return None

    # update the tracker
    def update_frame(self, frame):
        """Updates the tracked rectangle
        params: frame - np.array() image frame used for computation
        return: rectangle - a list [xmin, ymin, xmax, ymax]"""
        self.tracker.update(frame)
        track_rect = self.tracker.get_position()
        xmin = int(track_rect.left())
        ymin = int(track_rect.top())
        xmax = int(track_rect.right())
        ymax = int(track_rect.bottom())
        result = [xmin,ymin,xmax,ymax]
        return result 



class GOTURNTracker(AbstractTracker):

# Constuctor
    def __init__(self, tracker_type=TrackerType.GOTURN):
        # initializing the type of tracker to be used
        self.tracker_type = tracker_type
        self.tracker = None

    # initialize the tracker
    def start_tracking(self, rectangle,frame):
        """Initializes and starts the dlib tracker
        params: rectangle - a list [xmin, ymin, xmax, ymax]
                frame - np.array() initial image frame
        return: None"""
        if self.tracker_type == TrackerType.GOTURN:
            self.tracker = cv2.TrackerGOTURN_create()
            goturn_rect = rectangle
            self.tracker.init(frame, goturn_rect)
            return None

    # update the tracker
    def update_frame(self, frame):
        """Updates the tracked rectangle
        params: frame - np.array() image frame used for computation
        return: rectangle - a list [xmin, ymin, xmax, ymax]"""
        ok,bbox=self.tracker.update(frame)
        if ok:
            # Tracking success
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[0] + bbox[2])
            ymax = int(bbox[1] + bbox[3])
        result = [xmin,ymin,xmax,ymax]
        return result


def cv_tracking():
    """tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN']
    tracker_type = tracker_types[0]

    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
        tracker = cv2.TrackerGOTURN_create()"""

     # Read video
    video = cv2.VideoCapture("/home/ujjawal/project/Tracking-Detection/tankdemo.mp4")
    ok, frame = video.read()

    # check for video
    if not video.isOpened():
        print("video not opened")
        sys.exit()

    # Read first frame.
    count = 0
    while (count < 6300):
        ok, frame = video.read()
        if not ok:
            print ('Cannot read video file')
            sys.exit()

        count += 1

    # Define an initial bounding box
    # bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    #ok = tracker.init(frame, bbox)
    gt = GOTURNTracker()
    gt.start_tracking(bbox,frame)
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        #ok, bbox = tracker.update(frame)
        bbox = gt.update_frame(frame)
        print(bbox)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display tracker type on frame
        #cv2.putText(frame, tracker_type + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2);

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break
if __name__ == "__main__":
    cv_tracking() 






