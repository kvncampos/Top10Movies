import json
import requests
from flask import Flask, flash, render_template, redirect, session, url_for, request
from flask_cors import CORS, cross_origin
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from forms.add_form import SearchMovieForm
from forms.edit_form import RateMovieForm
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from api.db import create_db_and_tables, db_get_movies, db_get_movie, db_add_movie, db_update_movie, db_delete_movie
from api.models import Movie
from api.tmdb_api import TMDBApi
from dotenv import load_dotenv
from os import environ
from icecream import ic

'''

'''

# Load ENV Variables
load_dotenv()

# Load TMBDB API CLASS
movie_api = TMDBApi()

# Start Flask App
app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = environ.get('CORS_SECRET_KEY')
app.config['CORS_HEADERS'] = 'Content-Type'
Bootstrap5(app)

# CREATE DB and CREATE TABLES
create_db_and_tables()
 
# ---------------------------- ROUTES ----------------------------
@app.route("/")
def home():
    movies = db_get_movies()
    # for movie in movies:
        # ic(movie)
    return render_template("index.html", movies=movies)


from flask import session

@app.route("/add/", methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie_name = request.form.get('name')
        print(f"Movie Title: {movie_name}")
        response = movie_api.search_movie(movie_name)
        # print(type(response))
        
        # Serialize the JSON response to a string
        response_str = json.dumps(response)
        
        # Store the serialized response data in the session
        session['response'] = response_str
        
        # Redirect to the select_movie route
        return redirect(url_for('select_movie'))
    form = SearchMovieForm()
    return render_template("add.html", form=form)

@app.route("/select/", methods=['GET', 'POST'])
def select_movie():
    if request.method == 'POST':
        movie_id = request.form.get('id')
        if movie_id:
            # Redirect to the search_movie route with the movie ID
            return redirect(url_for('movie_details', id=movie_id))
        else:
            return "Missing MovieID"
    # Retrieve the serialized response data from the session
    response_str = session.pop('response', None)
    if response_str:
        # Deserialize the response string back to a JSON object
        response = json.loads(response_str)
        # Pass the response data to the template
        return render_template("select.html", movie_list=response)
    else:
        # Handle case where response data is not found in the session
        return "Response data not found."

@app.route('/movie-details/<id>', methods=['GET'])
def movie_details(id):
    # Get Movie Details from API
    movie_details = movie_api.movie_details(id)
    
    # Add Movie to DB
    status = db_add_movie(movie_details)

    if not status:
        flash("Movie already exists in DB.")
    else:
        flash("Movie added successfully.")
        movie = db_get_movie(movie_details)
        # TODO 1: Fix the Form in edit_movie, looks very generic.
        return redirect(url_for('edit_movie', id=movie.id))
    
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_movie(id=None):
    form = RateMovieForm()
    if request.method == 'POST':
        # Access form data using request.form
        review = request.form.get('review')
        rating = request.form.get('rating')
        
        # Update the movie in the database
        db_update_movie(id, rating, review)
        flash('Movie has been updated!')
        
        return redirect(url_for('home'))
    
    return render_template('edit.html', form=form, id=id)


@app.route('/delete/<int:id>', methods=['POST'])
def delete_movie(id=None):
    if request.method == 'POST':
        # Assuming you have a function to update the movie in the database
        db_delete_movie(id)
        return redirect(url_for('home'))
    else:
        print("HTTP/500: Issue with Delete API.")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
