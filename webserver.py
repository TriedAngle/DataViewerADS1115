from flask import Flask
from flask import render_template
app = Flask(__name__)

user = {
    'username': 'Sebastian',
    'age': 17
}

@app.route('/')
def home():
    return render_template('Home.html', title='Home', user=user)



if __name__ == "__name__":
    app.run(debug=True, port=5000)