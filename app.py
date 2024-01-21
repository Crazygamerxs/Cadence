from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz  # Change time zone
from speech_text import speech_to_text


app = Flask(__name__)


# Configuration for SQLAlchemy and Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.sqlite"
db = SQLAlchemy(app)

# Creating Table Todo
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Creating Table OnboardingSurvey
class OnboardingSurvey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    living_situation = db.Column(db.String(100), nullable=False)
    annual_income = db.Column(db.Float, nullable=False)
    yearly_expenses = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"{self.id} - {self.name}"

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

        todo = Todo(title=user_title, desc=user_desc, date_created=date_created)
        db.session.add(todo)
        db.session.commit()

    all_items = Todo.query.all()
    return render_template("Tasks.html", all_todos=all_items)

# Update route
@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update_item(sno):
    if request.method == "POST":
        user_title = request.form["title"]
        user_desc = request.form["desc"]

        item = Todo.query.get_or_404(sno)
        item.title = user_title
        item.desc = user_desc
        db.session.add(item)
        db.session.commit()
        return redirect("/")

    item = Todo.query.get_or_404(sno)
    return render_template("Tasks_update.html", todo=item)

# Delete route
@app.route('/delete/<int:sno>')
def delete_item(sno):
    item = Todo.query.get_or_404(sno)
    db.session.delete(item)
    db.session.commit()
    return redirect('/')

# Search route
@app.route('/search', methods=["GET", "POST"])
def search_item():
    # Get the search query from the URL parameter
    search_query = request.args.get('query')

    # Perform the search query
    result = Todo.query.filter(Todo.title == search_query).all()

    # Render the result
    return render_template('Task_result.html', posts=result)

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
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)