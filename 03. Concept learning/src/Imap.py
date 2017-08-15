import collections
import random

script, source_image, target_image = argv
srcImg = Image.open(source_image)
tgtImg = Image.open(target_image)
srcImg.show()
tgtImg.show()
width, height = srcImg.size
srcPix = srcImg.load()
tgtPix = tgtImg.load()
HiIn = srcImg.histogram()[:256]
HiOut = tgtImg.histogram()[:256]
PixPar = [set() for _ in range(256)]
for i in range(width):
    for j in range(height):
        value = srcPix[i, j][0]
        PixPar[value].add((i, j))

EqB = collections.deque()
excessBins = collections.deque()
deficitBins = collections.deque()
for i, _ in enumerate(HiIn):
    src_i = HiIn[i]
    tgt_i = HiOut[i]
    if src_i < tgt_i:
        deficitBins.append(i)
    elif src_i > tgt_i:
        excessBins.append(i)
    else:
        EqB.append(i)
def change_n_pixels(curVal, tgtVal, nToChange):
    candidatePxls = PixPar[curVal]
    Pi2P = random.sample(candidatePxls, nToChange)
    for pxl in Pi2P:
        srcPix[pxl] = (tgtVal, tgtVal, tgtVal)
        PixPar[curVal].remove(pxl)
        PixPar[tgtVal].add(pxl)
    HiIn[curVal] -= nToChange
    HiIn[tgtVal] += nToChange
def change_n_pixels_smooth(curVal, tgtVal, nToChange):
    Nincrements = abs(curVal - tgtVal)
    for inc in range(Nincrements):
        if tgtVal > curVal:
            try:
                change_n_pixels(curVal+inc, curVal+inc+1, nToChange)
            except IndexError:
                pass
        else:
            try:
                change_n_pixels(curVal-inc, curVal-inc-1, nToChange)
            except IndexError:
                pass
srcImg.show()
