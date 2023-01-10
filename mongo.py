from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os


class UserAccess:

    def __init__(self):
        self.cluster = os.environ.get("my_cluster_db2")
        self.client = MongoClient(self.cluster)
        self.db = self.client.law_user
        self.records = self.db.workers

    def register_user(self, name, email, password):
        hashed_and_salted_password = generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=6)

        new_user = {
            "users": {
                "username": name,
                "email": email,
                "password": hashed_and_salted_password
            }
        }
        self.records.insert_one(new_user)
        return f"User {name} is now registered."


user = UserAccess()
user.register_user(name="King Kunta", email="Kingkunta@gmail.com", password="zetzet")
