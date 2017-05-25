# -*- coding: utf-8 -*-
from flask import (Blueprint, request, render_template, flash, url_for, send_from_directory, make_response,
                   redirect, current_app)

from flask_login import login_required, logout_user, current_user
from nostra.utils import flash_errors, render_extensions
from nostra.forms.user import PasswordForm, EmailForm, UsernameForm, CompanyForm
from nostra.extensions import mail
from nostra.models.user import User
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import urllib, json


blueprint = Blueprint("user", __name__, url_prefix='/users',
                      static_folder="../static")


@blueprint.route("/", methods=["GET", "POST"])
@login_required
def profile():
    form = CompanyForm()
    if form.validate_on_submit():

        urlIS = 'http://edgaronline.api.mashery.com/v1/corefinancials?primarysymbols='+str(form.ticker.data)+'&conceptgroups=IncomeStatementConsolidated&appkey=anapqb65c25p9pr9twjapaj3'
        urlBS = 'http://edgaronline.api.mashery.com/v1/corefinancials?primarysymbols='+str(form.ticker.data)+'&conceptgroups=BalanceSheetConsolidated&appkey=anapqb65c25p9pr9twjapaj3'
        urlCFS = 'http://edgaronline.api.mashery.com/v1/corefinancials?primarysymbols='+str(form.ticker.data)+'&conceptgroups=CashFlowStatementConsolidated&appkey=anapqb65c25p9pr9twjapaj3'

        #testurl = urlIS = 'http://edgaronline.api.mashery.com/v1/corefinancials?primarysymbols=MSFT&conceptgroups=IncomeStatementConsolidated&appkey=anapqb65c25p9pr9twjapaj3'
        response = urllib.urlopen(urlIS)
        dataIS = json.loads(response.read())
        response = urllib.urlopen(urlBS)
        dataBS = json.loads(response.read())
        response = urllib.urlopen(urlCFS)
        dataCFS = json.loads(response.read())

        print "DATA FOR INCOME STATEMENT"

        print "DATA FOR BALANCE SHEET"
        for x in range(0, 3):
            for y in range(0, 30):
                print dataBS['result']['rowset'][x]['groups'][0]['rowset'][y]['value']

        print "DATA FOR INCOME STATEMENT"
        for x in range(0, 3):
            for y in range(0, 24):
                print dataBS['result']['rowset'][x]['groups'][0]['rowset'][y]['value']

        print "DATA FOR CASH FLOW STATEMENT"
        for x in range(0, 3):
            for y in range(0, 38):
                print dataBS['result']['rowset'][x]['groups'][0]['rowset'][y]['value']

    else:
        flash_errors(form)
    return render_extensions("users/profile.html", companyform=form)

@blueprint.route('/reset', methods=["GET", "POST"])
def reset():
    form = EmailForm()
    if form.validate_on_submit():
        emailuser = User.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested"
        from nostra.settings import Config

        ts = URLSafeTimedSerializer(Config.SECRET_KEY)
        token = ts.dumps(emailuser.email, salt='recover-key')

        recover_url = url_for('user.reset_with_token', token=token, _external=True)
        html = render_template('email/recover.html', recover_url=recover_url)

        msg = Message(html=html, recipients=[emailuser.email], subject=subject)
        mail.send(msg)

        return redirect(url_for('public.home'))
    else:
        flash_errors(form)

    return render_extensions('users/reset.html', resetform=form)

@blueprint.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
        from nostra.settings import Config

        ts = URLSafeTimedSerializer(Config.SECRET_KEY)
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        return render_template("404.html")

    form = PasswordForm()

    if form.validate_on_submit():
        emailuser = User.query.filter_by(email=email).first_or_404()
        emailuser.set_password(form.password.data)
        emailuser.save()
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)

    return render_extensions('users/reset_with_token.html', resetform=form, token=token)


@blueprint.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = PasswordForm()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        current_user.save()
        return redirect(url_for('user.profile'))
    else:
        flash_errors(form)

    return render_extensions('users/change_password.html', resetform=form)


@blueprint.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = UsernameForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.save()
        return redirect(url_for('user.profile'))
    else:
        flash_errors(form)

    return render_extensions('users/change_username.html', resetform=form)

@blueprint.route('/unsubscribe')
@login_required
def unsubscribe():
    return render_extensions('users/unsubscribe.html')


@blueprint.route('/unsubscribe_confirm')
@login_required
def unsubscribe_confirm():
    user = current_user
    user.username = '%s (Unsubscribed)' % (user.username,)
    user.email = '%s (Unsubscribed)' % (user.email,)
    user.is_admin = False
    user.active = False
    user.save()
    logout_user()
    return redirect(url_for('public.home'))
