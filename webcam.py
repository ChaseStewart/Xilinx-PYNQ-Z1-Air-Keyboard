from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
from pynq import PL
from PIL import Image as PIL_Image
import sys, cv2, math, copy
from time import time
import numpy as np
import asyncio
import datetime
import imutils

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
# initialize the first frame in the video stream
firstFrame = None

try:
	# main loop- grab a frame from webcam, process it, push to HDMI
	print("Initialize video stream!")
	while program_is_running == True:
		retcode, frame_vga = video_in.read()
		# if the first frame is None, initialize it
		if firstFrame is None:
			outframe = hdmi_out.newframe()
			outframe[0:480, 0:640,:] = frame_vga[0:480,0:640,:]
			outframe1 = cv2.cvtColor(outframe, cv2.COLOR_RGB2GRAY)
			outframe1 = imutils.resize(outframe1,height=480,width=640)
			firstFrame = outframe
			continue
			
		elif retcode == True:
			outframe = hdmi_out.newframe()

			# TODO FIXME process image here
			outframe[0:480, 0:640,:] = frame_vga[0:480,0:640,:]
			
			#outframe = imutils.resize(outframe, width=500)
			gray = cv2.cvtColor(outframe, cv2.COLOR_RGB2GRAY)
			gray = imutils.resize(gray,height=480,width=640)
			#gray_expanded = gray[:, :, np.newaxis]
			#gray = cv2.GaussianBlur(gray, (21, 21), 0)	
			
			cv2.rectangle(outframe,(20,120),(119,360),(255,0,0),2)
			cv2.rectangle(outframe,(120,120),(219,360),(255,0,0),2)
			cv2.rectangle(outframe,(220,120),(319,360),(255,0,0),2)
			cv2.rectangle(outframe,(320,120),(419,360),(255,0,0),2)
			cv2.rectangle(outframe,(420,120),(519,360),(255,0,0),2)
			cv2.rectangle(outframe,(520,120),(619,360),(255,0,0),2)
			
			# compute the absolute difference between the current frame and
			# first frame
			frameDelta = cv2.absdiff(outframe1, gray)
			#thresh = cv2.cvtColor(frameDelta, cv2.COLOR_RGB2GRAY)
			thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
 
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			thresh = cv2.dilate(thresh, None, iterations=2)
			(im2, contours, hierarchy) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			 
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			for c in contours:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < 1000:
					continue
				x, y, w, h = cv2.boundingRect(c)
				cv2.rectangle(outframe, (x, y), (x + w, y + h), (0, 255, 0), 2)
			
			hdmi_out.writeframe(outframe)	

		#you reached the end of video	
		else:
			print("Failed!")
			#break
		
		if (time()-starttime > 30 ):
			print("Timeout- terminate program")
			program_is_running = False

	# after 30s, close the stream 
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
	
except RuntimeError:
	print("Goodbye")
	video_in.release()
	hdmi_out.stop()
	del hdmi_out
	del video_in
	sys.exit()
