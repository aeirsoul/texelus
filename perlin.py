import random
import math
#https://gamedev.stackexchange.com/questions/23625/how-do-you-generate-tileable-perlin-noise
#https://gist.github.com/TimSC/afda36eeb3dac249b589535f8a7ad7b5

dirs = [(math.cos(a * 2.0 * math.pi / 256),
		 math.sin(a * 2.0 * math.pi / 256))
		 for a in range(256)]
		 
class PermHash(object):
	def __init__(self, perm=None):
		if perm is None:
			self._perm = list(range(256))
			random.shuffle(self._perm)
			self._perm += self._perm
		else:
			self._perm = perm

	def __call__(self, *args):
		return self._perm[(self._perm[int(args[0])%len(self._perm)] + int(args[1]))%len(self._perm)]

	def GetSaveState(self):
		return self._perm

def surflet(gridX, gridY, x, y, hashfunc):
	distX, distY = abs(x-gridX), abs(y-gridY)
	polyX = 1 - 6*distX**5 + 15*distX**4 - 10*distX**3
	polyY = 1 - 6*distY**5 + 15*distY**4 - 10*distY**3
	hashed = hashfunc(int(gridX), int(gridY))
	grad = (x-gridX)*dirs[hashed%len(dirs)][0] + (y-gridY)*dirs[hashed%len(dirs)][1]
	return polyX * polyY * grad

def noise(x, y, hashfunc):
	intX, intY = int(math.floor(x)), int(math.floor(y))
	s1 = surflet(intX+0, intY+0, x, y, hashfunc)
	s2 = surflet(intX+1, intY+0, x, y, hashfunc)
	s3 = surflet(intX+0, intY+1, x, y, hashfunc)
	s4 = surflet(intX+1, intY+1, x, y, hashfunc)
	return (s1 + s2 + s3 + s4)

def fBm(x, y, octs=2, hashfunc=PermHash()):
	val = 0
	for o in range(octs):
		scale = 2**o
		val += 0.5**o * noise(x*scale, y*scale, hashfunc)
	return val


if __name__=="__main__":
	from PIL import Image
	size, freq, octs, data = 200, 1/32.0, 2, []

	for y in range(size):
		for x in range(size):
			tx = x - 100
			ty = y - 100
			data.append(fBm(tx*freq, ty*freq))
	im = Image.new("L", (size, size))
	im.putdata(data, 128, 128)
	im.save("noise.png")