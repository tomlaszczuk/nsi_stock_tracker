from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(Form):
    username = StringField(
        'Login', validators=[
            DataRequired(), Length(1, 128),
            Regexp('^[A-Za-z][A-Za-z0-9_-]*$', 0,
                   message='Login musi się zaczynać literą i może'
                   'zawierać jedynie litery, cyfry lub znaki -._')
        ]
    )
    password = PasswordField('Hasło', validators=[DataRequired()])
    remember_me = BooleanField('Pamiętaj mnie')
    submit = SubmitField('Zaloguj')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 128),
                                             Email()])
    username = StringField(
        'Login',
        validators=[DataRequired(), Length(1, 128),
                    Regexp('^[A-Za-z][A-Za-z0-9_-]*$', 0,
                           message='Login musi się zaczynać literą i może'
                           'zawierać jedynie litery, cyfry lub znaki -._')]
    )
    password = PasswordField('Hasło', validators=[
        DataRequired(), EqualTo('password2',
                                message='Hasła muszą być takie same')])
    password2 = PasswordField('Powtórz hasło', validators=[DataRequired()])
    submit = SubmitField('Zarejestruj')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(
                'Ten adres email jest już przypisany do inengo konta'
            )

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Ten login jest już przypisany do inengo konta'
            )
