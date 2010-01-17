#!/usr/bin/python
# Modules
from opencv.highgui import *
from opencv.cv import *
import os

# Classes
execfile(os.getcwd()+"/config.py")
execfile(os.getcwd()+"/includes/performance.py")
execfile(os.getcwd()+"/includes/perspective.py")
execfile(os.getcwd()+"/includes/graphics.py")
execfile(os.getcwd()+"/includes/callibrate.py")
execfile(os.getcwd()+"/includes/tracker.py")

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

# Motion threshold slider
def change_threshold(thresh):
	global motion_threshold
	motion_threshold=thresh

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

# Create Motion threshold slider
motion_threshold=0
cvCreateTrackbar("Threshold", window_name, 0, 255, change_threshold);

running=True

lastframe=cvCreateImage(cvSize(width, height), 8, 3)

try:
	# Main Loop.
	while running:
		
		# Get Frame
		frame = cvQueryFrame(camera)
		
		if mode==0: # Normal Mode
			frame=gfx.draw_mode(frame,"Normal")
			frame=gfx.drawquad(frame)
		
		elif mode==1: # Track/effects Mode
			
			# Preserve the frame
			preserved_frame=cvCloneImage(frame)
			
			frame=tracker.track(frame, lastframe)
			frame=gfx.draw_mode(frame, "Motion Mode")
			
			# Make a copy
			lastframe=cvCloneImage(preserved_frame)
		   
		elif mode==2: # Transform Mode
			frame = perspective.warp(frame)
			frame=gfx.draw_mode(frame,"Transform")
		
		elif mode==3: # Callibrate Mode
			frame=gfx.draw_mode(frame,"Callibrate Mode")
			frame=gfx.drawquad(frame)

		# Write FPS
		frame = gfx.fps(frame, speed.go())
		
		# Post frame to window
		cvShowImage(window_name, frame)
		
		# Wait for 1ms (to stop freezing)
		cvWaitKey(2)
except KeyboardInterrupt:
	running=False
