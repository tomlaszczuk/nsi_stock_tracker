from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class LoginForm(Form):
	email = StringField('Email', validators=[DataRequired(), Length(1, 128),
											 Email()])
	password = PasswordField('Hasło', validators=[DataRequired()])
	remember_me = BooleanField('Pamiętaj mnie')
	submit = SubmitField('Zaloguj')