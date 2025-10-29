import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

import time
from . import line_analysis as la
from . import spectrum_tools as st
from . import dataIO as dio
import numpy as np
import pickle
from .config import DATA_DIR, CONFIG_DIR
import os

def run_pipeline(sources_table,
                source_id_column='source_id',
                xp_continuous_output_file='xp_continuous_downloaded.csv',
                eq_widths_output_file='Test_EqWidths',
                extrema_output_file='Test_Extrema',
                time_stamps=False,
                produce_eq_widths=True,
                config_file='test.xml'):

    """
    Run the XPy-TEAL pipeline to locate spectral lines and (optionally) compute equivalent widths.
    This function orchestrates the end-to-end processing of a list/table of sources:
    - Reads pipeline configuration from an XML file.
    - Ensures XP spectra are downloaded (or reads existing cached output).
    - Builds wavelength/line lists from configured default and user-specified lines.
    - Locates candidate spectral lines (derivative-based search) in parallel.
    - Optionally saves all found extrema to a pickle file.
    - Optionally computes equivalent widths for the requested wavelengths and lines,
        produces a pandas DataFrame of results, and can write that DataFrame to disk
        in CSV format (other formats may be added).
    Parameters
    ----------
    sources_table : object
            Source specification to feed to the downloader. This may be a path, a table-like
            object, or any input accepted by st.download_xp_spectra_if_needed that identifies
            which sources to download/analyze.
    source_id_column : str, optional
            Column name in sources_table used as the unique source identifier (default: 'source_id').
    xp_continuous_output_file : str, optional
            Path (including filename) for the local cached spectra file used by the downloader
            (default: DATA_DIR/'xp_continuous_downloaded.csv').
    eq_widths_output_file : str, optional
            Base filename (without extension) used when saving equivalent-width results
            to disk under the DATA_DIR (default: DATA_DIR/'Test_EqWidths').
    extrema_output_file : str, optional
            Base filename (without extension) used when saving extrema information as a pickle
            under the DATA_DIR (default: DATA_DIR/'Test_Extrema').
    time_stamps : bool, optional
            If True, print timing information for major pipeline stages to stdout (default: False).
    produce_eq_widths : bool, optional
            If True, run the equivalent-width calculation step; if False, skip it and return None
            for RESULT (default: True).
    config_file : str, optional
            Path to the pipeline XML configuration file used to set runtime options such as
            number of cores, output format, and which lines to analyze (default: DATA_DIR/'test.xml').
    Returns
    -------
    pandas.DataFrame or None
            If produce_eq_widths is True, returns a pandas.DataFrame containing equivalent-width
            measurements (and related metadata) for the requested lines and sources. If
            produce_eq_widths is False, returns None.
    Side effects
    ------------
    - Reads configuration via dio.read_xml(config_file).
    - Downloads or reads XP spectra, using st.download_xp_spectra_if_needed and writes the
        downloaded cache to xp_continuous_output_file as needed.
    - Writes extrema data to DATA_DIR/<extrema_output_file>.pkl if enabled in the config.
    - Writes equivalent-width results to DATA_DIR/<eq_widths_output_file>.<ext> when the
        configuration requests it; currently CSV output is supported.
    - Prints progress and timing information to stdout when time_stamps is True.
    - Uses parallel computation for line-finding (n_cores from configuration).
    - Deletes the internal LINE_DICT before returning.
    Notes
    -----
    - The function relies on external modules/functions (dio, st, la, numpy, pickle) to
        perform the actual IO, line detection and analysis; exceptions raised by those
        routines propagate to the caller.
    - The XML configuration determines flags such as 'output_format', 'provide_all_extrema',
        'provide_equivalent_widths', and 'number_of_cores'. Only CSV output is currently
        implemented for saving equivalent-width results in this function.
    - File paths printed in messages are relative to the working directory; ensure the
        DATA_DIR exists and is writable.
    """


    if time_stamps:
        print("Starting XPy-TEAL pipeline...")
        t1 = time.time()

    user_input = dio.read_xml(DATA_DIR/config_file)

    t = st.download_xp_spectra_if_needed(sources_table,
                                        source_id_column=source_id_column,
                                        output_file=xp_continuous_output_file)
    
    print('Number of sources to analyse: ', len(t))

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
    print('Total number of lines to analyse: ', len(LINE_NAMES))

    if time_stamps:
        t2 = time.time()
        print("Time to read/download data and set up parameters: ", t2-t1)

    LINE_DICT = la.getLinesInDeriv_parallel(datalink=t,
                                            n_cores=n_cores)
    
    if time_stamps:
        t3 = time.time()
        print("Time to get lines in derivative: ", t3-t2)

    if provide_all_extrema_flag:
        extrema_path = os.path.join(DATA_DIR, extrema_output_file + '.pkl')
        print("Saving all extrema information to file " + extrema_path)
        with open(extrema_path, 'wb') as f:
            pickle.dump(LINE_DICT, f)

    if produce_eq_widths:

        RESULT = la.analyseLine_all_wavelengths(datalink=t,WAVELENGTH_LIST=wavelength_list,
                                                LINE_NAMES=LINE_NAMES, LINE_DICT=LINE_DICT,
                                                k = K, ncores=n_cores)
        
        RESULT = la.make_output_dataframe(RESULT, LINE_NAMES)

        if time_stamps:
            t4 = time.time()
            print("Time to get equivalent widths: ", t4-t3)

        if provide_eq_widths_flag:
            out_path = os.path.join(DATA_DIR, eq_widths_output_file + "." + output_format)
            print("Saving equivalent widths to file " + out_path)
            if output_format == 'csv':
                RESULT.to_csv(os.path.join(DATA_DIR, eq_widths_output_file + '.csv'), index=False)
            
            # it will be the fastest to write to parquet
            # elif output_format == 'parquet':
            #     RESULT.to_parquet(os.path.join(DATA_DIR, eq_widths_output_file + '.parquet'), index=False)


    else:
        print("Skipping equivalent width calculations as per user request.")
        RESULT = None

    del LINE_DICT

    return RESULT