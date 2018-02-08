# GetFaces
***
Python script for extracting faces from video files


## Usage
***
1. Upon running the script, it will ask for a **target image**: point it to a photograph or screenshot from the video to be processed of the person you wish to extract

2. Next, it will ask for the **input video**: point it to the video to process

3. Finally, it will ask for a **tolerance** from 0.1 to 1.0, this is how close each face it detects must be to be considered the same person, a default value of 0.6 is recommended - if it's finding too many wrong faces, lower it by 0.1 and try again, and if it's not finding enough faces, do the same but raise it instead of lowering it.

## Dependencies
***
numpy
face_recognition
opencv-python
