from flask import Flask, make_response, request, render_template
import dotenv
import os
import secrets
from flask_mail import Mail, Message
from models import db, User
import json

dotenv.load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL")
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

app.secret_key = secrets.token_urlsafe(16)
mail = Mail(app)
db.init_app(app)

@app.route("/")
def healthcheck():
    return make_response("OK", 200)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = json.loads(request.get_json())
    if data['is_fake'] == False:
        print(data)
        emails = list(map(lambda row: row[0], User.query.with_entities(User.email).all()))
        post_url = data['post_url']

        msg = Message(
            subject="New post!",
            recipients=emails
        )
        msg.html = render_template('email.html', post_url=post_url)
        try:
            mail.send(msg)
        except Exception as e:
            print(e)
            return make_response("NOT OK", 500) 
    return make_response("OK", 200) 

if __name__ == '__main__':
    app.run(
        host=os.getenv("APP_HOST"), 
        port=os.getenv("SENDER_PORT"), 
        debug=True
    )