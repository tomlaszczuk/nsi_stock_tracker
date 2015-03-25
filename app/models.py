from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask.ext.login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable property of user')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_password_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def confirm_password_reset_token(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id, 'new_email': new_email})

    def confirm_email_change_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('id') != self.id:
            return False
        new_email = data.get('new_email')
        if not new_email:
            return False
        if User.query.filter_by(email=new_email).first():
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):
        return "<User: %s>" % self.email


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
