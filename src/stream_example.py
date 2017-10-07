from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
from PIL import Image as PIL_Image
import sys, cv2
import numpy as np


base = BaseOverlay("base.bit")
# TODO initialize a input webcam
my_mode = VideoMode(640, 480, 24)
hdmi_out = base.video.hdmi_out
hdmi_out.configure(my_mode, PIXEL_BGR)
hdmi_out.start()
print("Initialize output_HDMI")


# initialize an output HDMI stream
video_in = cv2.VideoCapture(0)
video_in.set(cv2.CAP_PROP_FRAME_WIDTH,  640 )
video_in.set(cv2.CAP_PROP_FRAME_HEIGHT, 480 )
print("Initialize video")

try:
	print("Initialize video stream!")

	while True:
		retcode, frame_vga = video_in.read()
		if retcode == True:
			outframe = hdmi_out.newframe()
			outframe[0:480, 0:640,:] = frame_vga[0:480,0:640,:]
			hdmi_out.writeframe(outframe)
	
		else:
			print("Failed! Exiting...")
			video_in.release()
			hdmi_out.stop()
			del hdmi_out
			del video_in
			sys.exit()

except KeyboardIAP_PROP_FRAME_WIDTH
	print("Goodbye")
	video_in.release()
	hdmi_out.stop()
	del hdmi_out
	del video_in
	sys.exit()

