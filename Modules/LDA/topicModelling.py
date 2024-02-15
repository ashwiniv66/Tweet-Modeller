from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

import tempDataReader as getData

import os
import logging


def topicModel(selected_topic):

    path_to_result = os.path.join("Data\\Result", selected_topic)
    os.mkdir(path_to_result)

    logging.info("Starting topic Modelling")

    tweetDataSet = getData.read_csv(selected_topic)

    print("...........Starting count Vectorizer..........")
    cv = CountVectorizer(max_df=0.9, min_df=2, stop_words="english")
    dtm = cv.fit_transform(tweetDataSet["Tweets"])
    print("...........Ending count Vectorizer..........")

    print("...........Starting LDA..............")
    LDA = LatentDirichletAllocation(n_components=10)
    LDA.fit(dtm)
    topicResult = LDA.transform(dtm)
    print("...........Ending LDA..............")

    print("............Starting to write topic..x..word results.........")

    for i, topic in enumerate(LDA.components_):
        tempStringList = []
        tempStringList.append(f"For topic {i+1} the top 15 words are:\n")
        topFifteenWords = [cv.get_feature_names()[idx] for idx in topic.argsort()[-15:]]
        for rank, word in enumerate(topFifteenWords):
            tempStringList.append(f"{rank}) {word}\n")
        with open(f".\\Data\\Result\\{selected_topic}\\{i+1}.txt", "w") as fhandler:
            fhandler.writelines(tempStringList)

    print("............Ending writing results.........")

    print("..........Starting to write topic..x..articles results............")

    tweetDataSet["Topic"] = topicResult.argmax(axis=1) + 1
    tweetDataSet.to_csv(path_to_result + f"\\{selected_topic}.csv", index=False)

    print("............Ending writing results.........")