from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():
    endpoints_description = """
    API Endpoints

    GET /forums
        Description: Retrieve a list of all forums.
        Response: JSON object containing the IDs and titles of all forums.
        Status Codes:
            200: Success.
            500: Internal Server Error.

    GET /join_forms
        Description: Retrieve a list of forums joined by the current user.
        Response: JSON object containing the IDs and titles of forums joined by the user.
        Status Codes:
            200: Success.
            500: Internal Server Error.

    GET /forums/<string:forum_id>/messages
        Description: Retrieve messages from a specific forum.
        Parameters: forum_id (string): The ID of the forum.
        Response: JSON object containing messages and users of the forum.
        Status Codes:
            200: Success.
            404: Forum not found.
            500: Internal Server Error.

    POST /forums/<string:forum_id>/users
        Description: Add a new user to the forum.
        Parameters:
            forum_id (string): The ID of the forum.
            title (string): The title of the forum.
        Response: JSON object confirming the addition of the user to the forum.
        Status Codes:
            201: Success.
            500: Internal Server Error.

    POST /forums/<string:forum_id>/messages
        Description: Post a message to a specific forum.
        Parameters:
            text (string): Text for message in the form.
            picture (string/none): Picture url for message in the form.
        Response: JSON object containing the posted message.
        Status Codes:
            201: Success.
            404: Forum not found.
            500: Internal Server Error.

    POST /forums
        Description: Create a new forum.
        Response: JSON object confirming the creation of the forum.
        Status Codes:
            201: Success.
            400: Forum ID and title must be provided.
            409: Forum already exists.
            500: Internal Server Error.
    """
    return endpoints_description, 200, {'Content-Type': 'text/plain'}
