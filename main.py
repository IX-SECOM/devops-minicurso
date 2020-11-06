from flask import Flask, render_template, request, redirect, url_for

from form import IMCForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'who-let-the-dogs-out'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.jinja2')


@app.route('/error')
@app.route('/error/<error_message>')
def error(error_message=None):
    return render_template("error.jinja2", error=error_message)


@app.route('/imc', methods=['GET', 'POST'])
def imc_route():
    form = IMCForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            imc = imc_calc(form.peso.data, form.altura.data)
            return render_template('imc_result.jinja2', imc_result=imc)
        else:
            return redirect(url_for('error', error_message=form.errors))

    return render_template('imc_calc.jinja2', form=form)


def imc_calc(peso: float, altura: float) -> float:
    return round(peso/altura**2, 2)


@app.errorhandler(Exception)
def all_exception_handler(error_):
    return redirect(url_for('error', error_message=error_))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
