from locust import FastHttpUser, task, between
from faker import Faker

fake = Faker()

class SignupLoginUser(FastHttpUser):
    # Set a small wait time to control request rate pacing
    wait_time = between(0.05, 0.2)

    def on_start(self):
        # 1. Generate unique user details for this virtual user using Faker
        self.username = fake.user_name() + str(fake.random_int(min=1000, max=99999))
        self.email = f"{self.username}@test.com"
        self.password = "SecurePassword123"

        # 2. Register the user once upon spawning
        register_payload = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        
        # Hit your full signup route
        reg_response = self.client.post("/api/register", json=register_payload, name="/api/register")
        
        if reg_response.status_code not in [200, 201]:
            print(f"Registration failed for {self.email}: {reg_response.text}")

    @task(1)
    def test_login_endpoint(self):
        # 3. Repeatedly test login using the account created in on_start
        login_payload = {
            "email": self.email,     # Change to "username" if your backend expects username
            "password": self.password
        }
        
        with self.client.post("/api/auth/login", json=login_payload, name="/api/auth/login", catch_response=True) as response:
            if response.status_code in [200, 202, 302]:
                response.success()
            else:
                response.failure(f"Login failed with status: {response.status_code} - {response.text}")