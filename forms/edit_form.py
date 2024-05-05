from flask_wtf import Form
from wtforms import StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import Length, NumberRange, InputRequired


class RateMovieForm(Form):
    review = StringField(
        'Your Review',
        validators=[InputRequired(), Length(min=6, max=100)],
        render_kw={"placeholder": "Enter your review here..."}
    )
    rating = FloatField(
        'Your rating out of 10 e.g. 7.5',
        validators=[InputRequired(), NumberRange(min=0.0, max=10.0, message='Rating Must be between 0 and 10.')],
        render_kw={"placeholder": "Enter your rating here..."}
    )
    submit = SubmitField('Submit', render_kw={"class": "btn btn-primary"})