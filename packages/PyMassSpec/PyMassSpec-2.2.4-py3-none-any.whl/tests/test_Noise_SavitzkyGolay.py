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

from pyms.IntensityMatrix import IntensityMatrix
from pyms.IonChromatogram import IonChromatogram
from pyms.Noise.SavitzkyGolay import savitzky_golay, savitzky_golay_im


def test_savitzky_golay(tic):
	assert isinstance(tic, IonChromatogram)
	
	# apply noise smoothing
	tic1 = savitzky_golay(tic)
	assert isinstance(tic1, IonChromatogram)
	
	assert tic1 != tic
	assert tic1.is_tic()
	assert len(tic1) == 2103
	assert len(tic) == len(tic1)  # Length should be unchanged
	assert tic1.get_intensity_at_index(test_int) == 421885.76190476184
	assert tic1.get_time_at_index(test_int) == 1304.15599823
	assert tic1.get_time_at_index(test_int) == tic.get_time_at_index(test_int)
	assert tic1.time_list[0] == 1.05200003833
	assert tic1.time_list[0] == tic.time_list[0]
	assert tic1.time_step == 1.0560000035830972
	assert tic1.time_step == tic1.time_step
	assert tic1.get_index_at_time(12) == 10
	assert tic1.get_index_at_time(12) == tic1.get_index_at_time(12)
	
	with pytest.warns(Warning):
		tic1.mass
	
	# Test Errors
	for type in [test_string, test_int, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			savitzky_golay(type)
	
	for type in [test_string, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			savitzky_golay(tic, degree=type)
	
	for type in [test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			savitzky_golay(tic, window=type)
		

def test_savitzky_golay_intensity_matrix(im, tic):
	# Use Savitzky-Golay filtering to smooth all IC's in the IM
	im_smooth = savitzky_golay_im(im)
	assert isinstance(im_smooth, IntensityMatrix)
	
	# find the IC for derivatisation product ion before smoothing
	ic = im.get_ic_at_index(73)
	assert isinstance(ic, IonChromatogram)
	
	# find the IC for derivatisation product ion after smoothing
	ic_smooth = im_smooth.get_ic_at_index(73)
	assert isinstance(ic_smooth, IonChromatogram)
	
	# TODO: value assertions
	
	savitzky_golay_im(im, degree=5)
	savitzky_golay_im(im, window=5)
	
	# Test Errors
	
	for type in [test_string, test_int, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			savitzky_golay_im(type)
	
	for type in [test_string, test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			savitzky_golay_im(im, degree=type)
		
	for type in [test_float, test_list_ints, test_list_strs, test_dict]:
		with pytest.raises(TypeError):
			savitzky_golay_im(im, window=type)



