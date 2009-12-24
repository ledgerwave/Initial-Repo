class Tracker:
    def __init__(self):
        pass
    
    def track(self, frame, lastframe):
        threshold=128
        
        diff=cvCreateImage(cvSize(frame.size[0], frame.size[1]), frame.depth, 1)
        bitimage=cvCreateImage(cvSize(frame.size[0], frame.size[1]), frame.depth, 1)
        cvAbsDiff(frame,lastframe,diff)
        cvThreshold(diff,bitimage,threshold,255,CV_THRESH_BINARY)
        return bitimage
