
def test_upload_video_with_no_token(client):
    response = client.post('/video', follow_redirects=True)
    assert response.status_code == 403


def test_upload_video_with_valid_token(client):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTg5MDg3MDQyfQ.6g8IcVXhfJ7nSIWSodqhC-wbNnoWkEW3MEY4pdrbpMg"
    headers = {
        'Authorization': '{}'.format(token)
    }
    response = client.post('/video', headers=headers, data={"title": "VIDEO1"}, follow_redirects=True)
    assert response.status_code == 201

