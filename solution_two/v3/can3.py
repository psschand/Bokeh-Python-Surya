"""
Task:
The peak memory usage of this script is too high and runs out of memory on users machines.

How can you fix the memory usage without breaking the test?
You should be able to relatively easily reduce the memory usage by _at least_ 25%
"""
import gc
import io
import pickle
from pandas.util import hash_pandas_object
import pandas as pd
import numpy as np
import hashlib
import typing
import random
import sys
from functools import reduce
from io import StringIO, BytesIO
from memory_profiler import profile

# Deterministic randomness for the assert at the end
random.seed(42)

precision = 5
TRANSFORMS = 10
ROWS = 20000000
DATA = (random.random() for _ in range(ROWS))

res = np.fromiter(DATA, np.float)

compressed_array = io.BytesIO()  # np.savez_compressed() requires a file-like object to write to
np.savez_compressed(compressed_array, res)


#
# def update_df(df_orig: pd.DataFrame, df_new: pd.DataFrame) -> pd.DataFrame:
#     return pd.concat((df_orig, df_new), axis=1)

def load_array(df1, df2):

    s_buf = io.StringIO()
    # saving a data frame to a buffer (same as with a regular file):
    df1['id'].to_csv(s_buf)
    s_buf.seek(0)

    s2_buf = io.StringIO()
    # saving a data frame to a buffer (same as with a regular file):
    df2['id'].to_csv(s2_buf)
    s2_buf.seek(0)

    compressed_1 = s_buf
    compressed_2 = s2_buf

    compressed_1.seek(0)  # seek back to the beginning of the file-like object
    compressed_2.seek(0)

    decompressed_df1 = np.load(compressed_1)['arr_0']
    decompressed_df2 = np.load(compressed_2)['arr_0']

    return pd.merge(decompressed_df1, decompressed_df2)


class Transform:
    """A transform that adds a column of random data"""

    def __init__(self, var: str):
        self.var = var

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        # df_new = pd.DataFrame({'id': compressed_array}, dtype=object)
        df_new = pd.DataFrame()
        df_new['id'] = compressed_array
        print("-------------------------start-------------------------------------")
        print(res.shape, sys.getsizeof(compressed_array), type(compressed_array))
        print(sys.getsizeof(df_new), type(df_new), df_new.dtypes)
        df_new.info()
        print("############")
        print(df_new.head())
        print("--------------------------end--------------------------------------")

        return df_new


class Pipeline:

    def __init__(self):
        self.df = pd.DataFrame()
        self.li = []
        self.transforms = [
            Transform(f'v{i}') for i in range(TRANSFORMS)
        ]

    def run(self):
        for t in self.transforms:
            self.li.append(t.transform(self.df))
            gc.collect()
        return self.li


if __name__ == '__main__':
    pipe = Pipeline()
    df_list = pipe.run()

    # pickiling
    with open('pipeline_list.pkl', 'wb') as f:
        pickle.dump(df_list, f)

    del df_list
    gc.collect()

    # unpickling
    with open('pipeline_list.pkl', 'rb') as f:
        df_list = pickle.load(f)

    dfs = (d for d in df_list)

    # df = pd.concat(dfs, axis=1)
    # df = reduce(lambda df1, df2: (pd.merge(np.load(df1.values[0]), np.load(df2.values[0])), gc.collect()), dfs)
    df = reduce(lambda df1, df2: load_array(df1, df2), dfs)
    del df_list
    del dfs

    # Dont break the test
    assert hashlib.sha256(pd.util.hash_pandas_object(df,
                                                     index=True).values).hexdigest() == '867567dc7d46f77af2bca9804ac366a5165d27612de100461b699bd23094ab90'
