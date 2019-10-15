"""
Task:
The peak memory usage of this script is too high and runs out of memory on users machines.

How can you fix the memory usage without breaking the test?
You should be able to relatively easily reduce the memory usage by _at least_ 25%
"""
import gc
import io
import pickle

# import deep as deep
from pandas.util import hash_pandas_object
import pandas as pd
import numpy as np
import hashlib
import typing
import random
import sys
from functools import reduce
# import pyarrow.parquet as pq
from memory_profiler import profile

# Deterministic randomness for the assert at the end
random.seed(42)

precision = 5
TRANSFORMS = 10
ROWS = 20000000
CHUNK = 2000
# splitting the iterable array in chunks
DATA = (random.random() for _ in range(ROWS))
res = np.fromiter(DATA, np.float)
res = np.array_split(res, CHUNK)


# print(sys.getsizeof(res), type(res), res[:10])


class Transform:
    """A transform that adds a column of random data"""

    def __init__(self, var: str):
        self.var = var

    # returns new numpy array with data
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_new = pd.DataFrame()
        df_new[self.var] = res
        print(sys.getsizeof(res), type(res), res[:10])
        # df_new.info()
        # print(df_new.head(), sys.getsizeof(df_new), type(df_new))
        print(self.var)
        return df_new


class Pipeline:

    def __init__(self):
        self.df = pd.DataFrame()
        self.df2 = pd.DataFrame()
        self.li = []
        self.transforms = [
            Transform(f'v{i}') for i in range(TRANSFORMS)
        ]

    def run(self):
        for t in self.transforms:
            # self.li.append(t.transform(self.df))
            self.df2 = pd.concat((self.df2, t.transform(self.df)), axis=1)
            # self.df2.info()

            # pickling
            with open('concat_df.pkl', 'wb') as f:
                pickle.dump(self.df2, f)

            print("pickled successfully")

            del self.df2
            gc.collect()

            # unpickling
            with open('concat_df.pkl', 'rb') as f:
                self.df2 = pickle.load(f)
            print("un pickled successfully")

            gc.collect()
        return self.df2


if __name__ == '__main__':
    pipe = Pipeline()
    df_list = pipe.run()
    df_list.info()

    # pickiling
    with open('pipeline_list.pkl', 'wb') as f:
        pickle.dump(df_list, f)

    print("pickled successfully")
    # explicit garbage collection
    del df_list
    gc.collect()

    # unpickling
    with open('pipeline_list.pkl', 'rb') as f:
        df = pickle.load(f)
    print("un pickled successfully")

    df.to_csv('big_df.csv')

    # np.savez_compressed('123', a=df_list)
    # del df_list
    # gc.collect()
    # print("pik")
    # df_list = np.load('123.npz')
    # print("unpik")

    # dfs = (d for d in df_list)
    # df = pd.concat(dfs, axis=1)
    # df = reduce(lambda df1, df2: (pd.merge(df1, df2)), dfs)
    # df = reduce(lambda df1, df2: (pd.merge(np.load(df1.values[0]), np.load(df2.values[0])), gc.collect()), dfs)
    # df = reduce(lambda df1, df2: load_array(df1, df2), dfs)
    # del df_list
    # del dfs
    # df = tuple(df)

    # Dont break the test
    assert hashlib.sha256(pd.util.hash_pandas_object(df,
                                                     index=True).values).hexdigest() == '867567dc7d46f77af2bca9804ac366a5165d27612de100461b699bd23094ab90'
