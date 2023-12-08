from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import baseball_manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import db, User, Player

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'fab2c24d650cb753060d20eb943b9a60'

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def index():
    lineup = baseball_manager.get_players(current_user.id)
    return render_template('index.html', lineup=lineup)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    error_message = None
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        at_bats = request.form['at_bats']
        hits = request.form['hits']

        # Data validation
        if not name or not position or not at_bats.isdigit() or not hits.isdigit():
            error_message = "Invalid input. Please fill out all fields correctly."
        elif position not in ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P']:
            error_message = "Invalid position. Please enter a valid position."

        if not error_message:
            baseball_manager.add_player(name, position, int(at_bats), int(hits))
            return redirect(url_for('index'))

    return render_template('add_player.html', error=error_message)

@app.route('/remove_player/<int:player_id>')
def remove_player(player_id):
    baseball_manager.remove_player(player_id, current_user.id)
    return redirect(url_for('index'))


@app.route('/edit_player/<string:name>', methods=['GET'])
@login_required
def edit_player(player_id):
    player = baseball_manager.get_player(player_id)
    if player is None:
        return redirect(url_for('index'))  # Redirect if player not found
    return render_template('edit_player.html', player=player)

@app.route('/update_player', methods=['POST'])
@login_required
def update_player():
    error_message = None
    original_name = request.form['original_name']
    name = request.form['name']
    position = request.form['position']
    at_bats = request.form['at_bats']
    hits = request.form['hits']

    if not name or not position or not at_bats.isdigit() or not hits.isdigit():
        error_message = "Invalid input. Please fill out all fields correctly."
    elif position not in ['C', '1B', '2B', '3B', 'SS', 'LF', 'CF', 'RF', 'P']:
        error_message = "Invalid position. Please enter a valid position."

    if not error_message:
        baseball_manager.update_player(original_name, name, position, int(at_bats), int(hits))
        return redirect(url_for('index'))

    player = [original_name, position, at_bats, hits]
    return render_template('edit_player.html', player=player, error=error_message)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        baseball_manager.clone_default_lineup_for_user(user.id)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            # Flash a message to the user indicating login failure
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
