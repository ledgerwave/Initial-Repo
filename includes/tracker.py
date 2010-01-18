class Tracker:
    def __init__(self):
        pass
    
    def filter_motion(self, frame, lastframe):
        global motion_threshold

        diff=cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        
        greyframe=cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        greylastframe=cvCreateImage(cvSize(lastframe.width, lastframe.height), lastframe.depth, 1)
        bitimage=cvCreateImage(cvSize(frame.width, frame.height), frame.depth, 1)
        
        cvCvtColor(frame, greyframe, CV_RGB2GRAY)
        cvCvtColor(lastframe, greylastframe, CV_RGB2GRAY)
        
        cvAbsDiff(greyframe, greylastframe, diff)
        cvThreshold(diff, bitimage, motion_threshold, 255, CV_THRESH_BINARY)
        return bitimage

	
