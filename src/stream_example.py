from pynq.overlays.base import BaseOverlay
from pynq.lib.video import *
from PIL import Image as PIL_Image
import sys, cv2
import numpy as np


# initialize output HDMI stream
base = BaseOverlay("base.bit")
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

try:
	print("Initialize video stream!")

	# main loop- grab a frame from webcam, process it, push to HDMI
	while True:
		retcode, frame_vga = video_in.read()

		# TODO FIXME process image here 
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

except KeyboardInterrupt:
	print("Goodbye")
	video_in.release()
	hdmi_out.stop()
	del hdmi_out
	del video_in
	sys.exit()

