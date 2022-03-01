from http import client
from rest_framework.test import APIClient
from rest_framework import status 

class TestGetBloggerList:
    def test_if_blogger_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.get('/blogapp/bloggers/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        
