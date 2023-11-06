from flask import Flask, request, jsonify
from utils import commit_to_db, error_response, get_model_by_id
from models import db, User, Like, Post
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///puppies.db'
db.init_app(app)

def create_tables():
    with app.app_context():
        db.create_all()

# Endpoint to create a user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return error_response("Name and email are required", 400)

    user = User(name=name, email=email)
    commit_to_db(user)

    return jsonify({"user_id": user.id, "name": user.name, "email": user.email}), 201

# Endpoint to authenticate a user
@app.route('/users/login', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    email = data.get('email')
    user = User.query.filter_by(email=email).first()

    if not user:
        return error_response("User not found", 404)

    return jsonify({"user_id": user.id, "name": user.name, "email": user.email, "access_token": "your_access_token"})

# Endpoint to create a post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    user_id = data.get('user_id')
    image_url = data.get('image_url')
    text_content = data.get('text_content')
    date = datetime.now()
    user = get_model_by_id(User, user_id)

    if not user:
        return error_response("User not found", 404)

    post = Post(user=user, image_url=image_url, text_content=text_content, date=date)
    commit_to_db(post)

    return jsonify({"post_id": post.id, "user_id": post.user.id, "image_url": post.image_url, "text_content": post.text_content, "date": post.date}), 201

# Endpoint to like a post
@app.route('/posts/<int:post_id>/like', methods=['POST'])
def like_post(post_id):
    data = request.get_json()
    user_id = data.get('user_id')
    post = get_model_by_id(Post, post_id)
    user = get_model_by_id(User, user_id)

    if post is None or user is None:
        return error_response("Post or user not found", 404)

    like = Like.query.filter_by(user=user, post=post).first()
    if like:
        return jsonify({"message": "Post already liked"}), 200

    like = Like(user=user, post=post)
    commit_to_db(like)

    return jsonify({"message": "Post liked successfully"})

# Endpoint to fetch a user's feed
@app.route('/users/<int:user_id>/feed', methods=['GET'])
def fetch_user_feed(user_id):
    user = get_model_by_id(User, user_id)

    if not user:
        return error_response("User not found", 404)

    user_posts = Post.query.filter_by(user=user).order_by(Post.date.desc()).all()
    feed = [{"post_id": post.id, "image_url": post.image_url, "text_content": post.text_content, "date": post.date} for post in user_posts]

    return jsonify(feed)

# Endpoint to fetch details of an individual post
@app.route('/posts/<int:post_id>', methods=['GET'])
def fetch_post_details(post_id):
    post = get_model_by_id(Post, post_id)

    if not post:
        return error_response("Post not found", 404)

    return jsonify({"post_id": post.id, "user_id": post.user.id, "image_url": post.image_url, "text_content": post.text_content, "date": post.date})

# Endpoint to fetch a user's profile
@app.route('/users/<int:user_id>/profile', methods=['GET'])
def fetch_user_profile(user_id):
    user = get_model_by_id(User, user_id)

    if not user:
        return error_response("User not found", 404)

    return jsonify({"user_id": user.id, "name": user.name, "email": user.email})

# Endpoint to fetch a list of the user's liked posts
@app.route('/users/<int:user_id>/liked-posts', methods=['GET'])
def fetch_user_liked_posts(user_id):
    user = get_model_by_id(User, user_id)

    if not user:
        return error_response("User not found", 404)

    liked_posts = [like.post for like in user.likes]
    liked_posts_data = [{"post_id": post.id, "image_url": post.image_url, "text_content": post.text_content, "date": post.date} for post in liked_posts]

    return jsonify(liked_posts_data)

# Endpoint to fetch a list of posts the user made
@app.route('/users/<int:user_id>/posts', methods=['GET'])
def fetch_user_posts(user_id):
    user = get_model_by_id(User, user_id)

    if not user:
        return error_response("User not found", 404)

    user_posts = [post for post in user.posts]
    user_posts_data = [{"post_id": post.id, "image_url": post.image_url, "text_content": post.text_content, "date": post.date} for post in user_posts]

    return jsonify(user_posts_data)


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)