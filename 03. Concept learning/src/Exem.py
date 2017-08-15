import math
while a<height:
    b = 0
    while b < width:
        index = 3*(a*width+b)
        red = pic[index]
        green = pic[index+1]
        blue = pic[index+1]
        gray = int(0.5+.3*red+.59*green+.11*blue)
        grayarr.append(gray)
        b+=1
    a+=1

blur = []
x = 0
while x<height:
	y = 0
	while y<width:
		if x==0 or y==0 or x+1==height or y+1==width:
			blur.append(grayarr[x*width+y])
		else:
			mid = (x*width+y)
			top = (mid-width)
			bottom = (mid+width)
			left = (mid-1)
			right = (mid+1)
			topleft = (mid-width-1)
			topright = (mid-width+1)
			bottomleft = (mid+width-1)
			bottomright = (mid+width+1)
			blurrr = int(.5+ ((.0625)*(grayarr[topleft]+grayarr[topright]+grayarr[bottomleft]+grayarr[bottomright])+(0.125)*(grayarr[top]+grayarr[bottom]+grayarr[left]+grayarr[right])+0.25*grayarr[mid]))
			blur.append(blurrr)
                y+=1
        x+=1

 
gx = []
gy = []
gxgy = []
x = 0
while x<height:
	y = 0
	while y<width:
		if x==0 or y==0 or x+1==height or y+1==width:
			gx.append(0)
			gy.append(0)
			gxgy.append(0)
		else:
			mid = (x*width+y)
			top = (mid-width)
			bottom = (mid+width)
			left = (mid-1)
			right = (mid+1)
			topleft = (mid-width-1)
			topright = (mid-width+1)
			bottomleft = (mid+width-1)
			bottomright = (mid+width+1)
			gxishere = ((((-.125)*(blur[topleft]+blur[bottomleft]))+ ((.125)*(blur[topright]+blur[bottomright]))+((-0.25)*(blur[left]))+((0.25)*(blur[right]))))
			gyishere = ((((-.125)*(blur[bottomleft]+blur[bottomright]))+ ((.125)*(blur[topleft]+blur[topright]))+((-0.25)*(blur[bottom]))+((0.25)*(blur[top]))))
			
			gx.append(gxishere)
			gy.append(gyishere)
            		angle = math.atan2(gxishere, gyishere)
            		dx = int(round(math.cos(angle))) 
            		dy = int(round(math.sin(angle)))
            		x1 = x+dx
            		y1 = y-dy
            		x2 = x-dx
            		y2 = y+dy
           		mid = (x1*width+y1)
			top = (mid-width)
			bottom = (mid+width)
			left = (mid-1)
			right = (mid+1)
			topleft = (mid-width-1)
			topright = (mid-width+1)
			bottomleft = (mid+width-1)
			bottomright = (mid+width+1)
            		gx1 = ((((-.125)*(blur[topleft]+blur[bottomleft]))+ ((.125)*(blur[topright]+blur[bottomright]))+((-0.25)*(blur[left]))+((0.25)*(blur[right]))))
            		gy1 = ((((-.125)*(blur[bottomleft]+blur[bottomright]))+ ((.125)*(blur[topleft]+blur[topright]))+((-0.25)*(blur[bottom]))+((0.25)*(blur[top]))))
            		mid = (x2*width+y2)
			top = (mid-width)
			bottom = (mid+width)
			left = (mid-1)
			right = (mid+1)
			topleft = (mid-width-1)
			topright = (mid-width+1)
			bottomleft = (mid+width-1)
			bottomright = (mid+width+1)
           		gx2 = ((((-.125)*(blur[topleft]+blur[bottomleft]))+ ((.125)*(blur[topright]+blur[bottomright]))+((-0.25)*(blur[left]))+((0.25)*(blur[right]))))
            		gy2 = ((((-.125)*(blur[bottomleft]+blur[bottomright]))+ ((.125)*(blur[topleft]+blur[topright]))+((-0.25)*(blur[bottom]))+((0.25)*(blur[top]))))
            
           		biggestg = max((abs(gxishere)+abs(gyishere)),(abs(gx1)+abs(gy1)),(abs(gx2)+abs(gy2)))

			gxgy.append(biggestg)
        	y+=1
       	x+=1

   
