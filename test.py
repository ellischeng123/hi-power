import pandas as pd

LIV_FILE = r"C:\Users\EC\workspace\py-workspace\hi-power\samples\LIV\2023_01_04_15_25_14.csv"
SPEC_FILE = r"C:\Users\EC\workspace\py-workspace\hi-power\samples\spectrum\han2006_HRD27891__0__15-48-07-350.txt"

if __name__ == '__main__':
    # spec = pd.read_table(filepath_or_buffer=SPEC_FILE, skiprows=[0, 1], names=['wl_p', 'value'])

    # print(spec['wl_p'][spec.idxmax()["value"]])

    liv = pd.read_csv(filepath_or_buffer=LIV_FILE, skiprows=[0, 1], names=['TCA', 'A', 'V', 'L', 'C'])
    low = liv.iloc[(liv['L'] - 6).abs().argsort()[:1]]
    high = liv.iloc[(liv['L'] - 9).abs().argsort()[:1]]

    print(liv)
    print(low)
    print(high)

    low_a = low['A'].values[0]
