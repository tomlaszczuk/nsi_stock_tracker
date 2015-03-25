from flask.ext.login import current_user
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


class ChangePasswordForm(Form):
    old_password = PasswordField('Stare hasło', validators=[DataRequired()])
    new_password = PasswordField('Nowe hasło', validators=[
        DataRequired(), EqualTo('confirm_password',
                                message='Hasła muszą być takie same.')
    ])
    confirm_password = PasswordField('Potwierdź nowe hasło',
                                     validators=[DataRequired()])
    submit = SubmitField('Zmień')

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Błędne hasło.')

    def validate_new_password(self, field):
        if current_user.verify_password(field.data):
            raise ValidationError('Nowe hasło powinno być inne niż stare')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(),
                                             Length(1, 128)])
    submit = SubmitField('Potwierdź')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Brak konta powiązanego z podanym adresem')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(),
                                             Length(1, 128)])
    new_password = PasswordField('Nowe hasło', validators=[
        DataRequired(), EqualTo('confirm_password',
                                message='Hasła muszą być takie same')
    ])
    confirm_password = PasswordField('Potwierdź nowe hasło',
                                     validators=[DataRequired()])
    submit = SubmitField('Zmień hasło')
