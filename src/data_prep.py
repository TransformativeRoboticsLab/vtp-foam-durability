# For data preparation from Instron
# VTP Compression Durability Analysis
# Jacob Miske
import pandas as pd
import matplotlib.pyplot as plt

def prep_compression_data(filename):
    """
    Given a filename, check order of force and displacement and zero point
    """
    df = pd.read_csv(filename,header=None)         # read file
    # df = df.drop(df.index[4::2])                 # drop every 2nd row
    # Convert displacment and force to negative numbers
    df[1] *= -1
    df[2] *= -1
    df.to_csv(filename[:-4] + "prepped.csv",index=None,header=None)     # save file
    return


def get_halved_csv_file(filename):
    """
    Given a filename, cut every other line and resave
    """
    df = pd.read_csv(filename,header=None)         # read file
    df = df.drop(df.index[4::2])                     # drop every 2nd rows
    df.to_csv(filename[:39] + "test.csv",index=None,header=None)     # save file


if __name__ == '__main__':
    prep_compression_data(filename="../data/100kcycle_0500MPa_1.csv")
