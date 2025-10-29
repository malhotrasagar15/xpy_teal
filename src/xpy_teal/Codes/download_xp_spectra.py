from astroquery.gaia import Gaia
import pandas as pd
import numpy as np
import getpass
from .config import DATA_DIR

def download_xp_spectra(source_id_table, data_release='Gaia DR3',
                        source_id_column='source_id',
                        gaia_class=None,
                        retrieval_type='XP_CONTINUOUS',
                        format_type='csv',
                        data_structure='RAW', output_file = None):
  """
  Download XP spectra metadata (datalink) for a list of Gaia source_ids.

  Parameters
  ----------
  source_id_table : pandas.DataFrame
    Table or DataFrame that contains Gaia source identifiers. Must contain
    a column named by `source_id_column`.
  data_release : str, optional
    Gaia data release to query (default: 'Gaia DR3').
  source_id_column : str, optional
    Name of the column in `source_id_table` that holds Gaia source IDs
    (default: 'source_id').
  gaia_class : module or class-like object, optional
    Object that exposes the same interface as astroquery.gaia.Gaia:
    - .load_data(ids=..., data_release=..., retrieval_type=..., data_structure=..., format=..., verbose=...)
    - .login(user=..., password=...)
    If None (default), the function will use the Gaia object from
    astroquery.gaia and will prompt for credentials when retrieving large
    numbers of IDs (>= 2000).
  retrieval_type : str, optional
    Retrieval type passed to Gaia.load_data (default: 'XP_CONTINUOUS').
  format_type : {'csv', 'parquet'}, optional
    Output file format to write `output_file` if provided. Only affects
    writing; the internal call to Gaia.load_data currently requests CSV
    and the returned datalink is converted to a pandas.DataFrame.
    Default is 'csv'.
  data_structure : str, optional
    Data structure parameter passed to Gaia.load_data (default: 'RAW').
  output_file : str or pathlib.Path, optional
    If provided, the retrieved datalink table will be saved to this path
    using the format specified by `format_type`. If None (default) no file
    is written.

  Returns
  -------
  pandas.DataFrame
    A DataFrame built from the datalink entry returned by Gaia.load_data
    for the requested source IDs. The exact columns depend on the Gaia
    datalink response and the chosen retrieval options.

  Notes
  -----
  - For large requests (>= 2000 source IDs) the function prompts interactively
    for Gaia credentials and calls `gaia_class.login(user, password)`.
  - The function sets `gaia_class.ROW_LIMIT = -1` to allow unbounded row
    retrieval; this mutates the provided `gaia_class`.
  - The function extracts the first key and first element of the datalink
    response and converts it to a pandas.DataFrame.
  - If `output_file` is provided and `format_type` is 'csv' or 'parquet', the
    DataFrame will be written to disk. Other values for `format_type` are
    not supported and will result in no file being written.

  Raises
  ------
  KeyError
    If `source_id_column` is not present in `source_id_table`.
  ValueError
    If an unsupported `format_type` is provided when attempting to write
    `output_file`.
  RuntimeError / various network exceptions
    Errors raised by the underlying Gaia client when authentication or
    data retrieval fails.

  Example
  -------
  >>> # Using a pandas DataFrame `df` with a 'source_id' column:
  >>> dl = download_xp_spectra(df, data_release='Gaia DR3', output_file='datalink.csv')
  """
  if gaia_class is None:
    gaia_class = Gaia
    if len(source_id_table) >= 2000:
      print('Log in to Gaia archive required for large data retrieval...')
      user = input('Enter your username: ')
      password = getpass.getpass('Password: ')
      gaia_class.login(user=user, password=password)

      del user
      del password

  gaia_class.ROW_LIMIT = -1

  datalink = Gaia.load_data(ids=source_id_table[source_id_column].tolist(),
          data_release=data_release,
                      retrieval_type=retrieval_type,
            data_structure=data_structure,
            format='csv',
            verbose=False
  )
  # get the first key of the datalink dictionary
  datalink = datalink[list(datalink.keys())[0]][0]
  datalink = datalink.to_pandas()

  if output_file is not None:
    if format_type == 'csv':
      datalink.to_csv(output_file, index=False)
    elif format_type == 'parquet':
      datalink.to_parquet(output_file, index=False)
  return datalink

