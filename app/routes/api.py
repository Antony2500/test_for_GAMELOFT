from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import json
from functools import wraps
from constants import USER_ID, USER_NAME, USER_PHOTO
from app.utils.tools_api import ensure_data_file, read_write_data, add_user_to_forum

api = Blueprint('api', __name__)


@api.route('/forums', methods=['GET'])
@ensure_data_file
def get_forums():
    """
    Retrieve a list of all forums.

    Returns:
        json: A JSON object containing the IDs and titles of all forums.
        status code: 200
    """
    with open(current_app.config['DATA_FILE'], 'r') as file:
        data = json.load(file)
    forums = data.get('forums', {})
    filtered_forums = {forum_id: {'title': forum_data['title']} for forum_id, forum_data in forums.items()}
    return jsonify(filtered_forums), 200


@api.route('/join_forms', methods=['GET'])
@ensure_data_file
def get_join_forms():
    """
    Retrieve a list of forums joined by the current user.

    Returns:
        json: A JSON object containing the IDs and titles of forums joined by the user.
        status code: 200
    """
    with open(current_app.config['DATA_FILE'], 'r') as file:
        data = json.load(file)
    
    user_join_forms = []

    for forum_id, forum_data in data['forums'].items():
        users = forum_data.get('users', [])
        for user in users:
            if user['user_id'] == USER_ID:
                user_join_forms.append({
                    'forum_id': forum_id,
                    'title': forum_data.get('title')
                })
                break 

    return jsonify(user_join_forms), 200


@api.route('/forums/<string:forum_id>/messages', methods=['GET'])
@ensure_data_file
def get_messages(forum_id):
    """
    Retrieve messages from a specific forum.

    Args:
        forum_id (str): The ID of the forum.

    Returns:
        json: A JSON object containing messages and users of the forum.
        status code: 200

    """
    with open(current_app.config['DATA_FILE'], 'r') as file:
        data = json.load(file)
    forum = data['forums'].get(forum_id)

    if not forum:
        return jsonify({'error': 'Forum not found'}), 404

    messages = forum.get('messages', [])
    sorted_messages = sorted(messages, key=lambda x: x['sending_time'])
    users = forum.get('users', [])
    filtered_users = [{'user_name': user['user_name'], 'user_photo': user['user_photo']} for user in users]
    
    return jsonify({'forum_messages': sorted_messages, 'users': filtered_users}), 200


@api.route('/forums/<string:forum_id>/users', methods=['POST'])
@add_user_to_forum
def add_user_to_forum_endpoint(data, forum_id):
    """
    Add a new user to the forum.

    Returns:
        json: A JSON object confirming the addition of the user to the forum.
        status code: 201

    """
    return jsonify({'message': 'User added to the forum successfully'}), 201


@api.route('/forums/<string:forum_id>/messages', methods=['POST'])
@add_user_to_forum
def post_message(data, forum_id):
    """
    Post a message to a specific forum.

    Args:
        forum_id (str): The ID of the forum.
        data (dict): The JSON data containing the message.

    Returns:
        json: A JSON object containing the posted message.
        status code: 201

    """
    forum = data['forums'].get(forum_id)

    if not forum:
        return jsonify({'error': 'Forum not found'}), 404

    if 'messages' not in forum:
        forum['messages'] = []

    message = {
        'sending_time': datetime.utcnow().isoformat(),
        'name_of_the_sender': USER_NAME,
        'text': request.json.get('text'),
        'picture': request.json.get('picture')
    }
    forum['messages'].append(message)
    return jsonify(message), 201


@api.route('/forums', methods=['POST'])
@read_write_data
def create_forum(data):
    """
    Create a new forum.

    Args:
        data (dict): The JSON data containing the forum information.

    Returns:
        json: A JSON object confirming the creation of the forum.
        status code: 201

    """
    request_data = request.json
    if not request_data or 'forum_id' not in request_data or 'title' not in request_data:
        return jsonify({'error': 'Forum ID and title must be provided'}), 400

    forum_id = request_data['forum_id']
    title = request_data['title']
    forums = data.get('forums', {})

    if forum_id in forums:
        return jsonify({'error': 'Forum already exists'}), 409

    NEW_USER_ID = USER_ID
    NEW_USER_NAME = USER_NAME
    NEW_USER_PHOTO = USER_PHOTO

    forums[forum_id] = {
        'title': title,
        'messages': [],
        'users': [{"user_id": NEW_USER_ID, "user_name": NEW_USER_NAME, "user_photo": NEW_USER_PHOTO}]
    }

    return jsonify({'message': 'Forum created successfully', 'forum_id': forum_id, 'title': title, 'users': [{"user_id": NEW_USER_ID, "user_name": NEW_USER_NAME, "user_photo": NEW_USER_PHOTO}]}), 201
