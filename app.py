from flask import Flask, render_template, url_for, redirect, request
import json
import urllib

app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'

def elevation(request):
	apikey = "AIzaSyDv9C5WnFwlmPtZWMtH6EqfMhSwJrlCcD0"
	url = "https://maps.googleapis.com/maps/api/elevation/json"
	request = urllib.request.urlopen(url+"?locations="+str(request)+"&key="+apikey)
	try:
		results = json.load(request).get('results')
		if 0 < len(results):
			mat={}
			for i in range(0,len(results)):	    
				elevation = results[i].get('elevation')
				location=results[i].get('location')
				loclat=[]
				loclat.append(location['lat'])
				loclat.append(location['lng'])
				loc=tuple(loclat)
				if elevation not in mat:
					mat[elevation]=[]
				mat[elevation].append(loc)
				# ELEVATION
			return mat
		else:
			print ('HTTP GET Request failed.')
	except ValueError as e:
		print ('JSON decode failed: '+str(request))

def postion(lat1,lon1,lat2,lon2):
  if(lat1>lat2):  # swaping cordinates to get range of latitude and longitude 
    temp=lat1
    lat1=lat2
    lat2=temp
  if(lon1>lon2):
    temp=lon1
    lon1=lon2
    lon2=temp
  res=''   #initializing string with null value
  i=0.0
  i=lat1	#itration variable for varying latitude
  while i<lat2:
    j=0.0
    j=lon1	#iteration variable for varying longitude
    while j<lon2:
      res=res+(str(i))	# adding current latitude to string
      res=res+','	# separator for latitude and longitude
      if((i+0.0001)>=lat2 and (j+0.0001)>=lon2):	#cheacking wheather the coordinate is last one
        res=res+(str(j))	# last coordinate need not to have '|' as its the last one
      else:
        res=res+(str(j))	#else we need to saperate the coordinates with '|'
        res=res+'|'	#adding '|' after one coordinate is entered
      j=j+0.0001		#increasing longitude by 10 meters
    i=i+0.0001		#increasing latitude by 10 meters
  result=elevation(res)		#calling elevaton function to get elevation data
  rest={}			#dictonary 
  for key in sorted(result.keys()):	#getting elevation in sorted order
    rest[key]=result[key]	
  return rest		#getting elevated data in increasing order

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
	pos = postion(13.00011,77.00011,13.0011,77.00111)
	return render_template('calculator.html', title='Calculator', position=pos)

@app.route('/trial', methods=['GET'])
def trial():
	return render_template('trial.html')

app.run(debug=True, port=5001)