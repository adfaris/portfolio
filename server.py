from flask import Flask, render_template, send_from_directory, url_for, request, redirect, jsonify
from markupsafe import escape
import csv
from flask_pymongo import PyMongo



app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb+srv://adfaris_db_user:@contactinfo.ek1jcgg.mongodb.net/?appName=contactInfo"


mongo = PyMongo(app)

# @app.route('/<username>/<int:post_id>')
# def home(username=None, post_id=None):
#     return render_template('index.html', name=username, post_id=post_id)

# @app.route('/')
# def home():
#     return render_template('index.html')

# users_collection = mongo.db.contact  # 'users' is the collection name
users_collection = mongo.cx["Users_info"]["contact"]



@app.route("/add_test_user")
def add_test_user():
    test_user = {"name": "Alice", "email": "alice@example.com"}
    inserted_id = users_collection.insert_one(test_user).inserted_id
    return {"msg": "Test user added", "id": str(inserted_id)}

# @app.route("/test")
# def test_db():
#     try:
#         db_names = mongo.cx.list_database_names()  # cx is the client
#         return {"databases": db_names}
#     except Exception as e:
#         return {"error": str(e)}

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route("/test")
def test_db():
    try:
        db_names = mongo.cx.list_database_names()
        return {"databases": db_names}
    except Exception as e:
        return {"error": str(e)}

def write_to_text(data):
    email = data['email']
    subject = data['subject']
    message = data['message']

    with open("database.txt", "a", encoding="utf-8") as f:
        f.write(f' \n {email}, {subject}, {message} ')

def write_to_csv(data):
    email = data['email']
    subject = data['subject']
    message = data['message']

    with open('database.csv', 'a', newline='') as csv_database:
        csv_writer = csv.writer(csv_database, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    try:
        if request.method == 'POST':
            data = request.form.to_dict()
            # write_to_text(data)
            # write_to_csv(data)
            users_collection.insert_one(data)
            return redirect('/thankyou.html')
        else:
            return 'something went wrong'
    except Exception as e:
        return {"error": str(e)}


# @app.route("/about.html")
# def about():
#     return render_template('about.html')


# @app.route("/works.html")
# def works():
#     return render_template('works.html')


# @app.route("/contact.html")
# def contact():
#     return render_template('contact.html')

# @app.route('/favicon.ico')
# def favicon():
#     return app.send_static_file('favicon.ico')

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    if request.method == 'POST':
        data = request.form.to_dict()
        breakpoint()
        print(request)
    return 'form submitted'

    # return f'Hello my dear friend {escape(username).upper()}'

