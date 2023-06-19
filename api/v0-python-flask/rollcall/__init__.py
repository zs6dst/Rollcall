from flask import Flask
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

MEMBERS = {} # id:member
ALTIDS  = {} # altId:id
FACES = [] # face encodings
LABELS = [] # face labels

from rollcall import helper, faces, routes

app.config['DATA'] = helper.setupDirs()
helper.getAllMembers()
faces.train()