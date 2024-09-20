# GAMELOFT FORM REST API

This project is a REST API for managing forums and performing various CRUD (create, read, update, delete) operations on them.

Main features:
Managing forums
Adding and retrieving forum posts
Adding and retrieving forum users
The project includes several tests to verify the functionality of the application, ensuring its reliability and correctness.

Launching a project
The project can be launched in the standard way via a file or using Docker to simplify deployment and dependency management.

Dependency management
The project uses poetry to manage dependencies. However, for those who prefer the classic approach, a standard requirements.txt file is also provided.


# Start a project using Poetry:

1. Make sure you have Poetry installed. If not, install it with the following command:

https://python-poetry.org/docs/

2. Activate the Poetry virtual environment: 

poetry shell

3. In .env file specify your SECRET_KEY for the configuration.

4. In the config.py file, specify the required JSON file.

5. In the constants.py file, specify your USER_ID, USER_NAME, and USER_PHOTO, as the client is already authorized according to the task requirements and there is no need to implement signup/login APIs.

6. Start the project:

/home/anton/.cache/pypoetry/virtualenvs/pythonproject-pflyVAO5-py3.10/bin/python /home/anton/flask_project/pythonProject/start.py

# Start a project using Docker Compose:

1. Install Docker and Docker Compose if they are not already installed.

https://docs.docker.com/compose/install/

2. Go to the root directory of the project (where locate docker-compose.yml).

3. Start the project using Docker Compose:

docker-compose up --build

Note: Before using Docker Compose, make sure you have Docker and Docker Compose installed on your system.


# Run tests:

Run the following command in a terminal to run the tests:

python -m unittest tests.test_api

Note: Make sure you are in the root directory of your project before running the tests.


# API Endpoints

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

GET /forums/string:forum_id/messages
Description: Retrieve messages from a specific forum.
    Parameters:
    forum_id (string): The ID of the forum.
    Response: JSON object containing messages and users of the forum.
    Status Codes:
        200: Success.
        404: Forum not found.
        500: Internal Server Error.

POST /forums/string:forum_id/users
    Description: Add a new user to the forum.
    Parameters:
        forum_id (string): The ID of the forum.
        title (string): The title of the forum.
    Response: JSON object confirming the addition of the user to the forum.
    Status Codes:
        201: Success.
        500: Internal Server Error.

POST /forums/string:forum_id/messages
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

# Using REST Client:

You can use any REST Client to send requests to your REST API. The following are sample requests for various operations that you can use in requests.http:

## Post a message to a specific forum:

POST http://127.0.0.1:5000/forums/id_forum/messages
Content-Type: application/json

{
    { “text”: “your_text”,
    “picture”: “your_url” or null
}

## Adding a new user to a specific forum:

POST http://127.0.0.1:5000/forums/id_forum/users
Content-Type: application/json

## Creating a new forum:

POST http://127.0.0.1:5000/forums
Content-Type: application/json

{
    “forum_id”: “forum_id”,
    { “title”: “your_title”
}

## Get a list of all forums:

GET http://127.0.0.1:5000/forums

## Get a list of forums joined by the current user:

GET http://127.0.0.1:5000/join_forms

## Get posts from a specific forum:

GET http://127.0.0.1:5000/forums/id_forum/messages