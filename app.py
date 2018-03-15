from flask import Flask, render_template

DEBUG = False

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=DEBUG)