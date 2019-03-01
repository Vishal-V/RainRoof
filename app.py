from flask import Flask, render_template, url_for, redirect

app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'

@app.route('/')
def home():
	return render_template('index.html', title='SIH 2019')

@app.route('/rooftop')
def rooftop():
	return render_template('roof.html', title='Rooftop Detection')

@app.route('/references')
def references():
	return render_template('references.html', title='References')

@app.route('/calculator')
def calculator():
	return render_template('calculator.html', title='Calculator')

app.run(debug=True, port=5001)