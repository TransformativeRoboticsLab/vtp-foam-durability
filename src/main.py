# VTP Compression Durability Analysis
# Jacob Miske
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'Times New Roman'
rcParams.update({'font.size': 14})


def load_file(file_name):
    # Given csv filename, get database
    # file_path = '../data/100kcycle_0500MPa_1prepped.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_name, skiprows=2)
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


def load_file_3pb(file_name):
    # Given csv filename, get database
    # file_path = '../data/100kcycle_0500MPa_1prepped.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_name, skiprows=2)
    # Check the data
    print(df.head())
    # Convert columns to plottable data types if not already
    col1 = df.iloc[:, 0] # .astype(float)  # First column as floats
    col2 = df.iloc[:, 1] # .astype(float)  # Second column as floats
    col3 = df.iloc[:, 2] # .astype(float)  # Third column as floats
    # Take every 515th row and save to a list
    sampled_rows = df.iloc[::515].astype(float)
    print("Sampled rows:", sampled_rows)
    # time, flex displacement, flexural stress
    return col1, col2, col3, sampled_rows


# def load_file_2():
#     # Given csv filename, get database
#     file_path = '../data/0500kPa_003SA_10000cycles_to_20000cycles.csv'  # Replace with file path
#     # Read the CSV and skip the first two rows
#     df = pd.read_csv(file_path, skiprows=2)
#     # Check the data
#     print(df.head())
#     # Convert columns to plottable data types if not already
#     col1_2 = df.iloc[:, 0].astype(float)  # First column as floats
#     col2_2 = df.iloc[:, 1].astype(float)  # Second column as floats
#     col3_2 = df.iloc[:, 2].astype(float)  # Third column as floats
#     # Take every 515th row and save to a list
#     sampled_rows_2 = df.iloc[::515].astype(float)
#     print("Sampled rows:", sampled_rows_2)
#     return col1_2, col2_2, col3_2, sampled_rows_2

def set_file_to_positive_force_displacement(file_name, new_file_name):
    """
    For files with negative force and displacement, convert to positive
    """
    # Given csv filename, get database
    # file_path = '../data/100kcycle_0500MPa_1prepped.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_name, skiprows=2)
    # Check the data
    print(df.head())
    # Invert the sign of the second and third columns
    df.iloc[:, 1:3] = -df.iloc[:, 1:3]    
    df.to_csv(new_file_name, index=False)
    return 0

def get_stress_strain_from_data(displacement, force, area, start_length):
    """
    Given force, area, displacement, and L0
    return stress and strain data
    """
    epsilon = [float(i)/start_length for i in displacement]
    # in MPa
    sigma = [1000*float(j)/area for j in force]
    return epsilon, sigma


def get_flexural_stress_strain_from_data(displacement, force, area, start_length):
    """
    Given force, area, displacement, and L0
    return stress and strain data
    """
    epsilon = [float(i)/start_length for i in displacement]
    sigma = [float(j)/(1000*area) for j in force]
    return epsilon, sigma


def get_positive_form(strain, stress):
    """
    """
    # Convert to positive
    epsilon = [-i for i in strain]
    sigma = [-i for i in stress]
    print(sigma[-10:])
    return epsilon, sigma


