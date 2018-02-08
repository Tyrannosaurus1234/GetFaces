import face_recognition
import numpy as np
import cv2
import random
import string
import os
import math
import argparse

#targfname = input("Target image filename: ")
#vidfname = input("Input video filename: ")
#tol = input("Target recognition tolerance (lower is more accurate but may miss faces, 0.1-1.0): ")
parser = argparse.ArgumentParser();
parser.add_argument('-i', type=str, help='Image of target face to scan for.', required=True)
parser.add_argument('-v', type=str, help='Video to process', required=True)
parser.add_argument('-t', type=float, help='Tolerance of face detection, lower is stricter. (0.1-1.0)', default=0.6)
parser.add_argument('-f', type=int, help='Amount of frames per second to extract.', default=1)
args = vars(parser.parse_args())

if args['t'] > 1.0:
	args['t'] = 1.0
elif args['t'] < 0.1:
	args['t'] = 0.1

targfname = args['i']
vidfname = args['v']
tol = args['t']
xfps = args['f']

print("target name: " + targfname)
print("video filename: " + vidfname)
print("tolerance: " + str(tol))

print("OpenCL: " + str(cv2.ocl.haveOpenCL()))
if(cv2.ocl.haveOpenCL()):
	print("Attempting to use OpenCL...")
	cv2.ocl.setUseOpenCL(True)
	print("Using OpenCL: " + str(cv2.ocl.useOpenCL()))

target_image = face_recognition.load_image_file(targfname)

#check if output directory already exists, and if not, create it
os.makedirs(str(str(os.path.splitext(targfname)[0]) + "_output"), exist_ok=True)

try:
	target_encoding = face_recognition.face_encodings(target_image)[0]
except IndexError:
	print("No face found in target image.")
	raise SystemExit(0)

input_video = cv2.VideoCapture(vidfname)

framenum = 0
facefound = False
vidheight = input_video.get(4)
vidwidth = input_video.get(3)
vidfps = input_video.get(cv2.CAP_PROP_FPS)

if xfps > vidfps:
	xfps = vidfps

totalframes = input_video.get(cv2.CAP_PROP_FRAME_COUNT)
outputsize = 256, 256
print("width: " + str(vidwidth) + ", height: " + str(vidheight) + ".")

known_faces = [
	target_encoding
]

def random_string(length):
	return ''.join(random.choice(string.ascii_letters) for m in range(length))

#switch to output directory
os.chdir(str(os.path.splitext(targfname)[0]) + "_output")

while(input_video.isOpened()):
	input_video.set(1, (framenum + (vidfps/xfps)))
	framenum += vidfps/xfps
	ret, frame = input_video.read()

	if not ret:
		break

	percentage = (framenum/totalframes)*100
	print("Checking frame " + str(int(framenum)) + str(" (%.2f%%)" % percentage))
	
	rgb_frame = frame[:, :, ::-1]
	
	face_locations = face_recognition.face_locations(rgb_frame)
	face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
	
	for fenc, floc in zip(face_encodings, face_locations):
		istarget = face_recognition.compare_faces(known_faces, fenc, tolerance=float(tol))
	
    	#if the face found matches the target
		if istarget[0]:
			top, right, bottom, left = floc
			facefound = True
			#squaring it up
			if (bottom - top) > (right - left):
				right = left + (bottom - top)
			elif (right - left) > (bottom - top):
				bottom = top + (right - left)
			#calculating the diagonal of the cropped face for rotation purposes
			#diagonal = math.sqrt(2*(bottom - top))
			#padding = diagonal / 2
			#alignment script causes images cropped "too closely" to get a bit fucky, so crop them less severely.
			padding = (bottom - top)/2
			
			if((top - padding >= 0) and (bottom + padding <= vidheight) and (left - padding >= 0) and (right + padding <= vidwidth)):
				croppedframe = frame[int(top - padding):int(bottom + padding), int(left - padding):int(right + padding)]
				#if the image is too small, resize it to outputsize
				cheight, cwidth, cchannels = croppedframe.shape
				if (cheight < 256) or (cwidth < 256):
					croppedframe = cv2.resize(croppedframe, outputsize, interpolation=cv2.INTER_CUBIC)
				print("writing image")
				cv2.imwrite(("0" + random_string(15) + ".jpg"), croppedframe, [int(cv2.IMWRITE_JPEG_QUALITY), 98])
input_video.release()
