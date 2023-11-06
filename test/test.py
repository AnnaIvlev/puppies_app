import unittest
import json
from app import app
from models import db

class TestAppEndpoints(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_puppies.db'
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def create_user(self, name, email):
        data = {
            'name': name,
            'email': email
        }
        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')
        return json.loads(response.data)

    def create_post(self, user_id, image_url, text_content):
        data = {
            'user_id': user_id,
            'image_url': image_url,
            'text_content': text_content
        }
        response = self.app.post('/posts', data=json.dumps(data), content_type='application/json')
        return json.loads(response.data)

    def like_post(self, user_id, post_id):
        data = {
            'user_id': user_id
        }
        response = self.app.post(f'/posts/{post_id}/like', data=json.dumps(data), content_type='application/json')
        return response

    def test_create_user(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')
        self.assertEqual(user_data['name'], 'John Doe')
        self.assertEqual(user_data['email'], 'johndoe@example.com')

    def test_create_user_missing_data(self):
        data = {
            'name': 'Alice'
        }
        response = self.app.post('/users', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_authenticate_user_success(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')

        auth_data = {
            'email': 'johndoe@example.com'
        }
        auth_response = self.app.post('/users/login', data=json.dumps(auth_data), content_type='application/json')
        user_info = json.loads(auth_response.data)
        self.assertEqual(user_info['name'], 'John Doe')
        self.assertEqual(user_info['email'], 'johndoe@example.com')

    def test_authenticate_user_not_found(self):
        auth_data = {
            'email': 'nonexistent@example.com'
        }
        auth_response = self.app.post('/users/login', data=json.dumps(auth_data), content_type='application/json')
        self.assertEqual(auth_response.status_code, 404)

    def test_fetch_user_feed_multiple_posts(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')
        user_id = user_data['user_id']

        post1 = self.create_post(user_id, 'image1.jpg', 'Post 1')
        post2 = self.create_post(user_id, 'image2.jpg', 'Post 2')
        post3 = self.create_post(user_id, 'image3.jpg', 'Post 3')
        feed_response = self.app.get(f'/users/{user_id}/feed')
        feed_data = json.loads(feed_response.data)

        self.assertEqual(len(feed_data), 3)
        self.assertEqual(feed_data[0]['post_id'], post3['post_id'])
        self.assertEqual(feed_data[1]['post_id'], post2['post_id'])
        self.assertEqual(feed_data[2]['post_id'], post1['post_id'])

    def test_fetch_user_feed_user_not_found(self):
        response = self.app.get('/users/999/feed')
        self.assertEqual(response.status_code, 404)

    def test_fetch_post_details(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')
        user_id = user_data['user_id']

        post_data = self.create_post(user_id, 'image1.jpg', 'Post 1')
        post_id = post_data['post_id']

        details_response = self.app.get(f'/posts/{post_id}')
        post_details = json.loads(details_response.data)
        self.assertEqual(post_details['post_id'], post_id)

    def test_fetch_post_details_post_not_found(self):
        response = self.app.get('/posts/999')
        self.assertEqual(response.status_code, 404)

    def test_fetch_user_profile(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')
        user_id = user_data['user_id']

        profile_response = self.app.get(f'/users/{user_id}/profile')
        profile_data = json.loads(profile_response.data)
        self.assertEqual(profile_data['user_id'], user_id)

    def test_fetch_user_profile_user_not_found(self):
        response = self.app.get('/users/999/profile')
        self.assertEqual(response.status_code, 404)

    def test_fetch_user_liked_posts(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')
        user_id = user_data['user_id']

        post_data = self.create_post(user_id, 'image1.jpg', 'Post 1')
        post_id = post_data['post_id']

        like_response = self.like_post(user_id, post_id)
        self.assertEqual(like_response.status_code, 200)

        liked_posts_response = self.app.get(f'/users/{user_id}/liked-posts')
        liked_posts_data = json.loads(liked_posts_response.data)
        self.assertEqual(len(liked_posts_data), 1)
        self.assertEqual(liked_posts_data[0]['post_id'], post_id)

    def test_fetch_user_liked_posts_user_not_found(self):
        response = self.app.get('/users/999/liked-posts')
        self.assertEqual(response.status_code, 404)

    def test_fetch_user_liked_posts_empty(self):
        user_data = self.create_user('Alice', 'alice@example.com')
        user_id = user_data['user_id']

        liked_posts_response = self.app.get(f'/users/{user_id}/liked-posts')
        liked_posts_data = json.loads(liked_posts_response.data)
        self.assertEqual(len(liked_posts_data), 0)

    def test_fetch_user_posts(self):
        user_data = self.create_user('John Doe', 'johndoe@example.com')
        user_id = user_data['user_id']

        post_data = self.create_post(user_id, 'image1.jpg', 'Post 1')
        post_id = post_data['post_id']

        user_posts_response = self.app.get(f'/users/{user_id}/posts')
        user_posts_data = json.loads(user_posts_response.data)
        self.assertEqual(len(user_posts_data), 1)
        self.assertEqual(user_posts_data[0]['post_id'], post_id)

    def test_fetch_user_posts_user_not_found(self):
        response = self.app.get('/users/999/posts')
        self.assertEqual(response.status_code, 404)

    def test_fetch_user_posts_empty(self):
        user_data = self.create_user('Alice', 'alice@example.com')
        user_id = user_data['user_id']
        user_posts_response = self.app.get(f'/users/{user_id}/posts')
        user_posts_data = json.loads(user_posts_response.data)
        self.assertEqual(len(user_posts_data), 0)
