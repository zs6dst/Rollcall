# *Rollcall* website

## Background
*Rollcall* is an attendance application for a club. *Rollcall* recognises a member from a photo captured with the camera and records the member's attendance at the meeting.

## Overview
The *Rollcall* website is a single page application that interacts with the *Rollcall* backend API.

## Technology used
- HTML with Bootstrap for layout and styling
- JavaScript to manipulate the HTML DOM and communicate with the *Rollcall* backend web API

## Approach taken
The main function of the website is to capture a photo of the member and submit it to the backend for processing. The website must react to the response from the backend to present appropriate messages and input elements to the user. Since the frontend functionality is rather simple, the web app is a single page application controlled by JavaScript.

## Improvements
Since the purpose of *Rollcall* is to identify a person from a photo, the live image presented to the user may be enhanced with a frame around the face to indicate that a face is detected in the image before submission to the backend.