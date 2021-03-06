import cv2
from PIL import ImageGrab, Image, ImageOps
import numpy as np 

#Resolution to resize everything to
high_def = (500, 422)

#Defines color value of green
lower_green = np.array([0, 50, 0])
higher_green = np.array([255, 255, 255])


def GetScreen():
	#Grabs screen and turns it into Numpy Array
	img = ImageGrab.grab()
	img_np = np.array(img)

	#Messes with the screen to get it looking proper
	RGB_Screen = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
	Final_Screen = Image.fromarray(RGB_Screen)
	im_mirror = ImageOps.mirror(Final_Screen)
	Final_Screen = im_mirror.resize(high_def)

	return Final_Screen

def MakeMask(makeFrame):
	#Converts frame of Mask video to 8-bit greyscale image, pretty sure Final_mask.convert is useless here but eh fuck it
	get_mask = cv2.inRange(makeFrame, lower_green, higher_green)
	#watch as I define Final_Mask three times
	Final_mask = Image.fromarray(get_mask) 
	Final_mask = Final_mask.convert("L")
	Final_mask = Final_mask.resize(high_def)
	

	return Final_mask





while True:
	
	#takes and reads the mask video and the animated Lily loop, you can replace the two videos here with two of your own and it should work just fine
	isclosed = 0
	mask_read = cv2.VideoCapture('LilyMask.mp4')
	video_read = cv2.VideoCapture('LilyLoopBeta.mp4')

	#not sure why a second while True loop is needed but it doesnt work without it
	while (True):
		#gets and converts video frame to an array
		ret, mask_frame = mask_read.read()
		ret2, video_frame = video_read.read()
		
		#repeats and plays video
		if ret and ret2 == True:
			
			video2image = Image.fromarray(video_frame)
			video2image = video2image.resize(high_def)
			
			#creates a blend of the screen and the loop then pastes that onto another a non blended version of the loop, using the frame from the mask video as a mask
			im = Image.blend(GetScreen(), video2image, 0.5)
			im = Image.composite(im, video2image, MakeMask(mask_frame))

			#i can only get it to display using CV2 so it has to be converted back to an array
			display = np.copy(im)

			#if you want the windows from to say a specific thing, put that title in the quotation marks
			cv2.imshow('', display)


			#waits for the escape key to be pressed before closing the program, clicking the X to close WILL NOT WORK
			if cv2.waitKey(10) == 27:
				isclosed = 1 
				break 
		else:
			break
	if isclosed:
		break






#makes sure that python doesnt run in the background after you press escape
mask_read.release()
video_read.release()
cv2.destroyAllWindows()