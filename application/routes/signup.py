import random, math, datetime
from flask import current_app as app
from flask import abort, request, render_template
from flask import Blueprint, url_for
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, validators
from ..models.users import User, UserStatus
from .. import db

blueprint = Blueprint('signup', __name__, template_folder="templates")

class SignupForm(Form):
    username = StringField('Yunlib Account', [ validators.DataRequired(), validators.Length(min=0,max=64) ])
    password = PasswordField('Yunlib Password',[ validators.DataRequired(), validators.Length(min=0,max=64) ])
    confirmpw= PasswordField('Cofirm Password',[ validators.DataRequired(), validators.EqualTo('password', message='Passwords must match') ])

# TODO: Move these code to somewhere else
def verification_code_generator():
    # Generate a string with 6 random number
    return str(math.floor(random.random() * 10 ** 6))

# TODO: Move these code to somewhere else
def verification_due_generator():
    # Generate a datetime after 10 min by now
    return datetime.datetime.now() + datetime.timedelta(minutes = 10)

@blueprint.route('/signup', methods = ['GET', 'POST'])
def signup():
    remote_address = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if remote_address != "127.0.0.1":
        abort(403)

    form = SignupForm(request.form)

    if request.method == 'POST' and form.validate():
        # Create new user and wait for code verification
        # TODO: There is a possible chance that code get conflict
        verify_code = verification_code_generator()
        verify_due  = verification_due_generator()
        user = User(
                userid = "--------------------------------",
                lib_username = form.username.data,
                lib_password = form.password.data,
                status = UserStatus.requireVerify,
                verify_code = verify_code,
                verify_due  = verify_due
                )
        db.session.add(user)
        db.session.commit()

        return "Please tell your bot 'verify %s' to finish registration. <br> Duetime: %s" % (verify_code, verify_due)

    return render_template("signup.html", form = form)
