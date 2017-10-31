#TODO Complete this with an actual walk
from random import randint
from copy import deepcopy

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
	initCord = (5,1) #TODO randomise etc..
	
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