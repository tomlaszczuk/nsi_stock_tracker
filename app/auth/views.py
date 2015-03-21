from flask import render_template, redirect, url_for, request, flash
from flask.ext.login import login_required, login_user, logout_user
from . import auth
from .forms import LoginForm
from ..models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Witaj, %s' % user.username, 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Błędny adres email lub hasło', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('Wylogowano', 'info')
	return redirect(url_for('auth.login'))