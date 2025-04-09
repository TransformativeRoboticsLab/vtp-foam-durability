# VTP Compression Durability Analysis
# Jacob Miske
import pandas as pd
import matplotlib.pyplot as plt


def load_file():
    # Given csv filename, get database
    file_path = '../data/100kcycle_0500MPa_1prepped.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_path, skiprows=2)
    # Check the data
    print(df.head())
    # Convert columns to plottable data types if not already
    col1 = df.iloc[:, 0].astype(float)  # First column as floats
    col2 = df.iloc[:, 1].astype(float)  # Second column as floats
    col3 = df.iloc[:, 2].astype(float)  # Third column as floats
    # Take every 515th row and save to a list
    sampled_rows = df.iloc[::515].astype(float)
    print("Sampled rows:", sampled_rows)
    return col1, col2, col3, sampled_rows


def load_file_2():
    # Given csv filename, get database
    file_path = '../data/0500kPa_003SA_10000cycles_to_20000cycles.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_path, skiprows=2)
    # Check the data
    print(df.head())
    # Convert columns to plottable data types if not already
    col1_2 = df.iloc[:, 0].astype(float)  # First column as floats
    col2_2 = df.iloc[:, 1].astype(float)  # Second column as floats
    col3_2 = df.iloc[:, 2].astype(float)  # Third column as floats
    # Take every 515th row and save to a list
    sampled_rows_2 = df.iloc[::515].astype(float)
    print("Sampled rows:", sampled_rows_2)
    return col1_2, col2_2, col3_2, sampled_rows_2


def get_stress_strain_from_data(displacement, force, area, start_length):
    """
    Given force, area, displacement, and L0
    return stress and strain data
    """
    epsilon = [i/start_length for i in displacement]
    sigma = [j/area for j in force]
    return epsilon, sigma


def plot_all_compression_data(col1, col2, col3, col1_2, col2_2, col3_2):
    plt.figure(figsize=(8, 6))
    print(type(col2))
    plt.plot(col2, col3, label="At 100 Kilocycles Sawzall")
    plt.plot(col2_2[:300], col3_2[:300], label="At 1000 cycles Instron (start)")
    # plt.plot(col2_2[-700:-430], col3_2[-700:-430], label="At 20000 cycles Instron (end)")
    # plt.plot(col2[:300], col3[:300], label="Start of 20000 cycles")
    # plt.plot(col2[200140:200360], col3[200140:200360], label="At 12500 cycles")
    # plt.plot(col2[300220:300440], col3[300220:300440], label="At 15000 cycles")
    # plt.plot(col2[400050:400300], col3[400050:400300], label="At 17500 cycles")
    # plt.plot(col2[-700:-450], col3[-700:-450], label="End of 20000 cycles")
    # plt.xlim([-8, 0])
    # plt.ylim([-0.25, 0])

    plt.legend()
    plt.grid()
    plt.xlabel('Strain')
    plt.ylabel('Stress [kPa]')
    plt.title('Plot at 100k and 1k cycles - 0.5 MPa 30 mm Cube VTP 2025/03/31')
    plt.savefig("./stress_strain_compression_cycle_plot_0500kpa_at_100kilocycles.png")
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
    plt.title('Plot at 100k and 1k cycles Zoomed In - 5 MPa 30 mm Cube VTP 2025/03/31')
    plt.savefig("./compression_cycle_plot_zoomed_0500kpa_at_100kilocycles.png")
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
    # get_halved_csv_file("../data/5000kPa_001SA_run2_10000cycle_2.csv")

    time0, disp0, force0, s_rows = load_file()
    time1, disp1, force1, s_rows_2 = load_file_2()
    area0 = 0.0009 # square meters
    area1 = 0.0009 # square meters
    area2 = 0.0009 # square meters
    L0_0 = 0.03*1000 # millimeters
    L0_1 = 0.0290*1000 # millimeters
    L0_2 = 0.0295*1000 # millimeters

    strain0, stress0 = get_stress_strain_from_data(displacement=list(disp0), force=list(force0), area=area0, start_length=L0_0)
    strain1, stress1 = get_stress_strain_from_data(displacement=list(disp1), force=list(force1), area=area1, start_length=L0_1)
    # Convert to positive
    strain0 = [-i for i in strain0]
    strain1 = [-i for i in strain1]
    stress0 = [-i for i in stress0]
    stress1 = [-i for i in stress1]

    plot_all_compression_data(time0, strain0, stress0, time1, strain1, stress1)
    # plot_zoomed_compression_data(col1, col2, col3)
    # s_col1 = s_rows.iloc[:, 1].astype(float)
    # s_col2 = s_rows.iloc[:, 2].astype(float)
    # print(type(s_rows))
    # print(s_rows)
    # plot_specific_compression_data(s_col1, s_col2)