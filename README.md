# GetFaces
Python script for extracting faces from video files


## Usage
`python getfaces.py -i TARGET_IMG -v INPUT_VIDEO -t TOLERANCE -f FPS -c CROP`

**TARGET_IMG**

An image (photo or screenshot from video) of the face you're scanning for, *e.g. nickcage.png*

**INPUT_VIDEO**

The video to be scanned *e.g. interview.mkv*

**TOLERANCE**

A value from 0.1 to 1.0 that represents the tolerance of the face detector, lower values make it more strict. If omitted will default to 0.6.

**FPS**

Amount of frames to scan and potentially extract per second of footage. If omitted will default to 1.

**CROP**

Whether to crop exported frames around the target's face. If omitted will default to true, if false will export full, uncropped frames.

## Dependencies
numpy

face_recognition

opencv-python >= 3.31
