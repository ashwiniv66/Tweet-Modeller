class GetHandlers(object):
    def get_twitter_handlers(self, topic):
        if topic == "Health":
            return [
                "bbchealth",
                "HarvardHealth",
                "StanfordMed",
                "NatureMedicine",
                "healthmagazine",
                "WHO",
                "HarvardChanSPH",
            ]

        else:
            return [
                "bbchealth",
                "HarvardHealth",
                "StanfordMed",
                "NatureMedicine",
                "healthmagazine",
                "WHO",
                "HarvardChanSPH",
            ]