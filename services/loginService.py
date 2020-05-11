import requests

login_endpoint = "https://chotuve-grupo2-auth-server-dev.herokuapp.com/login/"


def login_user(username, password):
    response = requests.post(login_endpoint,headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'},
     json={"username":username,"password":password})
    return response