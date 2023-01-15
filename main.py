import os
import subprocess

import pandas as pd
from decimal import *

HEADER = 'Lookup Low,Lookup High,WL_P,Low A,High A,Low V,High V,Slope\n'

# 比對兩個資料夾下檔案數量，若不相符則不執行並印出警告
# 取得檔案清單後先依檔名也就是時間排序，之後再依順序配對
# 輸出 csv sample:


def process_files(target_file: str, specs: list[str], livs: list[str], l_low: int, l_high: int):
    with open(target_file, mode='w') as target:
        target.write(HEADER)
        for idx, spec in enumerate(specs):
            result = calculate(spec, livs[idx], l_low, l_high)
            target.write(result)


def calculate(spec_file: str, liv_file: str, l_low: int, l_high: int):

    spec = pd.read_table(filepath_or_buffer=spec_file, skiprows=[0, 1], names=['wl_p', 'value'])
    wl_p = spec['wl_p'][spec.idxmax()["value"]]
    # print(f"WL_P: {wl_p}")

    liv = pd.read_csv(filepath_or_buffer=liv_file, skiprows=[0, 1], names=['TCA', 'A', 'V', 'L', 'C'])
    low = liv.iloc[(liv['L'] - l_low).abs().argsort()[:1]]
    high = liv.iloc[(liv['L'] - l_high).abs().argsort()[:1]]

    low_a = low['A'].values[0]
    # print(f"Low A: {low_a}")

    high_a = high['A'].values[0]
    # print(f"High A: {high_a}")

    low_v = low['V'].values[0]
    # print(f"Low V: {low_v}")

    high_v = high['V'].values[0]
    # print(f"High V: {high_v}")

    if not low['L'].values[0] == high['L'].values[0]:
        slope = (Decimal(high['L'].values[0]) - Decimal(low['L'].values[0])) / \
                (Decimal(high['A'].values[0]) - Decimal(low['A'].values[0]))
    else:
        slope = 0

    # print(f'slope: {slope : .3f}')

    return f"{l_low},{l_high},{wl_p},{low_a},{high_a},{low_v},{high_v},{slope}\n"


def main():
    getcontext().rounding = ROUND_FLOOR

    spectrum_dir = os.path.abspath(input("Enter SPECTRUM files storage dir: "))
    # spectrum_dir = os.path.abspath('./samples/spectrum')
    print(spectrum_dir)
    print()
    liv_dir = os.path.abspath(input("Enter LIV files storage dir: "))
    # liv_dir = os.path.abspath('./samples/LIV')
    print(liv_dir)
    print()

    spectrum_files = os.listdir(spectrum_dir)
    # print(spectrum_files)

    liv_files = os.listdir(liv_dir)
    # print(liv_files)

    if len(spectrum_files) != len(liv_files):
        raise RuntimeError('Spectrum files count and LIV files count not match.')

    target_dir = os.path.abspath(input("Enter the file with path you wish to save the result file: "))
    # target_dir = os.path.abspath('./samples')
    target_file = os.path.join(target_dir, 'result.csv')
    print()

    lookup_low = int(input('lookup_low: '))
    # lookup_low = 6
    print()

    lookup_high = int(input('lookup_high: '))
    # lookup_high = 9
    print()

    spectrum_files.sort()
    liv_files.sort()

    spectrum_files_abs_path = [os.path.join(spectrum_dir, file) for file in spectrum_files]
    liv_files_abs_path = [os.path.join(liv_dir, file) for file in liv_files]

    process_files(target_file, spectrum_files_abs_path, liv_files_abs_path, lookup_low, lookup_high)

    input(f"Job done, check result in {target_dir}")
    input("Result folder will be opened after you hit ENTER")
    subprocess.Popen(f'explorer {target_dir}')


if __name__ == '__main__':
    main()
