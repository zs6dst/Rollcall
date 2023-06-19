from rollcall import app, MEMBERS, FACES, LABELS
import os
import cv2
import numpy as np
import logging
import uuid
import math
import base64
import glob
import shutil


def detect(base64photo):
    '''Detects a face in an image
    Input: Base64 encoded image
    Returns: unique photo ID
    '''
    # Convert base64 to grayscale image
    try:
        img_raw = base64.b64decode(base64photo)
        img_npy = np.frombuffer(img_raw, dtype=np.uint8)
        img = cv2.imdecode(img_npy, cv2.IMREAD_UNCHANGED)  # ??
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        photoId = str(uuid.uuid1())
        logging.info('Converted photo to grayscale image')
    except:
        logging.error('Failed to convert photo')
        return None

    #Detect face(s) in image
    try:
        faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
        logging.info(f'{len(faces)} face(s) detected')
        if len(faces) == 0: return None
    except:
        logging.error('Failed to detect face')
        return None

    try:
        photoId = str(uuid.uuid1())
        path = os.path.join(app.config['DATA'], 'faces', f'{photoId}.jpg')
        face = _getLargest(faces)
        cv2.imwrite(path, gray[face[1]:face[1]+face[3], face[0]:face[0]+face[2]])
        return photoId
    except:
        logging.error('Failed to write jpg')
        return None


def recognise(photoId):
    '''Identify the member from a photo
    Input: unique photo ID
    Output: the member identified from the photo
    '''
    path = os.path.join(app.config['DATA'], 'faces', f'{photoId}.jpg')
    if not os.path.isfile(path): return None
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.read(os.path.join(app.config['DATA'], 'training.yml'))
    result = model.predict(img)
    id = f'{int(result[0]):06}'
    global MEMBERS
    return MEMBERS.get(id)


def _getLargest(faces):
    '''Helper function to select the face with the largest diagonal from a list of faces
    Input: collection of faces
    Output: the face with the largest diameter
    '''
    if len(faces) == 0: return None
    if len(faces) == 1: return faces[0]

    sizeOf = lambda f: math.sqrt(f[2]**2 + f[3]**2)
    maxSize = 0
    bigFace = faces[0]
    for face in faces:
        size = sizeOf(face)
        if size > maxSize: maxSize, bigFace = size, face
    return bigFace


def train():
    faces = []
    labels = []
    facesDir = os.path.join(app.config['DATA'], 'faces')
    for member in os.listdir(facesDir):
        memberDir = os.path.join(facesDir, member)
        if not os.path.isdir(memberDir): continue
        _duplicateSinglePhoto(memberDir)
        for photo in os.listdir(memberDir):
            path = os.path.join(facesDir, member, photo)
            if not os.path.isfile(path): continue
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(int(member))
    if not faces: return
    
    # Create the training data
    global FACES, LABELS
    FACES = np.array(faces, dtype=object)
    LABELS = np.array(labels)
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(FACES, LABELS)
    model.save(os.path.join(app.config['DATA'], 'training.yml'))

def _duplicateSinglePhoto(path):
    '''Duplicates an existing photo when only 1 in the directory
       This is necessary since the recognizer needs at least 2
    '''
    photos = glob.glob(os.path.join(path, '*.jpg'))
    if len(photos) == 1: shutil.copy(photos[0], os.path.join(path, 'duplicate.jpg'))
