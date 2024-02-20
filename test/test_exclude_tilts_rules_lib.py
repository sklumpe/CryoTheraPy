import unittest
import sys
import os
import pandas as pd
from pandas.testing import assert_frame_equal
import tempfile

current_dir = os.path.dirname(os.path.abspath(__name__))
root_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(root_dir)

from src.lib.exclude_tilts.exclude_tilts_rules_lib import col_of_df_to_series, series_higher_lower, combine_vectors, remove_tilts

class test_exclude_tilts_rules_lib_function_(unittest.TestCase):
    def test_(self):
        pass


"""
    looks into the ctf.star (already as df) and write a list of the Position_x_y.star files which have
    the parameters --> can use for list comprehension and call the other functions in that loop!
"""
class test_exclude_tilts_rules_lib_function_col_of_df_to_series(unittest.TestCase):
    def create_test_ctf_star_df(self):
        self.ctf_star_df = pd.DataFrame(
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
            "rlnVoltage": [
                "300.000000",
                "300.000000",
                "300.000000",
                ],
            "rlnSphericalAberration": [
                "2.700000",
                "2.700000",
                "2.700000",
                ],
            "rlnAmplitudeContrast": [
                "0.100000",
                "0.100000",
                "0.100000",
                ],
            "rlnMicrographOriginalPixelSize": [
                "2.930000",
                "2.930000",
                "2.930000",
                ],
            "rlnTomoHand": [
                "1.000000",
                "1.000000",
                "1.000000",
                ],
            "rlnTomoTiltSeriesPixelSize": [
                "2.930000",
                "2.930000",
                "2.930000",
                ]
            }
        )

    def test_col_of_df_to_series(self):
        self.create_test_ctf_star_df()
        self.series_tilts_star = col_of_df_to_series(self.ctf_star_df, "rlnTomoTiltSeriesStarFile")
        self.assertIsInstance(self.series_tilts_star, pd.Series, "Returned object is not a list")
        self.assertIn("CtfFind/job003/tilt_series/Position_1.star", self.series_tilts_star.values, "Position_1.star was not added")
        self.assertIn("CtfFind/job003/tilt_series/Position_2.star", self.series_tilts_star.values, "Position_2.star was not added")
        self.assertIn("CtfFind/job003/tilt_series/Position_10.star", self.series_tilts_star.values, "Position_10.star was not added")


class test_exclude_tilts_rules_lib_function_series_higher_lower(unittest.TestCase):
    def create_test_series_and_range(self):
        self.test_series = pd.Series(["9.260247", "8.772866", "5.123456", "7.012345", "4.234567", "5.543210", "8.765432", "9.321098", "6.888888", "9.101010"])
        self.test_range = (5.5, 9.2)
        self.expected_series = pd.Series([0, 1, 0, 1, 0, 1, 1, 0, 1, 1])

    def test_series_higher_lower(self):
        self.create_test_series_and_range()
        self.ser_0_1 = series_higher_lower(self.test_series, self.test_range)
        pd.testing.assert_series_equal(self.ser_0_1, self.expected_series, "Entries are not properly excluded based on range")


class test_exclude_tilts_rules_lib_function_combine_vectors(unittest.TestCase):
    def create_test_vectors(self):
        """
        create 3 vectors that resembles the vectors from the vect_higher_lowe function (= 1 --> low cut-off < value < high cut-off, else 0).
        """
        self.vector_a = pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1])
        self.vector_b = pd.Series([1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1])
        self.vector_c = pd.Series([1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1])
        self.df_vecs = pd.DataFrame({"a": self.vector_a, "b": self.vector_b, "c": self.vector_c})
        self.expected_vector = pd.Index([0, 2, 3, 5, 7, 9, 10, 11, 14, 15, 16, 18, 19]) # = indices where all vectors are 1

    def test_combine_vectors(self):
        self.create_test_vectors()
        self.test_vector = combine_vectors(self.df_vecs)
        pd.testing.assert_index_equal(self.test_vector, self.expected_vector, "The indices of the produces vector are not the expected indices")


