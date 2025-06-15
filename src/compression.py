# VTP Compression Durability Analysis
# Jacob Miske
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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
    # convert stress
    col3 = [i for i in col3]
    # Get initial linear fit
    linear_coeffs = np.polyfit(col2[:], col3[:], 1)
    y_line = [i * linear_coeffs[0] + linear_coeffs[1] for i in col2]
    # Make plot
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.plot(col2, col3, label="Sample")
    plt.plot(col2, y_line, label="Linear Fit", linestyle='dashed')
    # place a text box in upper left in axes coords
    ax.text(0.07, 0.92, "Young's Modulus: " + str(round(linear_coeffs[0], 2)) + " MPa", transform=ax.transAxes, fontsize=14,
        verticalalignment='top')
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
    plt.plot(strain1, y_line1, label="Fit Line, Low ρ Initial", linestyle='dashed', alpha=0.6, color="#ff0000")
    plt.plot(strain2, y_line2, label="Fit Line, Low ρ 1E5 Cycles", linestyle='dashed', alpha=0.6, color="#b50000")
    plt.plot(strain3, y_line3, label="Fit Line, High ρ Initial", linestyle='dashed', alpha=0.6, color="#0000ff")
    plt.plot(strain4, y_line4, label="Fit Line, High ρ 1E5 Cycles", linestyle='dashed', alpha=0.6, color="#0000b5")

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
    # generate figure
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.scatter(cycles, mods, color='purple', label='Moduli')
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


