import os
import time
import json

import requests


class Flutterwave:

    FLW_BASE_URL = "https://api.flutterwave.com/v3"

    def __init__(self, secret_key, public_key, env=None):

        self.secret_key = secret_key
        self.public_key = public_key
        self.env = env

        if self.env != None:
            self.secret_key = os.environ.get(secret_key, None)
            self.public_key = os.environ.get(public_key, None)

        self.headers = {
            'Authorization': f'Bearer {self.secret_key}',
            'Content-Type': 'application/json'}

    def standard(self, data):
        payload = json.dumps(data)

        try:
            response = requests.request(
                "POST", url=f"{self.FLW_BASE_URL}/payments", headers=self.headers, data=payload)

        except Exception as error:
            return error

        return response

    def verify(self, txRef):

        url = f'{self.FLW_BASE_URL}/transactions/{txRef}/verify'

        try:
            response = requests.request(
                "GET", url=url, headers=self.headers)
        except Exception as error:
            return error

        return response

    def show(self):
        return self.headers


flutterwave = Flutterwave('FLW_SECRET_KEY', 'FLW_PUBLIC_KEY', env=True)
