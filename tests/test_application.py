import json
import pytest
import boto3
from src.application import application

@pytest.fixture
def client():
    return application.test_client()

def test_request_example(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b"This is our content for the Home Page" in response.data

