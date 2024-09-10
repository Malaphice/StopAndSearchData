from datetime import datetime
from flask import render_template, request, jsonify
from StopAndSearchData import app
from StopAndSearchData.data_fetch import update_data

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/fetch_data', methods=['POST'])
def fetch_data():
    """Handles form submission and fetches data based on user input."""
    
    # Get data from the form
    force = request.form.get('force')
    year = request.form.get('year')
    month = request.form.get('month')

    # Call the update_data function with the selected parameters
    result = update_data(force=force, year=year, month=month)
    
    # Return the result as a JSON response
    return jsonify({"status": result})