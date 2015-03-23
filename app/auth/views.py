from flask import (render_template, redirect, url_for,
                   request, flash, current_app)
from flask.ext.login import (login_required, login_user, logout_user)
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from ..decorators import admin_required
from ..emails import send_mail
from .. import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Witaj, %s' % user.username, 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Błędny login lub hasło', 'danger')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Wylogowano', 'info')
    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(username=form.username.data,
                 email=form.email.data,
                 password=form.password.data)
        db.session.add(u)
        db.session.commit()

        send_mail(to=current_app._get_current_object().config['ADMIN_EMAIL'],
                  subject='Nowy użytkownik się zarejestrował',
                  template='email/new_user',
                  username=u.username)

        flash('Konto zostało zarejestrowane. Zostaniesz powiadomiony/a o '
              'potwierdzeniu przez administratora wiadomością malową',
              'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/unconfirmed')
@login_required
@admin_required
def unconfirmed_users_list():
    unconfirmed = User.query.filter_by(confirmed=False).all()
    return render_template('auth/unconfirmed.html', unconfirmed=unconfirmed)


@auth.route('/confirm/<int:id>')
@login_required
@admin_required
def confirm(id):
    user = User.query.get_or_404(id)
    user.confirmed = True
    db.session.add(user)
    flash('Użytkownik został zatwierdzony', 'success')
    send_mail(to=user.email, subject='Konto zatwiedzone',
              template='email/confirm')
    return redirect(url_for('auth.unconfirmed_users_list'))
