import os
import tomllib
import pandas as pd

LIV_FILE = r"C:\Users\EC\workspace\py-workspace\hi-power\samples\LIV\2023_01_04_15_25_14.csv"
SPEC_FILE = r"C:\Users\EC\workspace\py-workspace\hi-power\samples\spectrum\han2006_HRD27891__0__15-48-07-350.txt"

if __name__ == '__main__':
    if os.path.exists('./config.toml'):
        with open('./config.toml', mode='rb') as cfile:
            CONFIG = tomllib.load(cfile)

    print(CONFIG)
    config_keys = {
        'spectrum_dir',
        # 'liv_dir',
        # 'target_dir'
    }

    existing_keys = set(CONFIG.keys())

    print(existing_keys >= config_keys)

