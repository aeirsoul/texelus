from PIL import Image #pip install Pillow
from flask import Flask, send_file #pip install flask
from io import BytesIO
from random import randint

app = Flask(__name__)

def genImage():
	width = randint(100,1000)
	height = randint(100,1000)

	my_list = [(randint(0,255),randint(0,255),randint(0,255))]*width*height

	assert (len(my_list) == width*height)

	img = Image.new('RGB', (width, height))
	img.putdata(my_list)
	img_io = BytesIO()
	img.save(img_io, 'png')
	img_io.seek(0)
	
	return send_file(img_io, mimetype='image/png')
	

@app.route('/', methods=['GET'])
def img():
	return genImage()

if __name__ == '__main__':
	#app.secret_key = os.urandom(12)
	app.run(debug=True)