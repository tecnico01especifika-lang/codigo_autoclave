# autoclave/ui/services/backend_client.py

import json
from os import path
import requests

class BackendClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip("/")

    def get_status(self):
        r = requests.get(f"{self.base_url}/status", timeout=1.5)
        r.raise_for_status()
        return r.json()

    def post(self, path, json):
        r = requests.post(f"{self.base_url}{path}", json=json, timeout=1.5)
        r.raise_for_status()
        return r.json()