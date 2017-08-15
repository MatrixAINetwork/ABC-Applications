import sys
import getopt
import cv2
import math
import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy

class Histogram:
	def __init__(sst, Im, Para):
		"""Create histogram"""
		sst.Para = Para
		sst.hist = cv2.calcHist([Im],[0],None,[sst.Para],[0,sst.Para])
		"""Save cummulative sum and its maximum"""
		sst.cumsum = sst.hist.cumsum()
		sst.cumsum_max = sst.cumsum.max()

	def cdf(sst, i):
		"""Return value of cummulative distribution function at i"""
		return sst.cumsum[i]/sst.cumsum_max

	def new_val(sst, i):
		"""Use cdf to calculate new gray level"""
		return math.floor((sst.Para - 1)*sst.cdf(i))

	def transfer_function(sst, output_file):
		"""Create CDF array then plot"""
		transfer = sst.cumsum / sst.cumsum_max
		plt.plot(transfer)
		plt.xlim(xmax=sst.Para-1)
		plt.ylim(ymax=1.2)
		plt.xlabel("Gray Value")
		plt.ylabel("CDF")
		plt.title("Transfer Function")
		plt.savefig(output_file, bbox_inches="tight")
		plt.clf()	

						
def main():
	def usage():
		print "python histogram_equalization.py -i <inputf> [-o <outputf> -t <transferf> "\
					"-a <histinf> -b <histoutf>]"

	inputf = None
	outputf = None
	transferf = None
	histinf = None
	histoutf = None

	"""Process command line inputs"""
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:a:b:", ["inputf=", "outputf=", 
								 "transferf=", "histinf=", "histoutf="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()	
		elif opt in ("-i", "--inputf"):
			inputf = arg
		elif opt in ("-o", "--outputf"):
			outputf = arg
		elif opt in ("-t", "--transferf"):
			transferf = arg	
		elif opt in ("-a", "--histinf"):
			histinf = arg
		elif opt in ("-b", "--histoutf"):
			histoutf = arg				

	"""Required arguments"""
	if not inputf:
		usage()
		sys.exit()
	
	"""Create image and run histogram equalization"""		 
	Im = cv2.imread(inputf, 0)
	he = HistogramEqualization(Im)
	he.equalize()

	"""Save transfer function plot"""
	if transferf:
		he.transfer_function(transferf)

	"""Save input histogram"""
	if histinf:
		he.histogram_in(histinf)

	"""Save output histogram"""
	if histoutf:
		he.histogram_out(histoutf)		

	"""Save or plot image"""	
	if outputf:
		he.save(outputf)
	else:
		he.plot()

if __name__ == "__main__":
	main()
		