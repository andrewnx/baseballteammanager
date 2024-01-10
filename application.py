from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import baseball_manager
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_pymongo import PyMongo
import os
from bson import ObjectId

mongo = PyMongo()

class User:
    def __init__(self, user_data):
        self.user_data = user_data

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_data['_id'])

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.environ.get('MONGODB_URI')
    app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY') or 'fgqAaLGwkP'
    mongo.init_app(app)

    bcrypt = Bcrypt(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    class RegistrationForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
        password = PasswordField('Password', validators=[DataRequired()])
        confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
        submit = SubmitField('Sign Up')

        def validate_username(self, username):
            users_collection = mongo.db.users
            user = users_collection.find_one({'username': username.data})
            if user:
                raise ValidationError('That username is already taken. Please choose a different one.')

    class LoginForm(FlaskForm):
        username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Login')

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            lineup = baseball_manager.get_players(mongo, current_user['_id'])
        else:
            lineup = []  # Empty list for unauthenticated users

        return render_template('index.html', lineup=lineup, is_authenticated=current_user.is_authenticated)

    @app.route('/add_player', methods=['GET', 'POST'])
    def add_player_route():
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
                user_id = current_user.id
                baseball_manager.add_player(mongo, name, position, int(at_bats), int(hits), current_user['_id'])
                return redirect(url_for('index'))

        return render_template('add_player.html', error=error_message)

    @app.route('/remove_player/<int:player_id>')
    def remove_player(player_id):
        baseball_manager.remove_player(player_id, current_user.id)
        return redirect(url_for('index'))

    @app.route('/edit_player/<int:player_id>', methods=['GET'])
    @login_required
    def edit_player(player_id):
        player = baseball_manager.get_player(mongo, player_id)
        if player is None:
            return redirect(url_for('index'))  # Redirect if player not found
        return render_template('edit_player.html', player=player)

    @app.route('/update_player', methods=['POST'])
    @login_required
    def update_player():
        error_message = None
        player_id = request.form.get('player_id')
        original_name = request.form.get('original_name')
        name = request.form.get('name', '')
        position = request.form.get('position', '')
        at_bats = request.form.get('at_bats', '')
        hits = request.form.get('hits', '')

        player = baseball_manager.get_player(mongo, player_id)
        if player:
            if name:
                player.name = name
            if position:
                player.position = position
            if at_bats.isdigit():
                player.at_bats = int(at_bats)
            if hits.isdigit():
                player.hits = int(hits)
            player.avg = baseball_manager.get_batting_avg(player.at_bats, player.hits)
        else:
            error_message = "Player not found."

        if error_message:
            return render_template('edit_player.html', player=[original_name, position, at_bats, hits], error=error_message)

        return redirect(url_for('index'))

    @app.route("/register", methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user_data = {'username': form.username.data, 'password': hashed_password}
            user_id = baseball_manager.add_user(mongo, user_data)
            baseball_manager.clone_default_lineup_for_user(mongo, user_id)
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            users_collection = mongo.db.users
            user = users_collection.find_one({'username': form.username.data})
            if user and bcrypt.check_password_hash(user['password'], form.password.data):
                user_obj = User(user)  # Wrap dict in User class
                login_user(user_obj)
                return redirect(url_for('index'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)
    
    @login_manager.user_loader
    def load_user(user_id):
        users_collection = mongo.db.users
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        return User(user) if user else None

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))


    if __name__ == '__main__':
        app.run(debug=True)

    return app
