import requests

register_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/user/"


def register_user(username, password, email):
    response = requests.post(register_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'},
     json={"username":username,"password":password, "email":email})
    return response