import functools
import pandas as pd
import os
from datetime import datetime
import json

class _CachingTestingCSV:
    def __init__(self, func, filename=None):
        # functools.update_wrapper(self, func)
        self.__filename = filename 
        self.__func = func

    def __call__(self, *args, **kwargs):
        print(kwargs)
        print(args)

        curArgs = kwargs.get('caching_testing_args', None)
        kwargs.pop('caching_testing_args', None)

        # If testing, load the cached files with desirable tested date
        if curArgs and curArgs.testing:
            print("Start testing")
            with open(os.path.join(curArgs.testing, f"{self.__filename}_{curArgs.testing_date}_types.json"), "r") as fp:
                recover_types = json.load(fp)
            return pd.read_csv(os.path.join(curArgs.testing, f"{self.__filename}_{curArgs.testing_date}.csv"), 
                               index_col=0).astype(recover_types)
        
        result = self.__func(*args, **kwargs)

        # If args.cached, then cache. Currently only support pandas dataframe
        if isinstance(result, pd.DataFrame) and curArgs and curArgs.cached:
            print("Start caching")
            result.to_csv(os.path.join(curArgs.cached, f"{self.__filename}_{datetime.now().strftime('%Y%m%d')}.csv"))
            with open(os.path.join(curArgs.cached, f"{self.__filename}_{datetime.now().strftime('%Y%m%d')}_types.json"), "w") as fp:
                json.dump(result.dtypes.apply(lambda x: x.name).to_dict(), fp)

        return result
    
# Need another wrapper to return the object
def CachingTestingCSV(filename=None):
    def wrapper(function):
        return _CachingTestingCSV(function, filename) 
    return wrapper