if __name__ == '__main__':
    # file handling
    set_file_to_positive_force_displacement(file_name="../data/0500kPa001SA003SP_1k.csv", new_file_name="../data/0500kPa001SA003SP_1k_fixed.csv")
    set_file_to_positive_force_displacement(file_name="../data/0500kPa001SA003SP_10000cycles_to_20000cycles.csv", new_file_name="../data/0500kPa001SA003SP_10k_to_20k_fixed.csv")

    # get density based on low strain of different samples
    sample_moduli = [0.2, 0.5, 1, 2, 5] # MPa
    density = 1.21 # grams/cm^3
    TPU_max_modulus = 12 # MPa
    sample_volume_fraction = [i/TPU_max_modulus for i in sample_moduli]
    sample_density = [round(density*i,3) for i in sample_volume_fraction]
    print("Density of Samples: \n")
    print(sample_density)

    # Figure 4A. Stress Strain Curve for One Cube over first 1000 cycles
     

    # Figure 4B. Stress Strain Curves for Different Density
    area = 900  # mm squared
    L0 = 30     # mm
    time1, disp1, force1, s_rows = load_file(file_name='../data/0500kPa001SA003SP_1k.csv')
    time2, disp2, force2, s_rows = load_file(file_name='../data/0500kPa001SA006SP_100k.csv')
    time3, disp3, force3, s_rows = load_file(file_name='../data/5000kPa001SA006SP_1.csv')
    time4, disp4, force4, s_rows = load_file(file_name='../data/5000kPa001SA006SP_100k.csv')
    strain1, stress1 = get_stress_strain_from_data(displacement=list(disp1), force=list(force1), area=area, start_length=L0)
    strain2, stress2 = get_stress_strain_from_data(displacement=list(disp2), force=list(force2), area=area, start_length=L0)
    strain3, stress3 = get_stress_strain_from_data(displacement=list(disp3), force=list(force3), area=area, start_length=L0)
    strain4, stress4 = get_stress_strain_from_data(displacement=list(disp4), force=list(force4), area=area, start_length=L0)
    # convert old instron data to position format
    strain1, stress1 = get_positive_form(strain=strain1, stress=stress1)
    strain3, stress3 = get_positive_form(strain=strain3, stress=stress3)
    plot_four_compression_data(strain1[:230], stress1[:230], strain2, stress2, strain3[:100], stress3[:100], strain4, stress4, plot_title="Different Modulus in Cycled VTP Foam Stress to Strain", file_name="./figure4_0500kPa_to_5000kPa_comparison.png")


    # Figure 5A. SN Curve for Compression of High and Low Density Foam
    # first, get modulus at 10% strain for list of file names
    comp_modulus_list = []
    sample_height = [30.1, 29.8, 29.1, 29.0, 28.8]
    file_names = ["../data/0500kPa001SA003SP_1k_fixed.csv", "../data/0500kPa001SA003SP_10k_to_20k_fixed.csv", "../data/0500kPa001SA006SP_100k.csv", "../data/0500kPa001SA006SP_200k.csv", "../data/0500kPa001SA006SP_1E6cycles_1.csv"]
    cycles_list = [1000, 10000, 100000, 200000, 1000000]
    for file in file_names:
        _, disp1, force1, _ = load_file(file_name=file)
        strain1, stress1 = get_stress_strain_from_data(displacement=list(disp1), force=list(force1), area=area, start_length=L0)
        # Get 10% strain modulus
        index_at_strain = min(range(len(strain1)), key=lambda i: abs(strain1[i] - 0.2))
        print("Index at strain: {}".format(index_at_strain))
        modulus = np.average(stress1[index_at_strain-60:index_at_strain+60])/np.average(strain1[index_at_strain-60:index_at_strain+60])
        comp_modulus_list.append(modulus)
    # comp_modulus_list = [0.0]
    plot_SN_curve(cycles_list, comp_modulus_list, heights=sample_height, plot_title="0.04 g/cm3 VTP Foam SN Curve", file_name="./SNcurve_test.png")

    # Figure 5B. SN Curve for Flexural of High and Low Density Foam
    # first, get modulus at 10% strain for 
    #plot_SN_curve(cycle_list, modulus_list)

    quit()
    # OTHER FIGURE GENERATION

    # Abrasion Slab Effective Modulus sample 12000 kPa Surface coat
    time_filament, disp_filament, force_filament, s_rows = load_file(file_name='../data/6000kPa_E_Ab_12000kPaSurfaceCoat_002SP_1.csv')
    area1 = 3200 # mm squared
    L0_1 = 8.9 # mm
    strain_filament, stress_filament = get_stress_strain_from_data(displacement=list(disp_filament), force=list(force_filament), area=area1, start_length=L0_1)
    plot_compression_data(col1=time_filament, col2=strain_filament, col3=stress_filament, plot_title="5.9 MPa Equivalent Slab with 12 MPa Surface Stress to Strain", file_name="./5900kPa_Eq_12000kPa_coat_stress_strain_002SP.png")


    # Abrasion Slab Effective Modulus sample 1
    # time_filament, disp_filament, force_filament, s_rows = load_file(file_name='../data/1000kPa001SA_E_Ab_2000kPaSurfaceCoat_1.csv')
    # area1 = 3200 # mm squared
    # L0_1 = 8.9 # mm
    # strain_filament, stress_filament = get_stress_strain_from_data(displacement=list(disp_filament), force=list(force_filament), area=area1, start_length=L0_1)
    # plot_compression_data(col1=time_filament, col2=strain_filament, col3=stress_filament, plot_title="1 MPa Equivalent Slab with 2 MPa surface Stress to Strain", file_name="./1MPa_Eq_2MPa_coat_stress_strain_001SP.png")
    # # Abrasion Slab Effective Modulus sample 2
    # time_filament, disp_filament, force_filament, s_rows = load_file(file_name='../data/1000kPa001SA_E_Ab_2000kPaSurfaceCoat_2.csv')
    # area1 = 3200 # mm squared
    # L0_1 = 8.9 # mm
    # strain_filament, stress_filament = get_stress_strain_from_data(displacement=list(disp_filament), force=list(force_filament), area=area1, start_length=L0_1)
    # plot_compression_data(col1=time_filament, col2=strain_filament, col3=stress_filament, plot_title="1 MPa Equivalent Slab with 2 MPa surface Stress to Strain", file_name="./1MPa_Eq_2MPa_coat_stress_strain_002SP.png")


    # Filament pull data
    # time_filament, disp_filament, force_filament, s_rows = load_file(file_name='../data/TPU_filament_pull_1.csv')
    # plot_force_displacement(col1=disp_filament, col2=force_filament, plot_title="Ninjaflex TPU 85A Filament Force to Displacement", file_name="./TPU_F_to_disp.png")
    # area1 = 2.4 # mm squared
    # L0_1 = 130 # mm
    # strain_filament, stress_filament = get_stress_strain_from_data(displacement=list(disp_filament), force=list(force_filament), area=area1, start_length=L0_1)
    # Convert to positive
    # strain0 = [-i for i in strain0]
    # strain1 = [-i for i in strain_filament]
    # # stress0 = [-i for i in stress0]
    # stress1 = [-i for i in stress_filament]
    # plot_compression_data(col1=time_filament, col2=strain_filament, col3=stress_filament, plot_title="Ninjaflex TPU 85A Filament Stress to Strain", file_name="./TPU_filament_stress_strain.png")
    

    # get_halved_csv_file("../data/5000kPa_001SA_run2_10000cycle_2.csv")
    # time_3pb_5MPa_thick, disp_3pb_5MPa_thick, force_3pb_5MPa_thick, s_rows_3pb_5MPa_thick = load_file_3pb(file_name='../data/5000kPa_001SA_Ab_001SP_Flexural_1_1.csv')
    # time_3pb_5MPa_thin, disp_3pb_5MPa_thin, force_3pb_5MPa_thin, s_rows_3pb_5MPa_thick = load_file_3pb(file_name='../data/5000kPa-thin2_5_3pointbend.csv')
    # TODO: modify area and length for shear stress and strain
    # strain_3pb_5MPa_thick, stress_3pb_5MPa_thick = get_flexural_stress_strain_from_data(displacement=list(disp_3pb_5MPa_thick), force=list(force_3pb_5MPa_thick), area=area0, start_length=L0_0)
    # strain_3pb_5MPa_thin, stress_3pb_5MPa_thin = get_stress_strain_from_data(displacement=list(disp_3pb_5MPa_thin), force=list(force_3pb_5MPa_thin), area=area0, start_length=L0_0)
    # plot_3pointbend_data(time0, strain_3pb_5MPa_thick, stress_3pb_5MPa_thick, plot_title="Flexural 1000 cycle Shear Stress and Strain", file_name="./5MPa_3pb_20250507_1000cycle.png")
    # plot_3pointbend_data(time0, strain_3pb_5MPa_thin, stress_3pb_5MPa_thin, plot_title="Three Point Bend Shear Stress and Strain - Thin Samples", file_name="./5MPa_3pb_thin_20250416.png")

    

    # Cube Specimen Stress vs Strain
    time0, disp0, force0, s_rows = load_file(file_name='../data/5000kPa001SA007SP_baked80C_1.csv')
    time1, disp1, force1, s_rows_2 = load_file(file_name="../data/5000kPa_001SA_1_1.csv")
    area0 = 900 # square millimeters
    area1 = 900 # square millimeters
    area2 = 900 # square millimeters
    L0_0 = 30 # millimeters
    L0_1 = 29.0 # millimeters
    L0_2 = 29.5 # millimeters
    # Compression stress and strain
    strain0, stress0 = get_stress_strain_from_data(displacement=list(disp0), force=list(force0), area=area0, start_length=L0_0)
    strain1, stress1 = get_stress_strain_from_data(displacement=list(disp1), force=list(force1), area=area1, start_length=L0_1)
    # Convert to positive
    # strain0 = [-i for i in strain0]
    strain1 = [-i for i in strain1]
    # stress0 = [-i for i in stress0]
    stress1 = [-i for i in stress1]
    plot_compression_data(time0, strain0, stress0, plot_title="5 MPa Baked 80C Cube 2025/05/07", file_name="./5000kPa001SA007SP_baked.png")
    # plot_all_compression_data(time0, strain0, stress0, time1, strain1, stress1, plot_title="5 MPa Baked vs Unbaked Compression", file_name="./5000kPa_unbaked_vs_baked.png")

    # Cube cyclic testing
    time0, disp0, force0, s_rows = load_file(file_name='../data/5000kPa001SA006SP_100kcycle_comp_1.csv')
    area0 = 900 # square millimeters
    L0_0 = 30 # millimeters
    # Compression stress and strain
    strain0, stress0 = get_stress_strain_from_data(displacement=list(disp0), force=list(force0), area=area0, start_length=L0_0)
    # Convert to positive
    # strain0 = [-i for i in strain0]
    strain1 = [-i for i in strain1]
    # stress0 = [-i for i in stress0]
    stress1 = [-i for i in stress1]
    plot_compression_data(time0, strain0, stress0, plot_title="5 MPa cube at 100k cycle", file_name="./5000kPa001SA006SP_100k_cycle.png")
    
    
    # plot_zoomed_compression_data(col1, col2, col3)
    # s_col1 = s_rows.iloc[:, 1].astype(float)
    # s_col2 = s_rows.iloc[:, 2].astype(float)
    # print(type(s_rows))
    # print(s_rows)
    # plot_specific_compression_data(s_col1, s_col2)