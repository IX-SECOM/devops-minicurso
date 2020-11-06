from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField
from wtforms.validators import DataRequired, NumberRange


class IMCForm(FlaskForm):

    altura = FloatField('altura', validators=[DataRequired(), NumberRange(min=0.5, message="Altura mínima é 0.5!")])

    peso = FloatField('peso', validators=[DataRequired(), NumberRange(min=40, message="Peso mínimo é 40 Kg!")])

    submit = SubmitField('submit')
