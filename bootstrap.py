from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

from models import User

USER_NUM = 10

def bootstrap_data(app: Flask, db: SQLAlchemy):
    fake = Faker()
    domain = "adambra.com"

    usernames = set([fake.user_name() for _ in range(USER_NUM)])
    emails = [f"{username}@{domain}" for username in usernames]
    # usernames = ["Lamarr"]
    # emails = ["e_vodubrovec@kpfu.ru"]

    users = [User(username=username, email=email) for (username, email) in zip(usernames, emails)]

    session = db.session
    session.add_all(users)
    session.commit()
