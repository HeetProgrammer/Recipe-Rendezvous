from directory import app, db, api_key
from flask import render_template, redirect, url_for, flash, request
from directory.models import User
from directory.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
import requests

headers = {
    "x-api-key": api_key,
}
random_recipes_url = "https://api.spoonacular.com/recipes/random"



@app.route("/")
@app.route("/home<tags>")
def home_page(tags=None):
    results = []

    if current_user.is_authenticated:
        if not tags:
        
            params = {
                "number": 10,
            }
            response = requests.get(random_recipes_url, headers=headers, params=params)
            results = response.json()
            print(results)
        else:
            params = {
            "number": 10,
            "tags": tags
            }
            response = requests.get(random_recipes_url, headers=headers, params=params)
            results = response.json()
            print(results)


    return render_template("index.html", results=results)


@app.route('/register', methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Created Successfully! You are logged in as {user_to_create.username} ", category="success")
        return redirect(url_for('home_page'))
    
    if form.errors:
        for error in form.errors.values():
            flash(f"There was an error: {error}", category="danger")

    return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user:
            if attempted_user.check_password_correction(form.password.data):
                login_user(attempted_user)
                flash(f"Success! You are logged in as {attempted_user.username} ", category="success")
                return redirect(url_for('home_page'))
    
    for error in form.errors:
        if error:
            flash(error, category='danger')
    return render_template('login.html', form=form)

@login_required
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for('home_page'))

@login_required
@app.route("/filter", methods=["GET", "POST"])
def filter_results():
    if request.method == "POST":
        options = ['vegetarian', 'non-vegetarian', 'indian', 'japanese', 'american', 'italian', 'mexican', 'spanish', 'french', 'chinese']
        checked_options = []
        print(request.form)
        for option in options:
            if option in request.form:
                checked_options.append(option)
        
        tags = ','.join(checked_options)
        print(checked_options)
        print(tags)
        return redirect(f'/home{tags}')


@login_required
@app.route("/recipe_info/<int:id>")
def recipe_info(id):
    recipe_info_url = f"https://api.spoonacular.com/recipes/{id}/information"
    response = requests.get(recipe_info_url, headers=headers)
    result = response.json()
    return render_template("recipe_info.html", result=result)

        
        


