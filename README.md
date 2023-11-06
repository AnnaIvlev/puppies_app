# Puppies API

The Puppies API is a web-based application that allows users to share pictures of their dogs in a style similar to Instagram. It provides various endpoints for user management, post creation, post interactions, and profile retrieval. The API is implemented using Python and Flask, with data stored in a SQLite database.

## Table of Contents

- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Endpoints](#endpoints)
- [Database Structure](#database-structure)
- [Testing](#testing)

## Getting Started

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/your-username/puppies-api.git
    ```
2. Change to the project directory:
    ```bash
    cd Puppies_app
    ```
3. Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
5. Install project dependencies:
    ```bash
   pip install -r requirements.txt
   ```
6. Run the application:
     ```bash
   python app.py
   ```

## Usage
### Endpoints
The Puppies API provides the following endpoints:

- POST /users: Create a new user by providing a name and email.
- POST /users/login: Authenticate a user by providing their email.
- POST /posts: Create a new post with an image, text content, and date.
- POST /posts/<post_id>/like: Like a post by providing the post ID and user ID.
- GET /users/<user_id>/feed: Retrieve a user's feed, a list of posts ordered by date.
- GET /posts/<post_id>: Retrieve details of an individual post.
- GET /users/<user_id>/profile: Retrieve a user's profile.
- GET /users/<user_id>/liked-posts: Retrieve a list of posts the user has liked.
- GET /users/<user_id>/posts: Retrieve a list of posts the user has made.

### Database Structure
The API uses a SQLite database for data storage, with the following tables:

- User: Stores user information, including name and email.
- Post: Stores post information, including the user ID, image URL, text content, and date.
- Like: Stores information about likes on posts, associating users and posts.




