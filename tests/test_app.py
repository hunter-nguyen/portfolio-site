import unittest
import os

from werkzeug.wrappers import response
os.environ["TESTING"] = "true"

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '<meta property="og:title" content="Personal Portfolio">' in html
        
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None
        assert "timeline_posts" in json
        
    def test_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": "Hello, world!"})
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None
        assert "name" in json
        assert json["name"] == "John Doe"
    
    def test_get_timeline_post(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json is not None
        assert "timeline_posts" in json
        assert json["timeline_posts"][0]["name"] == "John Doe"
        
    def test_malformed_timeline_post(self):
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello, world!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid name' in html
        
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert 'Invalid content' in html
        
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello, world!"})
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'Invalid email' in html