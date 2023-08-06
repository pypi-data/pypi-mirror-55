import os
import pandas as pd
import pickle
import gzip
from typing import Dict, Union, Any


def _load_data(prefix: str, name: str) -> Union[pd.DataFrame, Dict[str, Any]]:
    p = os.path.join(os.path.dirname(__file__), 'res', prefix, '{}.pkl.gz'.format(name))
    with gzip.open(p, mode='rb') as f:
        return pickle.load(f)
