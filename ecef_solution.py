import pandas as pd
import numpy as np
import math

class VelocityCalculator:

    def __init__(self, dataframe):
        self.df = dataframe.sort_values('time')

    @staticmethod
    def __calc_velocity_vec(start_time_data, end_time_data):
        """
        Calculate vector velocity.
        """
        time_diff = end_time_data['time'] - start_time_data['time']
        X_velocity = (end_time_data['X'] - start_time_data['X'])/(time_diff)
        Y_velocity = (end_time_data['Y'] - start_time_data['Y'])/(time_diff)
        Z_velocity = (end_time_data['Z'] - start_time_data['Z'])/(time_diff)
        return X_velocity,Y_velocity,Z_velocity

    @staticmethod
    def lla_to_ecef(latitude, longitude, H):
        """
        Convert Latitude, Longitude, Altitude to ECEF coordinates. Latitude is in degrees, Longitude is in degrees, Altitude is in kilometers
        """
        #WGS84 Parameters
        a = 6378137
        b = 6356752.31424518

        #Convert degree to radians
        latitude_rad = math.radians(latitude)
        longitude_rad = math.radians(longitude)
        
        # Calculate eccentricity
        e = math.sqrt((a**2 - b**2)/a**2)

        # Radius of Curvature(meters)
        N = (a/math.sqrt(1-(e**2)*math.sin(latitude_rad)**2))

        # Calculate ellipsoidal height, N is in meters, H is in kilometers, * 1000 to convert to meters
        h = H * 1000 + N
        # The height unit is now in meters

        # Convert to ECEF coordinates
        X = (N + h)*math.cos(latitude_rad)*math.cos(longitude_rad)
        Y = (N + h)*math.cos(latitude_rad)*math.sin(longitude_rad)
        Z = ((b**2 / a**2) * N + h) * math.sin(latitude_rad)
        return X,Y,Z

    def calc_ecef_velocity(self, target_time):
        """
        Calculate ECEF velocity at a specific time.
        """
        df = self.df
        # Find the closest time values above and below the target time
        # Extract rows where time values exceed the target time
        above_time_rows = df.loc[df['time'] > target_time]
        below_time_rows = df.loc[df['time'] < target_time]
        
        if len(below_time_rows) <= 0:
            raise ValueError("Target time is below the earliest recorded time.")

        above_time_row = df.loc[above_time_rows.index[0]]
        below_time_row = df.loc[below_time_rows.index[-1]]
        
        return self.__calc_velocity_vec(above_time_row, below_time_row)


if __name__ == "__main__":

    # Load the CSV file
    df_raw = pd.read_csv('lla_code_problem_data.csv', header=None)
    #Namin the columns as they were unnamed in the CSV file
    df_raw.columns = ["time", "latitude", "longitude","altitude"]

    # Creates a series of ECEF data and passes it to df_ECEF.Using the lla_to_ecef function to get the X,Y,Z
    ecef_series = df_raw.apply(lambda row: VelocityCalculator.lla_to_ecef(row['latitude'], row['longitude'], row['altitude']), axis=1)
    df_ecef = pd.DataFrame(ecef_series.tolist(), columns=['X', 'Y', 'Z'])

    # Adds the ECEF_df to the original df to keep the time column. At this point we have the
    # original data, aka lat, long, time, altitude, along with X, Y, Z
    df_lla_ecef = pd.concat([df_raw, df_ecef], axis=1)

    # Instantiate VelocityCalculator which sorts the df based off of time
    vel_calc = VelocityCalculator(df_lla_ecef)

    #Input parameters given in the instructions
    time_1 = 1532334000
    time_2 = 1532335268

    # calculating the velocity at each time period
    velocities_1 = vel_calc.calc_ecef_velocity(time_1)
    velocities_2 = vel_calc.calc_ecef_velocity(time_2)

    print(f'The {time_1} point velocity vector is: X velocity: {round(velocities_1[0],2)} m/s, The Y velocity: {round(velocities_1[1])} m/s, The Z velocity: {round(velocities_1[2],2)} m/s')
    print(f'The {time_2} point velocity vector is: X velocity: {round(velocities_2[0],2)} m/s, The Y velocity: {round(velocities_2[1],2)} m/s, The Z velocity: {round(velocities_2[2],2)} m/s')