class test_exclude_tilts_rules_lib_function_remove_tilts(unittest.TestCase):
    def create_test_file(self):
        # Create a test df
        self.test_df = pd.DataFrame({
            "rlnMicrographMovieName": ["frames_schemes/Position_10_001_-10.00_20231020_224112_EER.eer",
                                    "frames_schemes/Position_10_002_-12.00_20231020_224136_EER.eer",
                                    "frames_schemes/Position_10_003_-10.00_20231020_224112_EER.eer",
                                    "frames_schemes/Position_10_004_-12.00_20231020_224136_EER.eer",
                                    "frames_schemes/Position_10_005_-10.00_20231020_224112_EER.eer",
                                    "frames_schemes/Position_10_006_-12.00_20231020_224136_EER.eer",
                                    "frames_schemes/Position_10_007_-10.00_20231020_224112_EER.eer",
                                    "frames_schemes/Position_10_008_-12.00_20231020_224136_EER.eer",
                                    "frames_schemes/Position_10_009_-10.00_20231020_224112_EER.eer",
                                    "frames_schemes/Position_10_010_-12.00_20231020_224136_EER.eer"],
            "rlnTomoTiltMovieFrameCount": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            "rlnTomoNominalStageTiltAngle": [-10.0, -11.99, -10.0, -11.99, -10.0, -11.99, -10.0, -11.99, -10.0, -11.99],
            "rlnTomoNominalTiltAxisAngle": [-95.0, -95.0, -95.0, -95.0, -95.0, -95.0, -95.0, -95.0, -95.0, -95.0],
            "rlnMicrographPreExposure": [0.0, 3.0, 0.0, 3.0, 0.0, 3.0, 0.0, 3.0, 0.0, 3.0],
            "rlnTomoNominalDefocus": [-2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0],
            "rlnCtfPowerSpectrum": ["MotionCorr/job002/frames_schemes/Position_10_001_-10_00_20231020_224112_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_002_-12_00_20231020_224136_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_003_-10_00_20231020_224112_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_004_-12_00_20231020_224136_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_005_-10_00_20231020_224112_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_006_-12_00_20231020_224136_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_007_-10_00_20231020_224112_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_008_-12_00_20231020_224136_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_009_-10_00_20231020_224112_EER_PS.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_010_-12_00_20231020_224136_EER_PS.mrc"],
            "rlnMicrographNameEven": ["MotionCorr/job002/frames_schemes/Position_10_001_-10_00_20231020_224112_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_002_-12_00_20231020_224136_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_003_-10_00_20231020_224112_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_004_-12_00_20231020_224136_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_005_-10_00_20231020_224112_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_006_-12_00_20231020_224136_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_007_-10_00_20231020_224112_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_008_-12_00_20231020_224136_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_009_-10_00_20231020_224112_EER_EVN.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_010_-12_00_20231020_224136_EER_EVN.mrc"],
            "rlnMicrographNameOdd": ["MotionCorr/job002/frames_schemes/Position_10_001_-10_00_20231020_224112_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_002_-12_00_20231020_224136_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_003_-10_00_20231020_224112_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_004_-12_00_20231020_224136_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_005_-10_00_20231020_224112_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_006_-12_00_20231020_224136_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_007_-10_00_20231020_224112_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_008_-12_00_20231020_224136_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_009_-10_00_20231020_224112_EER_ODD.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_010_-12_00_20231020_224136_EER_ODD.mrc"],
            "rlnMicrographName": ["MotionCorr/job002/frames_schemes/Position_10_001_-10_00_20231020_224112_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_002_-12_00_20231020_224136_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_003_-10_00_20231020_224112_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_004_-12_00_20231020_224136_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_005_-10_00_20231020_224112_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_006_-12_00_20231020_224136_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_007_-10_00_20231020_224112_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_008_-12_00_20231020_224136_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_009_-10_00_20231020_224112_EER.mrc",
                                    "MotionCorr/job002/frames_schemes/Position_10_010_-12_00_20231020_224136_EER.mrc"],
            "rlnMicrographMetadata": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "rlnAccumMotionTotal": [4.455545, 4.54099, 4.455545, 4.54099, 4.455545, 4.54099, 4.455545, 4.54099, 4.455545, 4.54099],
            "rlnAccumMotionEarly": [2.691712, 0.0, 2.691712, 0.0, 2.691712, 0.0, 2.691712, 0.0, 2.691712, 0.0],
            "rlnAccumMotionLate": [1.763833, 4.54099, 1.763833, 4.54099, 1.763833, 4.54099, 1.763833, 4.54099, 1.763833, 4.54099],
            "rlnCtfImage": ["CtfFind/job003/frames_schemes/Position_10_001_-10_00_20231020_224112_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_002_-12_00_20231020_224136_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_003_-10_00_20231020_224112_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_004_-12_00_20231020_224136_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_005_-10_00_20231020_224112_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_006_-12_00_20231020_224136_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_007_-10_00_20231020_224112_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_008_-12_00_20231020_224136_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_009_-10_00_20231020_224112_EER_PS.ctf:mrc",
                            "CtfFind/job003/frames_schemes/Position_10_010_-12_00_20231020_224136_EER_PS.ctf:mrc"],
            "rlnDefocusU": [18638.144531, 19790.931641, 18638.144531, 19790.931641, 18638.144531, 19790.931641, 18638.144531, 19790.931641, 18638.144531, 19790.931641],
            "rlnDefocusV": [18638.144531, 19531.273438, 18638.144531, 19531.273438, 18638.144531, 19531.273438, 18638.144531, 19531.273438, 18638.144531, 19531.273438],
            "rlnCtfAstigmatism": [0.0, 259.658203, 0.0, 259.658203, 0.0, 259.658203, 0.0, 259.658203, 0.0, 259.658203],
            "rlnDefocusAngle": [21.683119, 63.377064, 21.683119, 63.377064, 21.683119, 63.377064, 21.683119, 63.377064, 21.683119, 63.377064],
            "rlnCtfFigureOfMerit": [0.013286, 0.015763, 0.013286, 0.015763, 0.013286, 0.015763, 0.013286, 0.015763, 0.013286, 0.015763],
            "rlnCtfMaxResolution": [9.260247, 8.772866, 9.260247, 8.772866, 9.260247, 8.772866, 9.260247, 8.772866, 9.260247, 8.772866]
        })

        self.vect_indices_keep = [0, 2, 3, 6, 7, 9]

        self.expected_df = pd.DataFrame(index = range(len(self.vect_indices_keep)), columns = self.test_df.columns)
        self.expected_df.iloc[0] = self.test_df.iloc[0]
        self.expected_df.iloc[1] = self.test_df.iloc[2]
        self.expected_df.iloc[2] = self.test_df.iloc[3]
        self.expected_df.iloc[3] = self.test_df.iloc[6]
        self.expected_df.iloc[4] = self.test_df.iloc[7]
        self.expected_df.iloc[5] = self.test_df.iloc[9]


    def test_remove_tilts(self):
        self.create_test_file()
        self.after_func_df = remove_tilts(self.test_df, self.vect_indices_keep)
        for index, row in self.expected_df.iterrows():
            assert row.to_dict() in self.test_df.to_dict("records"), "expected_df was not constructed properly, test invalid"
        pd.testing.assert_frame_equal(self.after_func_df, self.expected_df, "The entries were not removed as expected")




