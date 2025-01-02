import pandas as pd
import os
import json
from decorator import CachingTestingCSV


# Testing the types storage
# TESTING_DIR = r"D:\Python\testingDecorator\loading"
# data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"], "col3": ["NaN", "NaN", "NaN"]}
# df = pd.DataFrame(data=data)
# print(df.dtypes)
# print(type(df.dtypes))
# print(df["col3"].str.upper())

# df.to_csv(os.path.join(TESTING_DIR, "myDf.csv"))
# with open(os.path.join(TESTING_DIR, "myTypes.json"), "w") as fp:
#     json.dump(df.dtypes.apply(lambda x: x.name).to_dict(), fp)
# print(df.dtypes)

# recover_df = pd.read_csv(os.path.join(TESTING_DIR, "myDf.csv"))
# with open(os.path.join(TESTING_DIR, "myTypes.json"), "r") as fp:
#     recover_types = json.load(fp)

# print(recover_types)
# recover_df = recover_df.astype(recover_types)
# print(recover_df.dtypes)
# print(recover_df["col3"].str.upper())

class mockArgs:
    def __init__(self, cached=None, testing=None, testing_date=None):
        self.cached = cached
        self.testing = testing
        self.testing_date = testing_date


@CachingTestingCSV(filename="myLoadStuff")
def loadStuff():
    df = pd.read_csv(r"D:\Python\testingDecorator\loading\myDf.csv", index_col=0)
    with open(r"D:\Python\testingDecorator\loading\myTypes.json", "r") as fp:
        df_types = json.load(fp)
    df = df.astype(df_types)
    return df

if __name__ == "__main__":
    myCachedArgs = mockArgs(cached=r"D:\Python\testingDecorator\testing")
    myTestArgs = mockArgs(testing=r"D:\Python\testingDecorator\testing", testing_date="20241227")

    loadStuff(caching_testing_args=myCachedArgs)

    print(loadStuff(caching_testing_args=myTestArgs))

    # Try backward-compatibility
    print(loadStuff())
    print(help(loadStuff))
