from asyncio.log import logger
from flask import request, jsonify
from rollcall import app
import rollcall.api as api
import http


@app.route('/',    methods=['GET'])
@app.route('/api', methods=['GET'])
def welcome():
    return jsonify(message='Welcome to the Rollcall API'), http.HTTPStatus.OK


@app.route('/api/identify', methods=['POST'])
def identify():
    try:
        photo = request.get_json(force=True).get('photo')
        if not photo: return jsonify(message='No photo'), http.HTTPStatus.BAD_REQUEST

        member, photoId = api.identify(photo)
        if not photoId: return jsonify(message='Bad photo'), http.HTTPStatus.BAD_REQUEST

        status = http.HTTPStatus.OK if member else http.HTTPStatus.NO_CONTENT
        return jsonify(photoId=photoId, member=member), status
    except Exception as e:
        logger.info(e)
        return None, http.HTTPStatus.INTERNAL_SERVER_ERROR


@app.route('/api/register', methods=['POST'])
def register():
    req_data = request.get_json(force=True)
    photoId = req_data.get('photoId')
    if not photoId:
        return jsonify(message='photoId not provided'), http.HTTPStatus.BAD_REQUEST
    member = req_data.get('member')  # member is a dictionary
    if not member or (not member.get('id') and not member.get('altId')):
        return jsonify(message='member ID not provided'), http.HTTPStatus.BAD_REQUEST

    try:
        member, photoId, message = api.register(member, photoId)
        if photoId:
            status = http.HTTPStatus.CREATED if member else http.HTTPStatus.NO_CONTENT
        else:
            status = http.HTTPStatus.BAD_REQUEST
    except Exception:
        status = http.HTTPStatus.INTERNAL_SERVER_ERROR
        message = 'Failed to register member'

    return jsonify(member=member, photoId=photoId, message=message), status
