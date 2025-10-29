import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import time
from . import line_analysis as la
from . import spectrum_tools as st
from . import math_tools as mt
from . import dataIO as dio
import numpy as np
import pandas as pd
import pickle
import importlib
importlib.reload(la)
importlib.reload(st)



def main():

    t1 = time.time()

    user_input = dio.read_xml('../Data/test.xml')

    t = pd.read_csv('../Data/xp_continuous_test.csv')
    t = st.process_data(t)

    #output_file_names

    file = "Test_EqWidths"
    extremaFile = "Test_Extrema"
    output_format = user_input['output_format']
    provide_all_extrema_flag = user_input['provide_all_extrema']
    provide_eq_widths_flag = user_input['provide_equivalent_widths']


    # general parameters:
    K = 2 # the order for local de-convolution
    n_cores = int(user_input['number_of_cores'])

    default_line_wavelengths = la.get_default_line_wavelengths(user_input['list_of_default_lines'])
    requested_lines = la.get_list_of_wavelegths(user_input['list_of_line_wavelengths'])

    wavelength_list = default_line_wavelengths + requested_lines
    wavelength_list = np.array(wavelength_list)

    LINE_NAMES = la.getLineNames(user_input['list_of_default_lines'], 
                                    user_input['list_of_line_wavelengths'])


    t2 = time.time()

    print("Time to read data and set up parameters: ", t2-t1)

    LINE_DICT = la.getLinesInDeriv_parallel(datalink=t,
                                            n_cores=n_cores)

    t3 = time.time()

    print("Time to get lines in derivative: ", t3-t2)


    RESULT = la.analyseLine_all_wavelengths(datalink=t,WAVELENGTH_LIST=wavelength_list,
                                            LINE_NAMES=LINE_NAMES, LINE_DICT=LINE_DICT,
                                            k = K, ncores=n_cores)


    t4 = time.time()

    print("Time to get results: ", t4-t3)

    RESULT = la.make_output_dataframe(RESULT, LINE_NAMES)

    if provide_eq_widths_flag:
        if output_format == 'csv':
            RESULT.to_csv('../Data/'+file+'.csv', index=False)


        # it will be the fastest to write to parquet
        elif output_format == 'parquet':
            RESULT.to_parquet('../Data/'+file+'.parquet', index=False)

    t5 = time.time()

    if provide_all_extrema_flag:
        with open('../Data/'+extremaFile+'.pkl', 'wb') as f:
            pickle.dump(LINE_DICT, f)


    print("Time to write results: ", t5-t4)

    print("Total time: ", t5-t1)

    return RESULT

if __name__ == "__main__":
    RESULT = main()