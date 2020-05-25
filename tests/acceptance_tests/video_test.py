from unittest.mock import Mock, patch

def test_upload_video_with_no_token(client):
    response = client.post('/video', follow_redirects=True)
    assert response.status_code == 403

@patch('app.media.upload_video')
def test_upload_video_with_valid_token(mock_post, client):
    mock_post.return_value.ok = True
    mock_post.return_value.status_code = 201
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {
        'Authorization': f"{token}"
    }
    data = dict(title="video1")
    response = client.post('/video', headers=headers, content_type="application/json", json=data, follow_redirects=True)
    assert response.status_code == 201
