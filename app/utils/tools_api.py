from functools import wraps
from constants import USER_ID, USER_NAME, USER_PHOTO
from flask import request, jsonify, current_app
import json
import os


def ensure_data_file(func):
    """
    Ensure that the data file exists before executing the decorated function.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(current_app.config['DATA_FILE']):
            return jsonify({'error': 'Data file not found'}), 500
        return func(*args, **kwargs)
    return wrapper


def read_write_data(func):
    """
    Read data from the file, execute the decorated function, and then write the updated data back to the file.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.
    """
    @wraps(func)
    @ensure_data_file
    def wrapper(*args, **kwargs):
        with open(current_app.config['DATA_FILE'], 'r') as file:
            data = json.load(file)
        result = func(data, *args, **kwargs)
        with open(current_app.config['DATA_FILE'], 'w') as file:
            json.dump(data, file, indent=4)
        return result
    return wrapper


def add_user_to_forum(func):
    """
    Add a default user to the forum if the user is not already present.

    Args:
        func (function): The function to be decorated.

    Returns:
        function: The wrapped function.
    """
    @wraps(func)
    @read_write_data
    def wrapper(data, forum_id, *args, **kwargs):
        forum = data['forums'].get(forum_id)
        if not forum:
            return jsonify({'error': 'Forum not found'}), 404

        users = forum.get('users', [])
        if not any(user['user_id'] == USER_ID for user in users):
            users.append({
                'user_id': USER_ID,
                'user_name': USER_NAME,
                'user_photo': USER_PHOTO
            })
            forum['users'] = users

        return func(data, forum_id, *args, **kwargs)
    return wrapper
