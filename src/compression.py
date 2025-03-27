# VTP Compression Durability Analysis
import pandas as pd
import matplotlib.pyplot as plt


def load_file():
    # Given csv filename, get database
    file_path = '../data/0500kPa_003SA_10000cycles_to_20000cycles.csv'  # Replace with file path
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

def get_halved_csv_file(filename):
    """
    Given a filename, cut every other line and resave
    """
    df = pd.read_csv(filename,header=None)         # read file
    df = df.drop(df.index[4::2])                     # drop every 2nd rows
    df.to_csv(filename[:39] + "test.csv",index=None,header=None)     # save file


def plot_all_compression_data(col1, col2, col3):
    plt.figure(figsize=(8, 6))
    print(type(col2))
    plt.plot(col2[:300], col3[:300], label="Start of 20000 cycles")
    plt.plot(col2[200140:200360], col3[200140:200360], label="At 12500 cycles")
    plt.plot(col2[300220:300440], col3[300220:300440], label="At 15000 cycles")
    plt.plot(col2[400050:400300], col3[400050:400300], label="At 17500 cycles")
    plt.plot(col2[-700:-450], col3[-700:-450], label="End of 20000 cycles")
    # plt.xlim([-8, 0])
    # plt.ylim([-0.25, 0])
    plt.legend()
    plt.grid()
    plt.xlabel('Deformation [mm]')
    plt.ylabel('Force [kN]')
    plt.title('Plot of Select Cycles in 20000 Compressions - 0.5 MPa 30 mm Cube VTP 2025/03/21')
    plt.savefig("./compression_cycling_plot_0500kpa_10k_to_20k_cycles_snapshots.png")
    plt.show()

def plot_zoomed_compression_data(col1, col2, col3):
    plt.figure(figsize=(8, 6))
    plt.plot(col2, col3)
    # plt.xlim([-14, -13.2])
    # plt.ylim([-0.038, -0.03])
    plt.legend()
    plt.grid()
    plt.xlabel('Deformation [mm]')
    plt.ylabel('Force [kN]')
    plt.title('Plot of 20000 Compressions Zoomed In - 5 MPa 30 mm Cube VTP 2025/03/21')
    plt.savefig("./compression_cycling_plot_zoomed_0500kpa_10k_to_20k_cycles.png")
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
    get_halved_csv_file("../data/5000kPa_001SA_run2_10000cycle_2.csv")

    col1, col2, col3, s_rows = load_file()
    plot_all_compression_data(col1, col2, col3)
    # plot_zoomed_compression_data(col1, col2, col3)
    # s_col1 = s_rows.iloc[:, 1].astype(float)
    # s_col2 = s_rows.iloc[:, 2].astype(float)
    # print(type(s_rows))
    # print(s_rows)
    # plot_specific_compression_data(s_col1, s_col2)