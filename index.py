from PIL import Image #pip install Pillow
from flask import Flask, send_file, request #pip install flask
from io import BytesIO
from random import randint, seed

import perlin
import walk

app = Flask(__name__)

def mix(x,y,a):
	return x*(1-a)+y*a

def genPattern(cord, hashfunc, domain=2):
	if(domain == 0):
		return perlin.fBm(cord[0], cord[1], hashfunc=hashfunc)
	elif(domain == 1):
		qx = perlin.fBm(cord[0], cord[1], hashfunc=hashfunc)
		qy = perlin.fBm(cord[0]+2.3, cord[1]+5.2, hashfunc=hashfunc)
		return (perlin.fBm(cord[0]+ 4*qx, cord[1]+ 4*qy, hashfunc=hashfunc), qx, qy)
	elif(domain == 2):
		qx = perlin.fBm(cord[0], cord[1], hashfunc=hashfunc)
		qy = perlin.fBm(cord[0]+2.3, cord[1]+5.2, hashfunc=hashfunc)
		rx = perlin.fBm(cord[0]+ 4*qx + 2.2, cord[1]+ 4*qy + 3.2, hashfunc=hashfunc)
		ry = perlin.fBm(cord[0]+ 4*qx + 1.5, cord[1]+ 4*qy + 2.4, hashfunc=hashfunc)
		return (perlin.fBm(cord[0]+ 4*rx, cord[1]+ 4*ry, hashfunc=hashfunc), qx, qy, rx, ry)

def genImage(w,h,d,q,s):
	width = 500 if w is None else w
	height = 500 if h is None else h
	d = 2 if d is None else d
	q = "" if q is None else q
	s = 64 if s is None else s
	seed(q)
	
	color1 = (randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
	color2 = (randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
	color3 = (randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
	color4 = (randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
	color5 = (randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
	color6 = (randint(0,255)/255,randint(0,255)/255,randint(0,255)/255)
	
	pixellist = [color1]*width*height
	hash = perlin.PermHash(None)#[1,5,4,7,4,2,56,2,3223,1,4])
	domain = d
	#TODO ensure perline are max range between 0 and 1, not 0.3-0.7 etc.
	for x in range(0,width):
		for y in range(0,height):
			tx = x - width/2
			ty = y - height/2
			ret = genPattern((tx/s,ty/s), hash, domain)
			r = 0
			g = 0
			b = 0
			if(domain == 0):
				r = int(mix(color1[0], color2[0], ret)*255)
				g = int(mix(color1[1], color2[1], ret)*255)
				b = int(mix(color1[2], color2[2], ret)*255)
			elif(domain == 1):
				(f,qx,qy) = ret
				r = int(mix(color1[0], mix(color2[0], mix(color3[0], color4[0], f), qx), qy)*255)
				g = int(mix(color1[1], mix(color2[1], mix(color3[1], color4[1], f), qx), qy)*255)
				b = int(mix(color1[2], mix(color2[2], mix(color3[2], color4[2], f), qx), qy)*255)
			elif(domain == 2):
				(f,qx,qy,rx,ry) = ret
				r = int(mix(color1[0], mix(color2[0], mix(color3[0], mix(color4[0], mix(color5[0], color6[0], f), qx), qy), rx), ry)*255)
				g = int(mix(color1[1], mix(color2[1], mix(color3[1], mix(color4[1], mix(color5[1], color6[1], f), qx), qy), rx), ry)*255)
				b = int(mix(color1[2], mix(color2[2], mix(color3[2], mix(color4[2], mix(color5[2], color6[2], f), qx), qy), rx), ry)*255)
			pixellist[x + width*y] = (r,g,b)
	
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
	print ("recieved")
	"""
		If no arguments are provided,
		then ultrarandom mode - where all
		parameters will be randomised
	"""
	"""Optional arguments:
		w/width: int,
		h/height: int,
		d/domain: 0/1/2 - warp factor
		q/query: string
	"""
	width = request.args.get('w')
	height = request.args.get('h')
	domain = request.args.get('d')
	query = request.args.get('q')
	scale = request.args.get('s')

	return genImage(width,height,domain,query,scale)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=7791)