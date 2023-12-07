from flask import Flask, render_template, request, redirect, url_for
import baseball_manager  # import your script here

app = Flask(__name__)

@app.route('/')
def index():
    lineup = baseball_manager.read_lineup()
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

@app.route('/remove_player/<string:name>')
def remove_player(name):
    baseball_manager.remove_player(name)
    return redirect(url_for('index'))


@app.route('/edit_player/<string:name>', methods=['GET'])
def edit_player(name):
    player = baseball_manager.get_player(name)
    if player is None:
        return redirect(url_for('index'))  # Redirect if player not found
    return render_template('edit_player.html', player=player)

@app.route('/update_player', methods=['POST'])
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


if __name__ == '__main__':
    app.run(debug=True)
