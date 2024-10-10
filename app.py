from flask import Flask, redirect, url_for, render_template
from forms import PostForm
from models import Post, db
import dotenv
import os
from bootstrap import bootstrap_data
import secrets
from flask_bootstrap import Bootstrap5
from flask_wtf import CSRFProtect
import json
import requests

from utils import get_notifier_url

dotenv.load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.secret_key = secrets.token_urlsafe(16)
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    bootstrap_data(app, db)


def notify_users(post_id: int):
    post_link = url_for('post_page', post_id=post_id)
    host = os.getenv("APP_HOST")
    app_port = os.getenv("APP_PORT")
    post_url = f"http://{host}:{app_port}{post_link}"
    json_data = json.dumps({
        'post_url': post_url,
        'is_fake': False,
    })
    sender_url = get_notifier_url()
    resp = requests.post(
        url=sender_url,
        json=json_data
    )
    print(resp.status_code)


@app.get("/")
def index_page():
    return render_template('index.html')

@app.get('/post/<post_id>')
def post_page(post_id: int):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/create_post', methods=['GET', 'POST'])
def create_post_page():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            text=form.text.data,
            user_id=1
        )
        session = db.session
        session.add(post)
        session.commit()
        session.flush()
        session.refresh(post)
        post_id = post.id
        notify_users(post_id)
        return redirect(url_for('post_page', post_id=post_id) )
    return render_template('create_post.html', form=form)

if __name__ == '__main__':
    app.run(
        host=os.getenv("APP_HOST"), 
        port=os.getenv("APP_PORT"), 
        debug=True
    )