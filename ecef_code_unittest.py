import unittest
import pandas as pd
import numpy as np
import math
from ecef_solution import VelocityCalculator

class TestVelocityCalculator(unittest.TestCase):
    
    def setUp(self):

        # Sample Dataframe using similar values as the CSV file
        self.df = pd.DataFrame({
            'time': [10, 11, 12],
            'latitude': [-20, -25, -30],
            'longitude': [5, 35, 40],
            'altitude': [10, 15, 25],
            'X': [-2160000.0, 4400000.0, 5800000.0],
            'Y': [4600000.0, 2500000.0, 800000.0],
            'Z': [-3700000.0, -3650000.0, -3100000.0]
        })
    
    def test_lla_to_ecef_normal_case(self):

        # Test lla_to_ecef function (lat, long, H (km))
        X, Y, Z = VelocityCalculator.lla_to_ecef(-21, 7, 12)
        self.assertAlmostEqual(X, 11836444, places=0)
        self.assertAlmostEqual(Y, 1453333, places=0)
        self.assertAlmostEqual(Z, -4562399, places=0)

    def test_lla_to_ecef_null(self):

        # Test lla_to_ecef function (lat, long, H (km))
        X, Y, Z = VelocityCalculator.lla_to_ecef(-2, 7, -5)
        self.assertAlmostEqual(X, 12648570, places=0)
        self.assertAlmostEqual(Y, 1553049, places=0)
        self.assertAlmostEqual(Z, -443525, places=0)

    def test_calc_ecef_velocity_normal_case(self):

        # Test calc_ecef_velocity function
        vel_calc = VelocityCalculator(self.df)
        X_velocity, Y_velocity, Z_velocity = vel_calc.calc_ecef_velocity(10.5)
        self.assertAlmostEqual(X_velocity, 6560000, places=0)
        self.assertAlmostEqual(Y_velocity, -2100000, places=0)
        self.assertAlmostEqual(Z_velocity, 50000, places=0)

    def test_calc_ecef_velocity_target_below_earliest(self):

        # Test calc_ecef_velocity when the target time is below the earliest recorded time. Edge case.
        vel_calc = VelocityCalculator(self.df)
        with self.assertRaises(ValueError):
            vel_calc.calc_ecef_velocity(10)

    def test_calc_ecef_velocity_target_above_latest(self):

        # Test calc_ecef_velocity when the target time is above the latest recorded time. Edge case.
        vel_calc = VelocityCalculator(self.df)
        with self.assertRaises(IndexError):
            vel_calc.calc_ecef_velocity(28387474758584984)

    def test_calc_ecef_velocity_target_null(self):

        # Test calc_ecef_velocity null value.
        vel_calc = VelocityCalculator(self.df)
        with self.assertRaises(ValueError):
            vel_calc.calc_ecef_velocity(None)

    def test_calc_ecef_velocity_target_negative(self):

        # Test calc_ecef_velocity negative value.
        vel_calc = VelocityCalculator(self.df)
        with self.assertRaises(ValueError):
            vel_calc.calc_ecef_velocity(-11.99)

if __name__ == '__main__':
    unittest.main()