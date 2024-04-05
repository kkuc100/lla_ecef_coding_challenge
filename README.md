# lla_ecef_coding_challenge
Calculation & Interpolation of ECEF Velocities

Python: 3.10.1

Overview:

This script is designed to perform calculations related to Earth-Centered, Earth-Fixed (ECEF) coordinates and velocities based on latitude, longitude, altitude (LLA) data provided in a CSV file. It provides functions to convert LLA coordinates to ECEF coordinates and to calculate ECEF velocities at specified target times.

Dependencies:

Use a package manager of choice to install the following:

- pandas: 2.1.0 (`pip install pandas==2.1.0`)
- numpy: 1.23.3 (`pip install numpy==1.23.3`)
- math: No specific version needed

Usage:

1. Ensure that the required dependencies are installed (`pandas`, `numpy`, `math`).
2. Load the CSV file containing LLA data using `pd.read_csv()` and specify the appropriate column names.
3. Call the `LLA_to_ECEF()` function to convert LLA coordinates to ECEF coordinates.
4. Concatenate the ECEF coordinates with the original DataFrame to maintain the time column.
5. Sort the DataFrame by the time column in preparation for velocity calculations.
6. Call the `Calc_ECEF_velocity()` function with a list of target times to calculate ECEF velocities at those times.

A Makefile is provided to automate common tasks related to the project. Here are the available commands:

- Install Make: If make is not installed, you'll need to install it.
make test: Executes unit tests using unittest to ensure code functionality.
make run: Executes the main script, allowing users to run the script without needing to remember the command-line arguments.

Functions:

LLA_to_ECEF(latitude, longitude, H):

**Parameters:**
- `latitude`: Latitude in degrees.
- `longitude`: Longitude in degrees.
- `H`: Altitude in kilometers.

**Returns:**
- Tuple `(X, Y, Z)` representing ECEF coordinates.

Calc_ECEF_velocity(target_time):

**Parameters:**
- `target_time`: List of target times for which velocities are to be calculated.

**Returns:**
- Velocities along X, Y, and Z axes at the specified target times.

Important Notes:

- Ensure that the input CSV file contains the necessary columns (`time`, `latitude`, `longitude`, `altitude`) in the correct format.
- The Altitude in the `LLA_to_ECEF` function is converted from kilometers to meters.
- Velocities at the first input point are assumed to be 0, as per the provided Code Challenge Instructions.
- Velocities at times that don't coincide with points in the input file are calculated by linearly interpolating velocities calculated for input points.

Output:

kevinkuc@Kevins-MacBook-Air Kuc_ecef coding challenge ver_3 % make run
python3 ecef_solution.py
The 1532334000 point velocity vector is: X velocity: -1871.83 m/s, The Y velocity: -4027 m/s, The Z velocity: -247.28 m/s
The 1532335268 point velocity vector is: X velocity: -5631.55 m/s, The Y velocity: -70.81 m/s, The Z velocity: -6143.92 m/s
kevinkuc@Kevins-MacBook-Air Kuc_ecef coding challenge ver_3 % make test
python3 ecef_code_unittest.py
.......
----------------------------------------------------------------------
Ran 7 tests in 0.007s

OK