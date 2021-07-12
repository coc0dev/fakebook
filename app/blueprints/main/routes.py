from flask import render_template, url_for, request, flash, redirect, current_app
from .import main as app
from flask_login import current_user, login_required
from app import db, mail
from flask_mail import Message, Mail
from app.blueprints.authentication.models import User
from app.blueprints.blog.models import Post
import boto3
import time

# posts = [
#         {
#             'id': 1,
#             'body': "This is the first blog post",
#             'author': "Somebody A. Someone",
#             'timestamp': "7-6-21"
#         },
#         {
#             'id': 2,
#             'body': "This is the second blog post",
#             'author': "Somebody B. Someone",
#             'timestamp': "7-5-21"
#         },
#         {
#             'id': 3,
#             'body': "This is the third blog post",
#             'author': "Somebody C. Someone",
#             'timestamp': "7-4-21"
#         }
#     ]

@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':

        post = Post(body=request.form.get('body_text'), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('You added a new post!', 'success')
        # return redirect(url_for('main.index'))
        
    context = {
        "posts": current_user.followed_posts()
    }
    return render_template("index.html", **context)

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        form_data = {
            'email': request.form.get('email'),
            'inquiry': request.form.get('inquiry'),
            'message': request.form.get('message')
        }

        msg = Message(
            'This is the subject line',
            sender="evanjcolondres@gmail.com",
            recipients=["mashersandgravy@me.com"],
            html=render_template('email/contact-results.html', **form_data)
            )
        mail.send(msg)
        flash('thanks you good', 'success')
        return redirect(url_for('main.contact'))
    return render_template("contact.html")

@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    # AWS and boto3 for when I have it set up
    # s3 = boto3.client('s3', 
    # aws_access_key_id=current_app.config.get('aws_access_key_id'), 
    # aws_secret_access_key=current_app.config.get('aws_secret_access_key')
    # )

    if request.method == 'POST':
        # request.files.get('profile-image').filename = str(int(time.time()))
        # content_type = request.files.get('profile-image').content_type
        

        u = User.query.get(current_user.id)
        u.first_name = request.form.get('first_name')
        u.last_name = request.form.get('last_name')
        u.email = request.form.get('email')
        u.bio = request.form.get('bio')
        # if len(request.files) > 0:
        #     s3.upload_fileobj(
        #         request.files.get('profile-image'),
        #         'bucket-name',
        #         filename,
        #         ExtraArgs={
        #             'ACL': 'public-read',
        #             'ContentType': content_type
        #         }
        #     )
            # u.image = f'{filename}.{content_type}'
        db.session.commit()
        flash("You updated your profile")
        return redirect(url_for('main.profile'))
    context = {
        "posts": current_user.my_posts()
    }
    return render_template('profile.html', **context)