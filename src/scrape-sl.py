import json
import requests

class TVChannel:
    def __init__(self):
        self._name = None
        self._logo = None
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
    def name(self):
        return self._name
    def logo(self):
        return self._logo

class SLMatch:

    def __init__(self):
        self._homeShort = None
        self._awayShort = None
        self._homeName = None
        self._awayName = None
        self._startdate = None
        self._tvchannel = TVChannel()
   
    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def homeShort(self):
        return self._homeShort
    def awayShort(self):
        return self._awayShort
    def tvChannel(self):
        return self._tvchannel

def getRoundId():
    seaeson_api = "https://api.superliga.dk/tournaments/46/season?appName=superligadk&access_token=5b6ab6f5eb84c60031bbbd24&env=production&seasonId=23624&locale=da"
    season_response = requests.get(seaeson_api)
    roundId = None
    seasonId = None
    if season_response.status_code == 200:
        season_json = season_response.json()
        seasonId = season_json["season"]["id"]
        #for item in season_json:
        #   print(item)
        roundslist = season_json["season"]["stages"][0]["roundsList"]
        for sl_round in roundslist:
            if sl_round["status"] == "inprogress":
                roundId = sl_round["name"]
    else:
        raise Exception("Could not get season information from API")

    if roundId is None or seasonId is None:
        raise Exception("Cound not find round ID")

    return roundId, seasonId


def getmatches(roundId, seasonId):
    matchList = []
    matches_url_str = "https://api.superliga.dk/events-v2?appName=dk.releaze.livecenter.spdk&access_token=5b6ab6f5eb84c60031bbbd24&env=production&locale=da&ttId=46&round={0}&seasonId={1}"
    matches_url = matches_url_str.format(roundId,seasonId)
    matches_response = requests.get(matches_url)

    if matches_response.status_code == 200:
        matches_json = matches_response.json()
        for event in matches_json["events"]:
            m = SLMatch()
            c = TVChannel()
            m.homeName = event["homeName"]
            m.awayName = event["awayName"]
            c.name = event["channel"]["name"]
            c.logo = event["channel"]["logoUrl"]
            m.tvChannel = c
            matchList.append(m)
            #print(event["homeName"] + " " + event["awayName"])

    return matchList


if __name__ == '__main__':
    roundId, seasonId = getRoundId()
    #print(roundId)
    matches = getmatches(roundId,seasonId)
    for m in matches:
        print(m)
    

    



