from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('start_page.html')

@app.route('/start_page')
def start_page():
    return render_template('start_page.html')


if __name__ == "__main__":
    app.run()