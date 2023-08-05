"""
Methods for manipulating the loaded data
"""
import numpy as np
from scipy.signal import find_peaks, savgol_filter, gaussian, convolve
from scipy.interpolate import interp1d
from pysprint.utils import findNearest, _handle_input


def savgol(
	initSpectrumX, initSpectrumY, referenceArmY, sampleArmY, window=101,
	order=3):

	Xdata, Ydata = _handle_input(
		initSpectrumX, initSpectrumY, referenceArmY, sampleArmY
		)
	xint, yint = interpolate_data(Xdata, Ydata, [], [])
	if window > order:
		try:
			if window % 2 == 1:
				fil = savgol_filter(yint, window_length = window, polyorder = order)
				return xint, fil
			else:
				fil = savgol_filter(yint, window_length = window + 1, polyorder = order)
				return xint, fil
		except Exception as e:
			print(e)
	else:
		raise ValueError('window must be bigger than order (currently {}/{})'.format(window, order))

# def cwt(initSpectrumX, initSpectrumY, referenceArmY, sampleArmY, proMax=1, proMin=1, threshold=0.1):   
# 	if len(initSpectrumX) > 0 and len(referenceArmY)>0 and len(sampleArmY)>0:
# 		Ydata = (initSpectrumY-referenceArmY-sampleArmY)/(2*np.sqrt(referenceArmY*sampleArmY))
# 	if len(initSpectrumX) == 0:
# 		raise
# 	elif len(referenceArmY) == 0 or len(sampleArmY) == 0:
# 		Ydata = initSpectrumY
# 	Xdata = initSpectrumX

# 	maxIndexes = find_peaks_cwt(Ydata, np.arange(1, 50)) 
# 	Ydata_rec = 1/Ydata
# 	minIndexes = find_peaks_cwt(Ydata_rec, np.arange(1, 1000))

# 	min_idx = []
# 	max_idx = []

# 	for idx in maxIndexes:
# 		if np.abs(Ydata[idx]) > threshold:
# 			max_idx.append(idx)
# 	for idx in minIndexes:
# 		if np.abs(Ydata[idx]) > threshold:
# 			min_idx.append(idx)

# 	if len(Xdata[max_idx]) != len(Ydata[max_idx]) or len(Xdata[min_idx]) != len(Ydata[min_idx]):
# 		raise ValueError('Something went wrong, try to cut the edges of data.')

# 	return Xdata[max_idx], Ydata[max_idx], Xdata[min_idx], Ydata[min_idx]

def find_peak(
	initSpectrumX, initSpectrumY, referenceArmY, sampleArmY,
	proMax=1, proMin=1, threshold=0.1):   

	Xdata, Ydata = _handle_input(initSpectrumX, initSpectrumY, referenceArmY, sampleArmY)
	maxIndexes, _ = find_peaks(Ydata, prominence = proMax) 
	Ydata_rec = 1/Ydata
	minIndexes, _ = find_peaks(Ydata_rec, prominence = proMin)
	min_idx = []
	max_idx = []
	for idx in maxIndexes:
		if np.abs(Ydata[idx]) > threshold:
			max_idx.append(idx)
	for idx in minIndexes:
		if np.abs(Ydata[idx]) > threshold:
			min_idx.append(idx)

	if len(Xdata[max_idx]) != len(Ydata[max_idx]) or len(Xdata[min_idx]) != len(Ydata[min_idx]):
		raise ValueError('Something went wrong, try to cut the edges of data.')

	return Xdata[max_idx], Ydata[max_idx], Xdata[min_idx], Ydata[min_idx]


def convolution(
	initSpectrumX, initSpectrumY, referenceArmY, sampleArmY,
	standev=200):

	Xdata, Ydata = _handle_input(
		initSpectrumX, initSpectrumY, referenceArmY, sampleArmY
		)
	xint, yint = interpolate_data(Xdata, Ydata, [], [])
	window = gaussian(len(xint), std=standev)
	smoothed = convolve(yint, window/window.sum(), mode='same')
	return xint, smoothed

def interpolate_data(initSpectrumX, initSpectrumY, referenceArmY, sampleArmY):
	Xdata, Ydata = _handle_input(
		initSpectrumX, initSpectrumY, referenceArmY, sampleArmY
		)
	xint = np.linspace(Xdata[0], Xdata[-1], len(Xdata))
	intp = interp1d(Xdata,Ydata, kind='linear')
	yint = intp(xint)
	return xint, yint


def cut_data(
	initSpectrumX, initSpectrumY, referenceArmY, sampleArmY,
	startValue=-9999, endValue=9999):

	Xdata, Ydata = _handle_input(
		initSpectrumX, initSpectrumY, referenceArmY, sampleArmY
		)
	if startValue < endValue:
		lowItem, lowIndex = findNearest(Xdata, startValue)
		highItem, highIndex = findNearest(Xdata, endValue)
		mask = np.where((Xdata>=lowItem) & (Xdata<=highItem))
		return Xdata[mask], Ydata[mask]
	else:
		pass

