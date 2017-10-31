from PIL import Image #pip install Pillow
from flask import Flask, send_file, request #pip install flask
from io import BytesIO
from random import randint

import perlin
import walk

app = Flask(__name__)

def genPattern(cord, hashfunc, domain=2):
	if(domain == 0):
		return perlin.fBm(cord[0], cord[1], hashfunc=hashfunc)
	elif(domain == 1):
		qx = perlin.fBm(cord[0], cord[1], hashfunc=hashfunc)
		qy = perlin.fBm(cord[0]+2.3, cord[1]+5.2, hashfunc=hashfunc)
		return perlin.fBm(cord[0]+ 4*qx, cord[1]+ 4*qy, hashfunc=hashfunc)
	elif(domain == 2):
		qx = perlin.fBm(cord[0], cord[1], hashfunc=hashfunc)
		qy = perlin.fBm(cord[0]+2.3, cord[1]+5.2, hashfunc=hashfunc)
		rx = perlin.fBm(cord[0]+ 4*qx + 1.2, cord[1]+ 4*qy + 3.2, hashfunc=hashfunc)
		ry = perlin.fBm(cord[0]+ 4*qx + 4.2, cord[1]+ 4*qy + 0.4, hashfunc=hashfunc)
		return perlin.fBm(cord[0]+ 4*rx, cord[1]+ 4*ry, hashfunc=hashfunc)

def genImage():
	width = 500#randint(100,1000)
	height = 500#randint(100,1000)

	color1 = (255,255,255)#(randint(0,255),randint(0,255),randint(0,255))
	color2 = (randint(0,255),randint(0,255),randint(0,255))
	
	pixellist = [color1]*width*height
	hash = perlin.PermHash(None)#[1,5,4,7,4,2,56,2,3223,1,4])
	for x in range(0,width):
		for y in range(0,height):
			tx = x - width/2
			ty = y - height/2
			f = abs(genPattern((tx/128,ty/128), hash, 0))
			pixellist[x + width*y] = (int(f*color1[0]),int(f*color1[1]),int(f*color1[2]))
	
	assert (len(pixellist) == width*height)
	
	#postGenList = genWalk(pixellist, color2, width, height, 1, 500)

	img = Image.new('RGB', (width, height))
	img.putdata(pixellist)
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
	app.run(debug=True)