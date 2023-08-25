import time

import google.auth.crypt
import google.auth.jwt

import requests
import os

base_path = os.path.dirname(__file__)
SERVICE_ACCOUNT_FILE = os.path.join(base_path, 'creds.json')#Mention the path to service account json file

def generate_jwt(
    sa_keyfile,
    sa_email="service account mail here",
    audience="https://oauth2.googleapis.com/token",
    expiry_length=3600,#Max expiry of 1 hour
):
    now = int(time.time())
    payload = {
        "scope":'gcloud scope here',
        "iat": now,
        "exp": now + expiry_length,
        "iss": sa_email,
        "aud": audience,
        "sub": sa_email,
        "email": sa_email,
    }
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)
    return jwt
def make_jwt_request(signed_jwt, url="https://oauth2.googleapis.com/token"):
    response = requests.post(url,data={"grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer","assertion":signed_jwt.decode("utf-8")})
    print(response.json()['access_token'])
    #Use the generated token as bearer in auth header
    #"Authorization", "Bearer {token}"
make_jwt_request(generate_jwt(SERVICE_ACCOUNT_FILE))