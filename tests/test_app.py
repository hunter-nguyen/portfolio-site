# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

import sys
# Add the parent directory to the Python path to find the app module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, TimelinePost

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        # Clear any existing data before each test
        TimelinePost.delete().execute()

    def tearDown(self):
        # Clean up after each test
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        
    def test_home_content(self):
        response = self.client.get("/")
        html = response.get_data(as_text=True)
        assert "MLH Fellow" in html
        assert "html" in html.lower()
        assert "body" in html.lower()

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "timeline" in html.lower()

    def test_timeline_api_empty(self):
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

    def test_timeline_post_create(self):
        post_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'content': 'test'
        }
        response = self.client.post("/api/timeline_post", data=post_data)
        assert response.status_code == 200
        assert response.is_json
        
        json = response.get_json()
        assert json['name'] == 'John Doe'
        assert json['email'] == 'john@example.com'
        assert json['content'] == 'test'

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data=
            {"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data=
            {"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
            {"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html