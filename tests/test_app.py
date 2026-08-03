# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Amandaleeanne Schock</title>" in html
        # The nav bar is the same on every page, so if it links to all of
        # these here, visitors can reach the rest of the site from home.
        assert 'href="/experience"' in html
        assert 'href="/hobbies"' in html
        assert 'href="/travel"' in html
        assert 'href="/timeline"' in html
        assert 'href="/blog"' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        # Post a new entry the same way the timeline page's form does, and
        # make sure the server hands back the exact post it just saved.
        post_response = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": "Hello world, I'm John!",
        })
        assert post_response.status_code == 200
        assert post_response.is_json
        created = post_response.get_json()
        assert created["name"] == "John Doe"
        assert created["email"] == "john@example.com"
        assert created["content"] == "Hello world, I'm John!"

        # That new post should now show up when we list them again.
        response = self.client.get("/api/timeline_post")
        json = response.get_json()
        assert len(json["timeline_posts"]) == 1
        assert json["timeline_posts"][0]["name"] == "John Doe"

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
