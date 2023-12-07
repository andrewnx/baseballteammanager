from flask import Flask, render_template, request, redirect, url_for
import baseball_manager  # import your script here

app = Flask(__name__)

@app.route('/')
def index():
    lineup = baseball_manager.read_lineup()
    return render_template('index.html', lineup=lineup)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        at_bats = int(request.form['at_bats'])
        hits = int(request.form['hits'])
        baseball_manager.add_player(name, position, at_bats, hits)
        return redirect(url_for('index'))
    return render_template('add_player.html')




if __name__ == '__main__':
    app.run(debug=True)
