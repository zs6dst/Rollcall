# *Rollcall* web API (Python)

## Background
*Rollcall* is an attendance application for a club. *Rollcall* recognises a member from a photo captured with the camera and records the member's attendance at the meeting.

## Overview
The *Rollcall* backend is a web API with appropriate methods to identify and register a member from a photo.

## Technology used
- Python with [Flask](https://flask.palletsprojects.com/en/2.1.x/) framework
- [OpenCV](https://opencv.org/) realtime computer vision library

## Approach taken
OpenCV is developed in C++, with bindings for Python. The objective of the Python backend was to develop a prototype API to test the feasibility of an attendance system at club meetings.

- When the services starts, it creates training data from all previously stored photos of members.
- The process starts with identifying a member from a photo. If a face is detected in the photo, the photo is stored with a unique ID.
- If a member is recognised from the photo, the photo ID is returned with the details of the member.
- The request to register a member is received, the photo ID and member ID must be included in the request. The photo is moved to the collection of photos for the specified member and the member's attendance is recorded.

## Improvements
Since the Python service was developed as a prototype, any operational problems will be addressed in a production system. Such a system will be developed in Go.
