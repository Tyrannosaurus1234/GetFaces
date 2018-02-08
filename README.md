# GetFaces
***
Python script for extracting faces from video files


## Usage
***
`python getfaces.py -i TARGET_IMG -v INPUT_VIDEO -t TOLERANCE`

**TARGET_IMG**

An image (photo or screenshot from video) of the face you're scanning for, *e.g. nickcage.png*

**INPUT_VIDEO**

The video to be scanned *e.g. interview.mkv*

**TOLERANCE**

A value from 0.1 to 1.0 that represents the tolerance of the face detector, lower values make it more strict. A default value of 0.6 is recommended.

## Dependencies
***
numpy

face_recognition

opencv-python
