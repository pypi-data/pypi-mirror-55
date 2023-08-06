# from dplus.DataModels import Constraints, Parameter
# from dplus.State import State, DomainPreferences, FittingPreferences
from dplus.Amplitudes import Amplitude, sph2cart
#from dplus.DataModels.models import UniformHollowCylinder
#from dplus.CalculationInput import CalculationInput
#from dplus.DataModels import ModelFactory, Population
from dplus.State import State
from math import pi
import numpy as np

exe_directory = r"C:\Users\chana\Sources\dplus\dplus-dev\x64\Release"
sess_dir = r"C:\Users\chana\Sources\dplus\for_dplus\testDplus\session"
state_file = r"C:\Users\chana\Sources\dplus\for_dplus\testDplus\session\aa.state"

from dplus.CalculationInput import CalculationInput
from dplus.CalculationRunner import LocalRunner

runner= LocalRunner(exe_directory, sess_dir)

# input=CalculationInput.load_from_state_file(state_file)
# result=runner.fit(input)
# print(result.graph)

input = CalculationInput.load_from_state_file(r"C:\Users\chana\Sources\dplus\for_dplus\testDplus\check_use_grid.state")
# #cylinder = input.get_model(7)
runner = LocalRunner(exe_directory, sess_dir)
input.Domain.Children[0].Children[0].Children[1].Children[0].use_grid = False
# #print("Original radius is ", cylinder.layer_params[1]['Radius'].value)
result = runner.generate(input)
pass

# def my_func(x, y, z):
# 	return np.complex64(x + y + z +x*1j)
#
# my_amp = Amplitude.load(r"C:\Users\chana\Sources\dplus\for_dplus\testDplus\sphere.ampj")
# my_amp_new = Amplitude(80,7.5)
# my_amp_new.fill(my_func)


#
# input.signal = result.signal
# cylinder = input.get_model(7)
# cylinder.layer_params[1]['Radius'].value = 2
# cylinder.layer_params[1]['Radius'].mutable = True
# input.FittingPreferences.convergence = 0.5
# input.use_gpu = True
# fit_result = runner.fit(input)
# optimized_input= fit_result.result_state
# result_cylinder=optimized_input.get_model(7)
# print(fit_result.parameter_tree)
# print("Result radius is ", result_cylinder.layer_params[1]['Radius'].value)

# input=CalculationInput.load_from_state_file(r"C:\Users\chana\Desktop\testDplus\aa.state")
# result=runner.fit(input)
# print(result.graph)

