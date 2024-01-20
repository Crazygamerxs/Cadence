from bson import ObjectId
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz  # Change time zone
from speech_text import speech_to_text
from pymongo import MongoClient

app = Flask(__name__)

# Replace "YOUR_PASSWORD" with your MongoDB Atlas password
password = "Hatakekakashi786"

# Connect to MongoDB
cluster = MongoClient(f"mongodb+srv://Crazygamerxs:{password}@cluster0.tvv8ix3.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Hackville"]
collection = db["Cadence"]

# Home route for displaying and adding new items
@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_title = request.form["title"]
        user_desc = request.form["desc"]

        ist_tz = pytz.timezone('Asia/Kolkata')
        ist_datetime = datetime.now(tz=ist_tz)
        date_format = '%d-%m-%Y %H:%M:%S'
        date_str = ist_datetime.strftime(date_format)
        date_created = datetime.strptime(date_str, date_format)

        post = {"title": user_title, "desc": user_desc, "date_created": date_created}
        collection.insert_one(post)

    all_items_cursor = collection.find()
    # Convert the cursor to a list
    all_items = list(all_items_cursor)
    return render_template("index.html", all_todos=all_items)


# Update route
@app.route("/update/<string:_id>", methods=["GET", "POST"])
def update_item(_id):
    if request.method == "POST":
        user_title = request.form["title"]
        user_desc = request.form["desc"]

        collection.update_one({"_id": ObjectId(_id)}, {"$set": {"title": user_title, "desc": user_desc}})
        return redirect("/")

    item = collection.find_one({"_id": ObjectId(_id)})
    return render_template("update.html", todo=item)

# Delete route
@app.route('/delete/<string:_id>')
def delete_item(_id):
    collection.delete_one({"_id": ObjectId(_id)})
    return redirect('/')

# Search route
@app.route('/search', methods=["GET", "POST"])
def search_item():
    # Get the search query from the URL parameter
    search_query = request.args.get('query')

    # Perform the search query
    result = collection.find({"title": search_query})
    
    # Render the result
    return render_template('result.html', posts=result)

# Speech to Text route
@app.route('/speech_text')
def speech_text_route():
    speech_to_text()
    return render_template('recording.html')

# Survey route
@app.route('/survey', methods=["GET", "POST"])
def onboarding_survey():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        living_situation = request.form["living_situation"]
        annual_income = request.form["annual_income"]
        yearly_expenses = request.form["yearly_expenses"]

        survey_entry = OnboardingSurvey(
            name=name,
            age=age,
            living_situation=living_situation,
            annual_income=annual_income,
            yearly_expenses=yearly_expenses
        )

        db.session.add(survey_entry)
        db.session.commit()

        return redirect("/thank-you")

    return render_template("survey.html")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
