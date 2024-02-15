import pandas as pd

from os import listdir
import sys

sys.path.append("TwitterAPI")
import get_handlers as GetHandlers
    

def read_csv(topic):

    twitter_handlers = GetHandlers.GetHandlers().get_twitter_handlers(topic)

    df = None

    for tweeter_handle in twitter_handlers:

        print("...STARTING TO FETCH DATA OF {}......".format(tweeter_handle))

        # Read Sample CSV file
        pathOfHT = "./Data/Fetched/{}/tweets/{}.csv".format(
            tweeter_handle, tweeter_handle
        )
        df_temp = pd.read_csv(pathOfHT)

        df_temp = pipe_translated_videos(df_temp,tweeter_handle)

        print("...FINISHED FETCHING DATA OF {}......".format(tweeter_handle))

        if df is None:
            df = df_temp.copy()
        else:
            df = df.append(df_temp, ignore_index=True)

    return df

def pipe_translated_videos(df,tweeter_handler):
    path = f"./Data/Text_translated/{tweeter_handler}"
    transalted_list = list(listdir(path))
    if(len(transalted_list)== 0):
        return df
    for index_unparsed in transalted_list:
        with open(path+f"//{index_unparsed}","r") as f:
            lines = f.readlines()
            index_parsed = int(index_unparsed[:-4])
            df.loc[index_parsed,'Tweets'] = df.loc[index_parsed,'Tweets'] + "".join(lines)
    return df
