# VTP Compression Durability Analysis
import pandas as pd
import matplotlib.pyplot as plt


def load_file():
    # Given csv filename, get database
    file_path = '../data/0500_kPa_sample_003_20250305_1000cycles.csv'  # Replace with file path
    # Read the CSV and skip the first two rows
    df = pd.read_csv(file_path, skiprows=2)
    # Check the data
    print(df.head())
    # Convert columns to plottable data types
    col1 = df.iloc[:, 0].astype(float)  # First column as floats
    col2 = df.iloc[:, 1].astype(float)  # Second column as floats
    col3 = df.iloc[:, 2].astype(float)  # Third column as floats
    return col1, col2, col3

def plot_data(col1, col2, col3):
    plt.figure(figsize=(8, 6))
    plt.plot(col2, col3)
    plt.legend()
    plt.xlabel('Index')
    plt.ylabel('Values')
    plt.title('Plot of Three Columns')
    plt.show()


if __name__ == '__main__':
    col1, col2, col3 = load_file()
    plot_data(col1, col2, col3)