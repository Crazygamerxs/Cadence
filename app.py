from flask import Flask, render_template
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

template_folder = os.path.join(script_dir, 'template')
static_folder = os.path.join(script_dir, 'static')

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder, static_url_path='/static')

@app.route('/')
def hello():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(port="8000",debug=True)

