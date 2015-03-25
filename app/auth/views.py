from flask import (render_template, redirect, url_for,
                   request, flash, current_app)
from flask.ext.login import (login_required, login_user, logout_user,
                             current_user)
from . import auth
from .forms import (LoginForm, RegistrationForm, ChangePasswordForm,
                    PasswordResetRequestForm, PasswordResetForm,
                    EmailChangeRequestForm)
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

        send_mail(to=current_app.config['ADMIN_EMAIL'],
                  subject='Nowy użytkownik się zarejestrował',
                  template='email/new_user',
                  username=u.username)

        flash('Konto zostało zarejestrowane. Zostaniesz powiadomiony/a o '
              'potwierdzeniu przez administratora wiadomością mailową. '
              'Do momentu aktywacji konta korzystanie z aplikacji nie będzie '
              'możliwe',
              'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/admin/unconfirmed')
@login_required
@admin_required
def unconfirmed_users_list():
    unconfirmed = User.query.filter_by(confirmed=False).all()
    return render_template('auth/unconfirmed_users.html',
                           unconfirmed=unconfirmed)


@auth.route('/admin/confirm/<int:id>')
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


@auth.route('/admin/confirm_all')
@login_required
@admin_required
def confirm_all_users():
    unconfirmed = User.query.filter_by(confirmed=False).all()
    for user in unconfirmed:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        send_mail(to=user.email, subject='Konto zatwiedzone',
                  template='email/confirm')
    flash('Operacja zakończona powodzeniem', 'success')
    return redirect(url_for('auth.unconfirmed_users_list'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated() and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    admin = current_app.config['ADMIN_EMAIL']
    return render_template('auth/unconfirmed_message.html', admin=admin)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.new_password.data
        db.session.add(current_user)
        flash('Hasło zmienione.', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/change_password.html', form=form)


@auth.route('/password-reset-request', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.generate_password_reset_token()
        send_mail(to=form.email.data, subject='Reset hasła',
                  template='email/password_reset',
                  token=token, user=user)
        flash('Wiadomość z dalszymi instrukcjami została '
              'wysłana na podany adres', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset_request.html', form=form)


@auth.route('/password-reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.confirm_password_reset_token(token,
                                                      form.new_password.data):
            flash('Sukces. Możesz się zalogować używając nowego hasła',
                  'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Nieprawidłowy lub przeterminowany link', 'danger')
    return render_template('auth/reset_password.html', form=form)


@auth.route('/emial-change-request', methods=['GET', 'POST'])
@login_required
def email_change_request():
    form = EmailChangeRequestForm()
    if form.validate_on_submit():
        token = current_user.generate_email_change_token(form.new_email.data)
        send_mail(to=form.new_email.data, subject='Zmiana adresu email',
                  template='email/email_change', user=current_user,
                  token=token)
        flash('Wiadomość z dalszymi instrukcjami została '
              'wysłana na podany adres', 'info')
        return redirect(url_for('main.index'))
    return render_template('auth/email_change_request.html', form=form)


@auth.route('/email-change-confirm/<token>')
@login_required
def confirm_email_change(token):
    if current_user.confirm_email_change_token(token):
        flash('Twój email został poprawnie zmieniony.', 'success')
    else:
        flash("Nieprawidłowy lub przeterminowany link potwierdzający",
              "danger")
    return redirect(url_for('main.index'))
