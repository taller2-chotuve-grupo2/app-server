import requests

auth_base_url = "https://chotuve-grupo2-auth-server-dev.herokuapp.com"
login_endpoint = f"{auth_base_url}/login/"
register_endpoint = f"{auth_base_url}/user/"


def login_user(username, password):
    response = requests.post(login_endpoint,headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'},
     json={"username":username,"password":password})
    return response

def register_user(username, password, email):
    response = requests.post(register_endpoint, headers={'authorization': 'Basic YWxhZGRpbjpvcGVuc2VzYW1l'},
     json={"username":username,"password":password, "email":email})
    return response