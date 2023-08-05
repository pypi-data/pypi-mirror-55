import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tests import utils
from cloudnetpy.instruments import ceilo2nc


source_path = f"{utils.get_test_path()}/source_data/vaisala_ceilo/"

for file in os.listdir(source_path):
    print(file)
    ceilo2nc(source_path + file, 'ceilo.nc', {'name': 'Foo', 'altitude': 20})
