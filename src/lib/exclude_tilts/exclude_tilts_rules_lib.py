# functions for the exclude tilts rules file
import os
import sys
import pandas as pd


def col_of_df_to_series(star_df, param):
    """
    looks into the ctf.star (already as df) and writes a list of the tilt_series star files containing the parameters.

    Args:
        star_df (pd.Dataframe): df of the contents of the tilt-series_ctf.star, containing the paths to the
        .star files of the individual tilts under "rlnTomoTiltSeriesStarFile".
        param (str): column label of df.
    
    Returns:
        series_of_param_values (pd.Series): pd.Series of the entries of star_df under param.
    
    Example:
    tilt_series_ctf_star_df = pd.DataFrame(
        {"rlnTomoName": [
            "Position_1", 
            "Position_2", 
            "Position_10",
            ], 
        "rlnTomoTiltSeriesStarFile": [
            "CtfFind/job003/tilt_series/Position_1.star",
            "CtfFind/job003/tilt_series/Position_2.star",
            "CtfFind/job003/tilt_series/Position_10.star",
            ],
            )
    
    The function will return: [
            "CtfFind/job003/tilt_series/Position_1.star",
            "CtfFind/job003/tilt_series/Position_2.star",
            "CtfFind/job003/tilt_series/Position_10.star",
            ]
    """
    series_of_param_values = pd.Series(star_df[param])
    return series_of_param_values


def series_higher_lower(series_of_values, range:tuple):
    """
    run through the entries of the given pd.Series and write a new vector of the same length. For this new
    vector, write 1 if the value is within the range, otherwise write 0.

    Args:
        series_of_values (pd.Series): series of values that should be tested.
        range (tubple): range as a cut-off where range[0] is the lower cut-off and range[1] the higher cut-off.
    
    Returns:
        higher_lower_series (pd.Series): series of 0s and 1s (0 = value was outside of range, 1 = value was inside).

    Example:
        series_of_values = pd.Series([1, 2, 3, 4, 5])
        range_ = (2, 4)

        The function will create a new pd.Series with the length 5, populated by 0. Then, it will iterate through the
        entries of the series_of_values and test whether it is true that they are >= 2 and <= 4 also ensures that the 
        entries are floats). If yes, True is saved, if not, False. Lastly, the newly created series will be set to 1 
        everywhere where the boolean is True and returned. 
    """
    higher_lower_series = pd.Series(0, index = series_of_values.index)
    mask_of_booleans = (series_of_values.astype(float) >= range[0]) & (series_of_values.astype(float) <= range[1])
    higher_lower_series[mask_of_booleans] = 1
    return higher_lower_series


def combine_vectors(df_0_1):
    """
    take a df of all pd.Series together created in series_higher_lower (one for each pparam) and find the indices
    where all vectors are 1.

    Args:
        df_0_1 (pd.Dataframe): a dataframe containing series of 0s and 1s, where 0s mean that a value at that index
        should be removed in future steps.

    Returns:
        indices_true (pd.Index): index object containing all indices where all series in the df are 1.

    Example:
        df_0_1 = pd.DataFrame({"a": vector_a, "b":vector_b, "c": vector_c})
        (with: 
        vector_a = pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        vector_b = pd.Series([1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        vector_c = pd.Series([1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1])
        )

        The function will create a pd.Series containing True where all rows (axis = 1) of df_0_1 are 1, and False
        if they do not. Then, it will get (and return) the indeces of df_0_1 where all_ones_df is True. In this case,
        pd.Index([0, 2, 3, 5, 7, 9, 10, 11, 14, 15, 16, 18, 19]) would be returned.
    """
    all_ones_df = (df_0_1 == 1).all(axis=1)
    # Find the indices where all values are 1
    indices_true = df_0_1.index[all_ones_df]
    return indices_true


def remove_tilts(star_file_df, indices_keep_tilts):
    """
    write a new df with only the entries of the all 1 indices_vector
    """
    new_df = pd.DataFrame(index = range(len(indices_keep_tilts)), columns = star_file_df.columns)
    i = 0
    for index in indices_keep_tilts:
        new_df.loc[i] = star_file_df.loc[index]
        i += 1
    return new_df

