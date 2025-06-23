from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_strong_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login manager setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Friendships association table
friendships = db.Table('friendships',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_friend_requests')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_friend_requests')

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    journals = db.relationship('Journal', backref='author', lazy=True)
    friends = db.relationship('User', 
                              secondary=friendships,
                              primaryjoin=(friendships.c.user_id == id),
                              secondaryjoin=(friendships.c.friend_id == id),
                              backref=db.backref('friend_of', lazy='dynamic'),
                              lazy='dynamic')

    def add_friend(self, user):
        if not self.is_friend(user):
            self.friends.append(user)
            user.friends.append(self)
            return self

    def remove_friend(self, user):
        if self.is_friend(user):
            self.friends.remove(user)
            user.friends.remove(self)
            return self

    def is_friend(self, user):
        return self.friends.filter(friendships.c.friend_id == user.id).count() > 0

# Journal model
class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    friends_journals = Journal.query.filter(Journal.user_id.in_([friend.id for friend in current_user.friends])).order_by(Journal.timestamp.desc()).all()
    pending_requests = current_user.received_friend_requests
    return render_template('dashboard.html', user=current_user, friends_journals=friends_journals, pending_requests=pending_requests)

@app.route('/friends')
@login_required
def friends():
    user_friends = current_user.friends.all()
    return render_template('friends.html', friends=user_friends)

@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@app.route('/add_journal', methods=['GET', 'POST'])
@login_required
def add_journal():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        new_journal = Journal(title=title, content=content, author=current_user)
        db.session.add(new_journal)
        db.session.commit()
        flash('Journal added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_journal.html')

@app.route('/send_friend_request', methods=['POST'])
@login_required
def send_friend_request():
    username = request.form.get('username')
    receiver = User.query.filter_by(username=username).first()

    if not receiver:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

    if receiver == current_user:
        flash("You cannot send a friend request to yourself.", 'warning')
        return redirect(url_for('dashboard'))

    if current_user.is_friend(receiver):
        flash('You are already friends with this user.', 'info')
        return redirect(url_for('dashboard'))

    existing_request = FriendRequest.query.filter(
        (FriendRequest.sender_id == current_user.id) & (FriendRequest.receiver_id == receiver.id)
    ).first()
    
    if existing_request:
        flash('You have already sent a friend request to this user.', 'info')
        return redirect(url_for('dashboard'))

    received_request = FriendRequest.query.filter(
        (FriendRequest.sender_id == receiver.id) & (FriendRequest.receiver_id == current_user.id)
    ).first()

    if received_request:
        flash(f'{receiver.username} has already sent you a friend request. Please accept or reject it.', 'info')
        return redirect(url_for('dashboard'))
    
    new_request = FriendRequest(sender=current_user, receiver=receiver)
    db.session.add(new_request)
    db.session.commit()
    
    flash(f'Friend request sent to {receiver.username}.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/accept_friend_request/<int:request_id>', methods=['POST'])
@login_required
def accept_friend_request(request_id):
    friend_request = FriendRequest.query.get_or_404(request_id)
    if friend_request.receiver_id != current_user.id:
        return redirect(url_for('dashboard'))

    sender = friend_request.sender
    current_user.add_friend(sender)
    db.session.delete(friend_request)
    db.session.commit()
    
    flash(f'You are now friends with {sender.username}.', 'success')
    return redirect(url_for('dashboard'))

@app.route('/reject_friend_request/<int:request_id>', methods=['POST'])
@login_required
def reject_friend_request(request_id):
    friend_request = FriendRequest.query.get_or_404(request_id)
    if friend_request.receiver_id != current_user.id:
        return redirect(url_for('dashboard'))
    
    sender = friend_request.sender
    db.session.delete(friend_request)
    db.session.commit()
    
    flash(f'You have rejected the friend request from {sender.username}.', 'info')
    return redirect(url_for('dashboard'))

@app.route('/remove_friend/<int:friend_id>', methods=['POST'])
@login_required
def remove_friend(friend_id):
    friend = User.query.get_or_404(friend_id)
    if not current_user.is_friend(friend):
        flash('You are not friends with this user.', 'warning')
        return redirect(url_for('friends'))
    
    current_user.remove_friend(friend)
    db.session.commit()
    flash(f'You are no longer friends with {friend.username}.', 'success')
    return redirect(url_for('friends'))

@app.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    username = request.form.get('username')
    friend = User.query.filter_by(username=username).first()

    if not friend:
        flash('User not found.', 'danger')
        return redirect(url_for('dashboard'))

    if friend == current_user:
        flash("You cannot add yourself as a friend.", 'warning')
        return redirect(url_for('dashboard'))

    if current_user.is_friend(friend):
        flash('You are already friends with this user.', 'info')
        return redirect(url_for('dashboard'))

    current_user.add_friend(friend)
    db.session.commit()
    flash(f'{friend.username} has been added to your friends.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True) 