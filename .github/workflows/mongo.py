from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import os


class UserAccess:

    def __init__(self):
        self.cluster = os.environ.get("MONGO_URL")
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
        if self.is_user(email):
            message = "This email is already registered for a user."
            return False, message
        else:
            self.records.insert_one(new_user)
            message = f"User {name} is now registered."
            return True, message

    def is_user(self, email_address):
        answer = None
        results = self.records.find({})
        for users in results:
            if users["users"]["email"] == email_address:
                return True
            else:
                answer = False
        return answer

    def search(self, email_address):
        results = self.records.find({})
        for users in results:
            if users["users"]["email"] == email_address:
                return users["_id"]

    def check_password(self, email, password):
        answer = None
        results = self.records.find({})
        for users in results:
            if users["users"]["email"] == email and check_password_hash(pwhash=users["users"]["password"],
                                                                        password=password):
                answer = True
                return answer
            else:
                answer = False
        return answer

    def load_user(self, email_address):
        if self.is_user(email_address):
            return self.search(email_address)

    def update(self, email_address, new_password):
        answer = None
        message = None
        results = self.records.find({})
        for users in results:
            if users["users"]["email"] == email_address:
                password = generate_password_hash(password=new_password, method='pbkdf2:sha256', salt_length=6)
                self.records.update_one({'_id': users["_id"]}, {'$set': {"password": password}})
                answer = True
                message = "Update was a success."
            else:
                answer = False
                message = "Update Failed"
        return answer, message


