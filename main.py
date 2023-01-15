import os
import subprocess
import tomllib

import pandas as pd
from decimal import *

HEADER = 'Lookup Low,Lookup High,WL_P,Low A,High A,Low V,High V,Slope\n'
CONFIG = dict()
CONFIG_DICT = {
    'spectrum_dir': 'Enter SPECTRUM files storage dir: ',
    'liv_dir': 'Enter LIV files storage dir: ',
    'target_dir': 'Enter the path you wish to save the result file: '
}


def setup():
    global CONFIG
    getcontext().rounding = ROUND_FLOOR

    if os.path.exists('./config.toml'):
        with open('./config.toml', mode='rb') as cfile:
            CONFIG = tomllib.load(cfile)

    ask_vars()


def ask_vars():
    print(CONFIG)
    existing_configs = set(CONFIG.keys())
    config_keys = set(CONFIG_DICT.keys())

    if not existing_configs >= config_keys:
        for key in config_keys - existing_configs:
            CONFIG[key] = os.path.abspath(input(CONFIG_DICT[key]))

    if CONFIG.get('lookup_low') is None:
        CONFIG['lookup_low'] = int(input("Enter lookup low value: "))

    if CONFIG.get('lookup_high') is None:
        CONFIG['lookup_high'] = int(input("Enter lookup high value: "))


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
    setup()

    spectrum_files = os.listdir(CONFIG['spectrum_dir'])
    liv_files = os.listdir(CONFIG['liv_dir'])

    if len(spectrum_files) != len(liv_files):
        raise RuntimeError('Spectrum files count and LIV files count not match.')

    target_dir = os.path.abspath(CONFIG['target_dir'])
    target_file = os.path.join(CONFIG['target_dir'], 'result.csv')
    lookup_low = CONFIG['lookup_low']
    lookup_high = CONFIG['lookup_high']

    spectrum_files.sort()
    liv_files.sort()

    spectrum_files_abs_path = [os.path.join(CONFIG['spectrum_dir'], file) for file in spectrum_files]
    liv_files_abs_path = [os.path.join(CONFIG['liv_dir'], file) for file in liv_files]

    process_files(target_file, spectrum_files_abs_path, liv_files_abs_path, lookup_low, lookup_high)

    input(f"Job done, check result in {target_dir}")
    input("Result folder will be opened after you hit ENTER")
    subprocess.Popen(f"explorer {target_dir}")


if __name__ == '__main__':
    main()
