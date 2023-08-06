#############################################################################
#                                                                           #
#    PyMassSpec software for processing of mass-spectrometry data           #
#    Copyright (C) 2019 Dominic Davis-Foster                                #
#                                                                           #
#    This program is free software; you can redistribute it and/or modify   #
#    it under the terms of the GNU General Public License version 2 as      #
#    published by the Free Software Foundation.                             #
#                                                                           #
#    This program is distributed in the hope that it will be useful,        #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#    GNU General Public License for more details.                           #
#                                                                           #
#    You should have received a copy of the GNU General Public License      #
#    along with this program; if not, write to the Free Software            #
#    Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.              #
#                                                                           #
#############################################################################

import pytest
from tests.constants import *

from pyms.IntensityMatrix import build_intensity_matrix_i
from pyms.Noise.Window import window_smooth_im, window_smooth
from pyms.IntensityMatrix import IntensityMatrix
from pyms.IonChromatogram import IonChromatogram
from pyms.Noise.SavitzkyGolay import savitzky_golay
from pyms.TopHat import tophat


def test_window_smooth(tic):
	assert isinstance(tic, IonChromatogram)

	# apply window smoothing: mean and median, in both cases
	# the window is 5 points
	tic1 = window_smooth(tic, window=5)
	assert isinstance(tic1, IonChromatogram)
	
	tic2 = window_smooth(tic, window=5, median=True)
	assert isinstance(tic2, IonChromatogram)
	
	# an example of how to specify window as a time string
	# (7 seconds in this case)
	tic3 = window_smooth(tic, window='7s')
	assert isinstance(tic3, IonChromatogram)
	
	for type in [test_int, test_string, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			window_smooth(type)
	for type in [test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			window_smooth(tic, window=type)
	for type in [test_string, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			window_smooth(tic, median=type)


def test_window_smooth_im(im):
	
	window_smooth_im(im)
	window_smooth_im(im, window=5)
	
	# Use window averaging to smooth all IC's in the IM
	im_smooth = window_smooth_im(im, window=5, median=False)
	assert isinstance(im_smooth, IntensityMatrix)
	
	# find the IC for derivatisation product ion before smoothing
	ic = im.get_ic_at_index(73)
	assert isinstance(ic, IonChromatogram)
	
	# find the IC for derivatisation product ion after smoothing
	ic_smooth = im_smooth.get_ic_at_index(73)
	assert isinstance(ic_smooth, IonChromatogram)

	for type in [test_int, test_string, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			window_smooth_im(type)
	for type in [test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			window_smooth_im(im, window=type)
	for type in [test_string, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			window_smooth_im(im, median=type)


def test_smooth_im(data):
	# Build intensity matrix with defaults, float masses with interval
	# (bin size) of one from min mass
	im = build_intensity_matrix_i(data)
	
	off = im.min_mass
	n_scan, n_mz = im.size
	
	# process data
	for ii in range(n_mz):
		#print("Working on IC#", ii + 1)
		ic = im.get_ic_at_index(ii)
		assert isinstance(ic, IonChromatogram)
		
		# if ((ii+off) in [319, 205, 160, 217]):
		#	ic.write("output/ic-raw-%d.dat" % (ii+off))
		
		ic_smooth = savitzky_golay(ic)
		assert isinstance(ic_smooth, IonChromatogram)
		
		ic_bc = tophat(ic_smooth, struct="1.5m")
		assert isinstance(ic_bc, IonChromatogram)
		
		# if ((ii+off) in [319, 205, 160, 217]):
		#	ic_bc.write("output/ic-flt-%d.dat" % (ii+off))
		
		im.set_ic_at_index(ii, ic_bc)
		assert im.get_ic_at_index(ii) == ic_bc

