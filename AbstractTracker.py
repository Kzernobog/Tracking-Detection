from abc import ABC, abstractmethod

class AbstractTracker(ABC):

    # constructor
    @abstractmethod 
    def __init__(self):
        pass

    # start tracking
    @abstractmethod
    def start_tracking(self):
        pass

    # update the frame
    @abstractmethod
    def update_frame(self):
        pass





