import uuid
from locust import HttpUser, task, between
from faker import Faker

faker = Faker()

class AuthUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.name = faker.name()
        self.email = f"user_{uuid.uuid4().hex[:10]}@test.com"
        self.password = "TestPass123!"

        with self.client.post("/api/register", json={
            "username": self.name, 
            "email": self.email, 
            "password": self.password}, catch_response=True) as resp:
            if resp.status_code != 201:
                resp.failure(f"Registration failed with status {resp.status_code}")

    @task(5)
    def login(self):
        payload = {
            "email": self.email, 
            "password": self.password
        }
        
        with self.client.post("/api/auth/login", json=payload, catch_response=True) as resp:
            if resp.status_code != 202:
                resp.failure(f"Expected 202, got {resp.status_code}: {resp.text}")
