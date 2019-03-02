from __future__ import print_function
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, url_for, redirect, request, flash, request
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import argparse
import imutils
import json
import urllib
import cv2
import os
from werkzeug.utils import secure_filename
from PIL import Image

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask("__app__")
app.config['SECRET_KEY'] = 'a551d32359baf371b9095f28d45347c8b8621830'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('calculator.html', val=1)

from flask import send_from_directory

# Watershed Algorithm
def equalize(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(ycrcb)
    cv2.equalizeHist(channels[0], channels[0])
    cv2.merge(channels, ycrcb)
    cv2.cvtColor(ycrcb, cv2.COLOR_YCR_CB2BGR, img)
    return img

def Watershed(location_det):
	print(location_det)
	image = cv2.imread(location_det)
	im = equalize(image)
	shifted = cv2.pyrMeanShiftFiltering(image, 21, 51)

	gray = cv2.cvtColor(shifted, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	plt.imshow(thresh, cmap=plt.get_cmap('gray'))

	D = ndimage.distance_transform_edt(thresh)
	localMax = peak_local_max(D, indices=False, min_distance=20,
	                          labels=thresh)

	markers = ndimage.label(localMax, structure=np.ones((3, 3)))[0]
	labels = watershed(-D, markers, mask=thresh)
	print("[INFO] {} unique segments found".format(len(np.unique(labels)) - 1))

	for label in np.unique(labels):
	    if label == 0:
	        continue
	    mask = np.zeros(gray.shape, dtype="uint8")
	    mask[labels == label] = 255
	    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	    
	    for (i, c) in enumerate(cnts):
	 
	        ((x, y), _) = cv2.minEnclosingCircle(c)
	        cv2.putText(image, "#{}".format(i + 1), (int(x) - 10, int(y)),
	                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
	        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

	# plt.savefig('./static/images/fig1.png')
	plt.figure()
	plt.imshow(image, cmap='gray')
	plt.axis('off')
	plt.savefig('fig1.png')
	imag = Image.open('fig1.png')
	imag.show()
	
# To measure the dimensions
def midpoint(ptA,ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def measure_dim(loc):

	# ap = argparse.ArgumentParser()
	# ap.add_argument("-i", "--image", required = True, help="path to input image")
	# ap.add_argument("-w", "--width", type=float, required=True, help="width of the object")
	# args = vars(ap.parse_args())
	image = cv2.imread(loc)
	# image = cv2.imread(args["image"])
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (7,7), 0)

	edged = cv2.Canny(gray, 50, 100)
	edged = cv2.dilate(edged, None, iterations = 1)
	edged = cv2.erode(edged, None, iterations = 1)

	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	(cnts, _) = contours.sort_contours(cnts)
	pixelsPerMetric = None

	for c in cnts:
	    if cv2.contourArea(c) < 100:
	        continue
	    orig = image.copy()
	    box = cv2.minAreaRect(c)
	    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	    box = np.array(box, dtype="int")
	    box = perspective.order_points(box)
	    cv2.drawContours(orig, [box.astype("int")], -1, (0,255,255), 2)
	
	for (x,y) in box: 
	    cv2.circle(orig,(int(x),int(y)), 5, (0,0,255), -1)
	
	(tl, tr, br, bl) = box
	(tltrX, tltrY) = midpoint(tl,tr)
	(blbrX, blbrY) = midpoint(bl,br)
	(tlblX,tlblY) = midpoint(tl,bl)
	(trbrX, trbrY) = midpoint(tr,br)

	#Draw the midpoints on the image
	cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

	#intersect the lines between midpoints
	cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
			(255,255, 255), 2)
	cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
			(255, 255, 255), 2)
	#compute the Euclidean distance between midpoints
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
	#We initialize the pixels per metric has not been established 
	if pixelsPerMetric is None:
	    pixelsPerMetric = dB / 750
	dimA = dA / pixelsPerMetric
	dimB = dB / pixelsPerMetric
	#to compute the final object size
	cv2.putText(orig, "{:.1f} feet".format(dimA*10),
			(int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (255, 0, 0), 2)
	cv2.putText(orig, "{:.1f} feet".format(dimB),
			(int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, (255, 0, 0), 2)
	area = dimA*dimB
	dims = area
	print(f'The dims: {dims}')
	return dims

@app.route('/uploads/<filename>')
def uploaded_file(filename):
	# print('./static/images/'+filename)
	Watershed(str('./static/images/'+filename))
	dims = measure_dim(str('./static/images/'+filename))
	dims/=10000
	return render_template('calculator.html', val=1, dims=dims)

# Least Geographic Elevation
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

# All routes beyond this
@app.route('/')
def home():
	return render_template('index.html', title='SIH 2019')

@app.route('/rooftop')
def rooftop():
	return render_template('roof.html', title='Rooftop Detection')

@app.route('/references')
def references():
	return render_template('references.html', title='References')

@app.route('/calculator', methods=['GET','POST'])
def calculator():
	pos = postion(13.00011,77.00011,13.0011,77.00111)
	return render_template('calculator.html', title='Calculator', position=pos, val=1)

@app.route('/trial', methods=['GET'])
def trial():
	return render_template('trial.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')

app.run(debug=True, port=5002)