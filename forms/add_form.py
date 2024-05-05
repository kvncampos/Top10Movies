from flask_wtf import Form
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length

class SearchMovieForm(Form):
    name = StringField(
        'Movie Title',
        validators=[DataRequired(), Length(min=1, max=30)],
        render_kw={"placeholder": "Ex: Ocean's Eleven"}
    )

    submit = SubmitField('Submit')