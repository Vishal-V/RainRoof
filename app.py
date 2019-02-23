from flask import Flask, render_template, url_for, redirect

app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'

@app.route('/home', methods=['GET, POST'])
def home():
	return render_template('index.html', title='SIH Home')

@app.route('/rooftop')
def rooftop():
	return render_template('roof.html', title='Rooftop Detection')

app.run(debug=True)