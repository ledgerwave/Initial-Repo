# Modules
from opencv.highgui import *
from opencv.cv import *

# Classes
execfile("config.py")
execfile("includes/performance.py")
execfile("includes/perspective.py")
execfile("includes/graphics.py")
execfile("includes/callibrate.py")
execfile("includes/tracker.py")

## Set up classes
speed = FpsMeter() # Set up FPS Meter
perspective = Perspective() # Make Perspective Warp Map
gfx = Graphics() # Set up graphics drawing class
callib = Callibrate() # Set up callibrate class
tracker = Tracker() # Set up motion tracker

# Mode changer for slider
def change_mode(position):
    global mode
    mode=position

# Universal function for handling a click
def handleclick(event, x, y, flags, param):
    global mode
    if mode==2 and event==CV_EVENT_LBUTTONDOWN: # Callibrate Mode
        callib.click(x, y)

# Make window & set click handler
cvNamedWindow(window_name, 1)
cvSetMouseCallback(window_name, handleclick);

# Open Camera
camera = cvCreateCameraCapture(camnum)
cvSetCaptureProperty(camera, CV_CAP_PROP_FRAME_WIDTH, width)
cvSetCaptureProperty(camera, CV_CAP_PROP_FRAME_HEIGHT, height)

mode=0 # Normal Mode

# Create Mode Slider
cvCreateTrackbar("Mode", window_name, 0, 3, change_mode);


# Main Loop.
while True:
    
    # Get Frame
    frame = cvQueryFrame(camera)

    if mode==0: # Normal Mode
        frame=gfx.draw_mode(frame,"Normal")
        frame=gfx.drawquad(frame)
    
    elif mode==1: # Track/effects Mode
        frame=tracker.track(frame, lastframe)
        frame.gfx.draw_mode(frame, "Track Mode")
       
    elif mode==2: # Transform Mode
        frame = perspective.warp(frame)
        frame=gfx.draw_mode(frame,"Transform")
    elif mode==3: # Callibrate Mode
        frame=gfx.draw_mode(frame,"Callibrate Mode")
        frame=gfx.drawquad(frame)

    # Write FPS
    frame = gfx.fps(frame, speed.go())
    
    # For motion tracking
    lastframe=cvCloneImage(frame)
    
    # Post frame to window
    cvShowImage(window_name, frame)
    
    # Wait for 1ms (to stop freezing)
    cvWaitKey(2)
