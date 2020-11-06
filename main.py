from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'who-let-the-dogs-out'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')


if __name__ == '__main__':
    app.run(port=5000)
