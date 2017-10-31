from PIL import Image #pip install Pillow
from flask import Flask, send_file, request #pip install flask
from io import BytesIO
from random import randint
from copy import deepcopy

app = Flask(__name__)

#Recursive structure that returns a list of cords
# that we have walked through
def branch(width, height, cur_cord, cur_depth, maxdepth):
	if(cur_depth == maxdepth):
		return [cur_cord]
		
	(x,y) = deepcopy(cur_cord)
	
	#Randomise direction for next step
	r = randint(0,8)
	if(r == 0):
		x -= 1
		y -= 1
	elif(r == 1):
		y -= 1
	elif(r == 2):
		x += 1
		y -= 1
	elif(r == 3):
		x -= 1
	elif(r == 4):
		x += 1
	elif(r == 5):
		x -= 1
		y += 1
	elif(r == 6):
		y += 1
	elif(r == 7):
		x += 1
		y += 1
		
	#validate
	if(x < 0):
		x = width-1
	elif(x >= width):
		x = 0
		
	if(y < 0):
		y = height-1
	elif(y >= height):
		y = 0
	
	#print ("height: "+str(height) + " x: "+str(x) + " y: "+str(y))
	
	#Take the next step
	#branch(width, height, (x,y), cur_depth+1, maxdepth)+[cur_cord]
	
	return branch(width, height, (x,y), cur_depth+1, maxdepth)+[cur_cord]
	

def genWalk(pixellist, color, width, height, scale, maxdepth):
	#Adjust for scale
	adjustedWidth = int(width/scale)
	adjustedHeight = int(width/scale)
	
	#Choose start point
	initCord = (5,1)
	
	#Do walk
	filledIn = branch(adjustedWidth, adjustedHeight, initCord, 0, maxdepth)
	
	#Fill out our list
	for pix in filledIn:
		#each pixel is worth scale width/height instead of 1
		(x,y) = pix
		#adjust back to normal size
		realX = x*scale
		realY = y*scale
		
		for i in range(0, scale):
			for j in range(0, scale):
				pixellist[(realX+i) + width*(realY+j)] = color
				
	return pixellist		

def genImage():
	width = 500#randint(100,1000)
	height = 500#randint(100,1000)

	color1 = (randint(0,255),randint(0,255),randint(0,255))
	color2 = (randint(0,255),randint(0,255),randint(0,255))
	
	pixellist = [color1]*width*height
	assert (len(pixellist) == width*height)
	
	postGenList = genWalk(pixellist, color2, width, height, 1, 500)

	img = Image.new('RGB', (width, height))
	img.putdata(postGenList)
	img_io = BytesIO()
	img.save(img_io, 'png')
	img_io.seek(0)
	
	return send_file(img_io, mimetype='image/png')
	

@app.route('/', methods=['GET'])
def img():
	"""
		If no arguments are provided,
		then ultrarandom mode - where all
		parameters will be randomised
	"""
	"""Optional arguments:
		w/width: int,
		h/height: int,
		t/type: default "random", "gradient", "...", - colour style
		c/colours: [],
		s/scale: default 10
	"""
	width = request.args.get('width')
	width = request.args.get('height')


	return genImage()

if __name__ == '__main__':
	#app.secret_key = os.urandom(12)
	app.run(debug=True)