def plot_force_displacement(col1, col2, plot_title, file_name):
    """
    Take data from Instron force and displacement and plot relative
    """
    # Convert to Newtons
    col2 = [1000*i for i in col2]
    # Get initial linear fit
    linear_coeffs = np.polyfit(col1[:80], col2[0:80], 1)
    y_line = [i * linear_coeffs[0] + linear_coeffs[1] for i in col1]
    # Get second order fit
    second_order_coeffs = np.polyfit(col1, col2, 3)
    y_arc = [i**2 * second_order_coeffs[0] + i * second_order_coeffs[1] + second_order_coeffs[2] for i in col1]
    # Make plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(col1, col2, label="TPU Filament (130 mm)")
    plt.plot(col1, y_line, label="Linear Fit", linestyle='dashed')
    plt.plot(col1, y_arc, label="Second Order Fit", linestyle='dashed')
    # place a text box in upper left in axes coords
    ax.text(0.07, 0.92, "Force to Displacement Ratio: " + str(round(linear_coeffs[0], 2)) + " N/mm", transform=ax.transAxes, fontsize=14,
        verticalalignment='top')
    plt.legend()
    plt.grid()
    plt.xlabel('Displacement (mm)')
    plt.ylabel('Force [N]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()
    return 0


def plot_compression_data(col1, col2, col3, plot_title, file_name):
    """
    """
    # convert stress if necessary
    col3 = [i for i in col3]
    # adjust strain
    col2 = [i-0.01 for i in col2]
    # get 5% and 15% strain points
    five_percent_index = min(range(len(col2)), key=lambda i: abs(col2[i] - 0.05))
    six_percent_index = min(range(len(col2)), key=lambda i: abs(col2[i] - 0.06))
    ten_percent_index = min(range(len(col2)), key=lambda i: abs(col2[i] - 0.10))

    # Get linear fit
    linear_coeffs = np.polyfit(col2[five_percent_index:six_percent_index], col3[five_percent_index:six_percent_index], 1)
    y_line = [i * linear_coeffs[0] + linear_coeffs[1] for i in col2]
    # Make plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(col2, col3, label="Sample")
    # plt.plot(col2, y_line, label="Linear Fit", linestyle='dashed')
    # place a text box in upper left in axes coords
    # ax.text(0.07, 0.92, "Young's Modulus: " + str(round(linear_coeffs[0], 2)) + " MPa", transform=ax.transAxes, fontsize=14,
    #    verticalalignment='top')
    # plt.xlim([0, 0.5])
    # plt.ylim([0, 0.01])
    plt.legend()
    plt.grid()
    plt.xlabel('Strain')
    plt.ylabel('Stress [MPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()
    return 0

def plot_shear_data(col1, col2, col3, plot_title, file_name):
    """
    """
    # convert stress if necessary
    col3 = [-i*1000 for i in col3]
    # adjust strain
    col2 = [-i for i in col2]
    # # get 5% and 15% strain points
    # five_percent_index = min(range(len(col2)), key=lambda i: abs(col2[i] - 0.05))
    # six_percent_index = min(range(len(col2)), key=lambda i: abs(col2[i] - 0.06))
    # ten_percent_index = min(range(len(col2)), key=lambda i: abs(col2[i] - 0.10))
    # # Get linear fit
    # linear_coeffs = np.polyfit(col2[five_percent_index:six_percent_index], col3[five_percent_index:six_percent_index], 1)
    # y_line = [i * linear_coeffs[0] + linear_coeffs[1] for i in col2]
    # Make plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(col2[:100], col3[:100], label="First Cycle")
    plt.plot(col2[-100:], col3[-100:], label="1000th Cycle")
    plt.legend()
    plt.grid()
    plt.xlabel('Shear Strain')
    plt.ylabel('Shear Stress [MPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()
    return 0



def plot_compression_data_at_four_levels(col1, col2, col3, plot_title, file_name):
    """
    """
    data_len = int(len(col2))
    quarter_len = int(round(data_len/4,0))
    half_len = int(round(data_len/2,0))
    threequart_len = int(round(3*data_len/4,0))

    # convert stress
    col3 = [i for i in col3]
    # Make plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(col2[:500], col3[:500], label="First Cycle")
    plt.plot(col2[quarter_len:quarter_len+500], col3[quarter_len:quarter_len+500], label="250th Cycle")
    plt.plot(col2[half_len:half_len+500], col3[half_len:half_len+500], label="500th Cycle")
    plt.plot(col2[threequart_len:threequart_len+500], col3[threequart_len:threequart_len+500], label="750th Cycle")
    plt.plot(col2[-500:0], col3[-500:0], label="1000th Cycle")
    # plt.xlim([0, 0.25])
    # plt.ylim([0, 0.30])
    plt.legend()
    plt.grid()
    plt.xlabel('Strain')
    plt.ylabel('Stress [MPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()
    return 0



def plot_3pointbend_data(col1, col2, col3, plot_title, file_name):
    """
    """
    col2 = [(-i-0.04) for i in col2]
    col3 = [(-i-0.04)*10000+400 for i in col3]

    plt.figure(figsize=(8, 6))
    print(type(col2))
    plt.plot(col2[:150], col3[:150], label="Start")
    plt.plot(col2[5050:5170], col3[5050:5170], label="1000 Cycle")

    plt.legend()
    plt.xlim([0, 0.3])
    plt.grid()
    plt.xlabel('Flexural Strain')
    plt.ylabel('Shear Stress [kPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()


def plot_all_compression_data(col1, col2, col3, col1_2, col2_2, col3_2, plot_title, file_name):
    plt.figure(figsize=(8, 6))
    print(type(col2))
    # pre process
    col2_2 = [i -0.01 for i in col2_2]
    plt.plot(col2, col3, label="Baked")
    plt.plot(col2_2[:105], col3_2[:105], label="Unbaked")
    # plt.plot(col2_2[-700:-430], col3_2[-700:-430], label="At 20000 cycles Instron (end)")
    # plt.plot(col2[:300], col3[:300], label="Start of 20000 cycles")
    # plt.plot(col2[200140:200360], col3[200140:200360], label="At 12500 cycles")
    # plt.plot(col2[300220:300440], col3[300220:300440], label="At 15000 cycles")
    # plt.plot(col2[400050:400300], col3[400050:400300], label="At 17500 cycles")
    # plt.plot(col2[-700:-450], col3[-700:-450], label="End of 20000 cycles")
    plt.xlim([0, 0.35])
    plt.ylim([0, 200])
    plt.legend()
    plt.grid()
    plt.xlabel('Strain')
    plt.ylabel('Stress [kPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()


def plot_four_compression_data_figure4(strain1, stress1, strain2, stress2, strain3, stress3, strain4, stress4, plot_title, file_name):
    # Get linear fits
    linear_coeffs1 = np.polyfit(strain1[:230], stress1[:230], 1)
    y_line1 = [i * linear_coeffs1[0] + linear_coeffs1[1] for i in strain1]
    linear_coeffs2 = np.polyfit(strain2[:1000], stress2[:1000], 1)
    y_line2 = [i * linear_coeffs2[0] + linear_coeffs2[1] for i in strain2]
    linear_coeffs3 = np.polyfit(strain3[:100], stress3[:100], 1)
    y_line3 = [i * linear_coeffs3[0] + linear_coeffs3[1] for i in strain3]
    linear_coeffs4 = np.polyfit(strain4[:], stress4[:], 1)
    y_line4 = [i * linear_coeffs4[0] + linear_coeffs4[1] for i in strain4]
    # generate figure
    fig, ax = plt.subplots(figsize=(8, 6))
    # pre process to adjust zero points
    strain1 = [i - 0.11 for i in strain1]
    strain3 = [i - 0.02 for i in strain3]
    strain4 = [i - 0.01 for i in strain4]
    plt.plot(strain1, stress1, label="Low ρ Initial", color="#ff0000")
    plt.plot(strain2, stress2, label="Low ρ at 1E5 Cycles", color="#b50000")
    plt.plot(strain3, stress3, label="High ρ Initial", color="#0000ff")
    plt.plot(strain4, stress4, label="High ρ at 1E5 Cycles", color="#0000b5")
    plt.plot(strain1, y_line1, label="Fit Line, Low ρ Initial", linestyle='dashed', alpha=0.6, color="#ff0000")
    plt.plot(strain2, y_line2, label="Fit Line, Low ρ 1E5 Cycles", linestyle='dashed', alpha=0.6, color="#b50000")
    plt.plot(strain3, y_line3, label="Fit Line, High ρ Initial", linestyle='dashed', alpha=0.6, color="#0000ff")
    plt.plot(strain4, y_line4, label="Fit Line, High ρ 1E5 Cycles", linestyle='dashed', alpha=0.6, color="#0000b5")
    plt.xlim([0, 0.3])
    plt.ylim([0, 0.2])
    plt.legend()
    plt.grid()
    plt.xlabel('Strain')
    plt.ylabel('Stress [MPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()


def plot_four_compression_data(strain1, stress1, strain2, stress2, strain3, stress3, strain4, stress4, plot_title, file_name):
    """
    """
    # Get linear fits
    linear_coeffs1 = np.polyfit(strain1[:230], stress1[:230], 1)
    y_line1 = [i * linear_coeffs1[0] + linear_coeffs1[1] for i in strain1]
    linear_coeffs2 = np.polyfit(strain2[:1000], stress2[:1000], 1)
    y_line2 = [i * linear_coeffs2[0] + linear_coeffs2[1] for i in strain2]
    linear_coeffs3 = np.polyfit(strain3[:100], stress3[:100], 1)
    y_line3 = [i * linear_coeffs3[0] + linear_coeffs3[1] for i in strain3]
    linear_coeffs4 = np.polyfit(strain4[:], stress4[:], 1)
    y_line4 = [i * linear_coeffs4[0] + linear_coeffs4[1] for i in strain4]
    # generate figure
    fig, ax = plt.subplots(figsize=(8, 6))
    # pre process to adjust zero points
    strain1 = [i - 0.11 for i in strain1]
    strain3 = [i - 0.02 for i in strain3]
    strain4 = [i - 0.01 for i in strain4]
    plt.plot(strain1, stress1, label="Low ρ Initial", color="#ff0000")
    plt.plot(strain2, stress2, label="Low ρ at 1E5 Cycles", color="#b50000")
    plt.plot(strain3, stress3, label="High ρ Initial", color="#0000ff")
    plt.plot(strain4, stress4, label="High ρ at 1E5 Cycles", color="#0000b5")
    # plt.plot(strain1, y_line1, label="Fit Line, Low ρ Initial", linestyle='dashed', alpha=0.6, color="#ff0000")
    # plt.plot(strain2, y_line2, label="Fit Line, Low ρ 1E5 Cycles", linestyle='dashed', alpha=0.6, color="#b50000")
    # plt.plot(strain3, y_line3, label="Fit Line, High ρ Initial", linestyle='dashed', alpha=0.6, color="#0000ff")
    # plt.plot(strain4, y_line4, label="Fit Line, High ρ 1E5 Cycles", linestyle='dashed', alpha=0.6, color="#0000b5")

    # place a text box in upper left in axes coords
    # ax.text(0.07, 0.92, "Young's Modulus: " + str(round(linear_coeffs1[0], 2)) + " MPa", transform=ax.transAxes, fontsize=14,
    #     verticalalignment='top')
    # ax.text(0.07, 0.88, "Young's Modulus: " + str(round(linear_coeffs2[0], 2)) + " MPa", transform=ax.transAxes, fontsize=14,
    #     verticalalignment='top')
    # ax.text(0.07, 0.84, "Young's Modulus: " + str(round(linear_coeffs3[0], 2)) + " MPa", transform=ax.transAxes, fontsize=14,
    #     verticalalignment='top')
    # ax.text(0.07, 0.8, "Young's Modulus: " + str(round(linear_coeffs4[0], 2)) + " MPa", transform=ax.transAxes, fontsize=14,
    #     verticalalignment='top')
    plt.xlim([0, 0.3])
    plt.ylim([0, 0.2])
    plt.legend()
    plt.grid()
    plt.xlabel('Strain')
    plt.ylabel('Stress [MPa]')
    plt.title(plot_title)
    plt.savefig(file_name)
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


def plot_SN_curve(cycles, mods, heights, plot_title, file_name):
    """
    """
    # convert MPa moduli to kPa
    mods = [i*1000 for i in mods]
    # get polyfit lines
    coeffs = np.polyfit(cycles, mods, deg=4)
    print(coeffs)
    fit_fn = [coeffs[0]**4 * i + coeffs[1]**3 * i + coeffs[2]**2 * i + coeffs[3] * i + coeffs[4] for i in cycles]
    # generate figure
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.scatter(cycles, mods, color='purple', label='Moduli')
    # plt.plot(cycles, fit_fn, color='black', linestyle='dashed')
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel('Compression Modulus [kPa]', color='purple')
    ax.tick_params(axis='y', labelcolor='purple')
    # Create second y-axis (right side)
    ax2 = ax.twinx()
    # Second scatter plot (right y-axis)
    ax2.scatter(cycles, heights, color='green', label='Heights')
    ax2.set_ylabel('Sample Height [mm]', color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    plt.legend()
    plt.grid()
    ax.set_xlabel('220 N Compression Cycles')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()
    return 0


def plot_two_SN_curves(cycles1, mods1, heights1, cycles2, mods2, heights2, plot_title, file_name):
    """
    """
    # convert MPa moduli to kPa
    mods1 = [i*1000 for i in mods1]
    mods2 = [i*1000 for i in mods2]
    # Generate figure
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.scatter(cycles1, mods1, color='#ff0000', label='Low Density Moduli')
    plt.scatter(cycles2, mods2, color='#0000ff', label='High Density Moduli')
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel('Compression Modulus [kPa]', color='purple')
    ax.tick_params(axis='y', labelcolor='purple')
    # Create second y-axis (right side)
    ax2 = ax.twinx()
    # Second scatter plot (right y-axis)
    ax2.scatter(cycles1, heights1, color='#00ff00', label='Heights')
    ax2.scatter(cycles2, heights2, color="#007C00", label='Heights')

    ax2.set_ylabel('Sample Height [mm]', color='#00ff00')
    ax2.tick_params(axis='y', labelcolor='#00ff00')
    
    plt.legend()
    plt.grid()
    ax.set_xlabel('220 N Compression Cycles')
    plt.title(plot_title)
    plt.savefig(file_name)
    plt.show()
    return 0




if __name__ == '__main__':
    # Metal samples
    # area0 = 400  # mm squared
    # area1 = 350 # mm squared
    # L0 = 20     # mm
    # L1 = 13     # mm
    # t1, disp1, force1, s_rows = load_file(file_name='../data/PLA_copper_1point6mmlines_25percentvolume_gyroid_1.csv')
    # t2, disp2, force2, s_rows = load_file(file_name='../data/PLA_mean_copper_VTP_specimen001_20250722_1kN_1.csv')
    # strain1, stress1 = get_stress_strain_from_data(displacement=list(disp1), force=list(force1), area=area0, start_length=L0)
    # strain2, stress2 = get_stress_strain_from_data(displacement=list(disp2), force=list(force2), area=area1, start_length=L1)
    # plot_compression_data(col1=t1, col2=strain1, col3=stress1, plot_title="Copper PLA 1.6mm Line Thickness 25% Volume Fraction", file_name="./copper_1p6mm_gyroid_25percent_001_nofit.png")
    # plot_compression_data(col1=t2, col2=strain2, col3=stress2, plot_title="Copper PLA Model Mean VTP Specimen 001", file_name="./copper_PLA_VTP_001_nofit.png")
    

    # Effective Modulus Samples
    area = 900  # mm squared
    L0 = 30     # mm
    t1, disp1, force1, s_rows = load_file(file_name='../data/VTP_testing/PLA_high_effective_001_1.csv')
    t2, disp2, force2, s_rows = load_file(file_name='../data/VTP_testing/PLA_low_effective_001_1.csv')
    t3, disp3, force3, s_rows = load_file(file_name='../data/VTP_testing/TPU_high_effective_001_1.csv')
    t4, disp4, force4, s_rows = load_file(file_name='../data/VTP_testing/TPU_mean_effective_001_1.csv')
    t5, disp5, force5, s_rows = load_file(file_name='../data/VTP_testing/TPU_median_effective_001_1.csv')
    strain1, stress1 = get_stress_strain_from_data(displacement=list(disp1), force=list(force1), area=area, start_length=L0)
    strain2, stress2 = get_stress_strain_from_data(displacement=list(disp2), force=list(force2), area=area, start_length=L0)
    strain3, stress3 = get_stress_strain_from_data(displacement=list(disp3), force=list(force3), area=area, start_length=L0)
    strain4, stress4 = get_stress_strain_from_data(displacement=list(disp4), force=list(force4), area=area, start_length=L0)
    strain5, stress5 = get_stress_strain_from_data(displacement=list(disp5), force=list(force5), area=area, start_length=L0)
    plot_compression_data(col1=t1, col2=strain1, col3=stress1, plot_title="PLA High Effective 001", file_name="./PLA_HIGH_EFFECTIVE_001.png")
    plot_compression_data(col1=t2, col2=strain2, col3=stress2, plot_title="PLA Low Effective 001", file_name="./PLA_LOW_EFFECTIVE_001.png")
    plot_compression_data(col1=t3, col2=strain3, col3=stress3, plot_title="TPU High Effective 001", file_name="./TPU_HIGH_EFFECTIVE_001.png")
    plot_compression_data(col1=t4, col2=strain4, col3=stress4, plot_title="TPU Mean Effective 001", file_name="./TPU_MEAN_EFFECTIVE_001.png")
    plot_compression_data(col1=t5, col2=strain5, col3=stress5, plot_title="TPU Median Effective 001", file_name="./TPU_MEDIAN_EFFECTIVE_001.png")
