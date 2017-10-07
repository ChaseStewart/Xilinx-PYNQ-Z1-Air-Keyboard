from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
from pynq import PL
from PIL import Image as PIL_Image
import sys, cv2, math, copy
from time import time
import numpy as np
import asyncio
#from appscript import app

program_is_running = True

base = BaseOverlay("base.bit")
# initialize output HDMI stream
my_mode = VideoMode(640, 480, 24)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(my_mode, None ) 
hdmi_out.start()
print("Initialize output_HDMI")

# initialize input USB video capture
video_in = cv2.VideoCapture(0)
video_in.set(cv2.CAP_PROP_FRAME_WIDTH,  640 )
video_in.set(cv2.CAP_PROP_FRAME_HEIGHT, 480 )
print("Initialize video")
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
threshold = 60  #  BINARY threshold
blurValue = 41  # GaussianBlur parameter
bgSubThreshold = 50

starttime = time()
# variables
isBgCaptured = 0   # bool, whether the background captured
triggerSwitch = False  # if true, keyborad simulator works

try:
	# main loop- grab a frame from webcam, process it, push to HDMI
	print("Initialize video stream!")
	while program_is_running == True:
		retcode, frame_vga = video_in.read()
		if retcode == True:
			outframe = hdmi_out.newframe()

			#bgModel = cv2.BackgroundSubtractorMOG2(0, bgSubThreshold)
			#isBgCaptured = 1
			#print("Background Captured")
			# TODO FIXME process image here
			outframe[0:480, 0:640,:] = frame_vga[0:480,0:640,:]

			cv2.rectangle(outframe,(20,120),(119,360),(255,0,0),2)
			cv2.rectangle(outframe,(120,120),(219,360),(255,0,0),2)
			cv2.rectangle(outframe,(220,120),(319,360),(255,0,0),2)
			cv2.rectangle(outframe,(320,120),(419,360),(255,0,0),2)
			cv2.rectangle(outframe,(420,120),(519,360),(255,0,0),2)
			cv2.rectangle(outframe,(520,120),(619,360),(255,0,0),2)
			hdmi_out.writeframe(outframe)
			#bgModel = None
			#triggerSwitch = False
			#isBgCaptured = 0
			#print("Reset BackGround")
		else:
			print("Failed!")
		
		if (time()-starttime > 20 ):
			print("Timeout- terminate program")
			program_is_running = False

	# after 20s, close the stream 
	print("Closing, goodbye!")
	video_in.release()
	hdmi_out.stop()
	del video_in
	del hdmi_out
	sys.exit()

# TODO we wish this would work but jupyter is handling SIGINT 
except KeyboardInterrupt:
	print("Goodbye")
	video_in.release()
	hdmi_out.stop()
	del hdmi_out
	del video_in
	sys.exit()
