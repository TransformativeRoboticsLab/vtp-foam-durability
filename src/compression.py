# VTP Compression Durability Analysis
import pandas as pd
import matplotlib.pyplot as plt


def load_file():
    # Given csv filename, get database
    file_path = '../data/pack_foam_sample_001_20250305_1.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_path, skiprows=2)
    # Check the data
    print(df.head())
    # Convert columns to plottable data types
    col1 = df.iloc[:, 0].astype(float)  # First column as floats
    col2 = df.iloc[:, 1].astype(float)  # Second column as floats
    col3 = df.iloc[:, 2].astype(float)  # Third column as floats
    # Take every 515th row and save to a list
    sampled_rows = df.iloc[::515].astype(float)
    print("Sampled rows:", sampled_rows)

    return col1, col2, col3, sampled_rows


def plot_all_compression_data(col1, col2, col3):
    plt.figure(figsize=(8, 6))
    print(type(col2))
    plt.plot(col2[:1000], col3[:1000])
    plt.xlim([-15, 0])
    plt.ylim([-0.2, 0])
    plt.legend()
    plt.grid()
    plt.xlabel('Deformation [mm]')
    plt.ylabel('Force [kN]')
    plt.title('Plot of Initial Compression Cycles - Expanded Polyurethane 30 mm cube 2025/03/04')
    plt.show()

def plot_zoomed_compression_data(col1, col2, col3):
    plt.figure(figsize=(8, 6))
    plt.plot(col2, col3)
    plt.xlim([-14, -13.2])
    plt.ylim([-0.038, -0.03])
    plt.legend()
    plt.grid()
    plt.xlabel('Deformation [mm]')
    plt.ylabel('Force [kN]')
    plt.title('Plot of 1000 Compression Cycles - 0.5 MPa 30 mm Cube VTP 2025/03/04')
    plt.show()


def plot_specific_compression_data(deformation_col, force_col):
    plt.figure(figsize=(8, 6))
    plt.plot(deformation_col, force_col)
    plt.legend()
    plt.xlabel('Deformation')
    plt.ylabel('Force')
    plt.title('Deformation vs Force')
    plt.show()


if __name__ == '__main__':
    col1, col2, col3, s_rows = load_file()
    plot_all_compression_data(col1, col2, col3)
    # plot_zoomed_compression_data(col1, col2, col3)
    s_col1 = s_rows.iloc[:, 1].astype(float)
    s_col2 = s_rows.iloc[:, 2].astype(float)
    print(type(s_rows))
    print(s_rows)
    # plot_specific_compression_data(s_col1, s_col2)