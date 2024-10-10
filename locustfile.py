import time
from locust import HttpUser, task, between
from faker import Faker
import json
import requests
import utils

class QuickstartUser(HttpUser):
    fake = Faker()

    @task
    def send_fake(self):
        url = self.fake.url()
        json_data = json.dumps({
            'post_url': url,
            'is_fake': False
        })
        self.client.post('/send_email', json=json_data)