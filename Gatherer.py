import GameScheduler, time, requests
'''
Gatherer class gathers all the json payload for a given gamePK, each payload is timestamped.
This is because Gatherer should end a game with a timestamped payload every 30 seconds due to 
changing game conditions as game persists to regulation final. 
to be used by a controller that calls Gatherer's set_payload_entry function, until gamestate = Final

@brief Gatherer: Abstract Data Type - contains gamePk payloads
@detail each gamePk (reps an NHL game) will have a Gatherer ADT for each

'''

class Gatherer:

    def set_payload_entry(self):

        timestamp = time.time()
        # convert to datetime
        date_time = datetime.fromtimestamp(timestamp)
        # convert timestamp to string in HH:MM:SS
        str_time = date_time.strftime("%H:%M:%S")

        self.payloads.setdefault(str_time, self.get_payload())

    def get_payload(self):
        return GameScheduler.get_json(self.gamePk_url)

    '''
    @brief gamestate_check returns the state of a given gamePk
    @detail returns string value of abstractGameState field from schedule payload'''
    @staticmethod
    def get_gamestate(gamePk, url):
        data = Gatherer.get_json(url)
        for i in range(0, data["dates"][0]["totalGames"]):
            if (data["dates"][0]["games"][i]["gamePk"] == gamePk):
                return data["dates"][0]["games"][i]["status"]["abstractGameState"]
            else:
                continue
    '''
    @brief static method that takes as argument an NHL API return url containing json
    @detail arg ex:  "https://statsapi.web.nhl.com/api/v1/game/2021020292/boxscore"
    @detail staticmethod allows access outside of class instance
    '''
    @staticmethod
    def get_json(NHL_url):
        #'response' type: request.modles.Reponse
        response = requests.get(NHL_url)
        #type(data) == dict
        data = response.json()
        return data

    def __init__(self, gamePk, gamePk_url, schedule_url):
        self.gamePk = gamePk
        self.gamePk_url = gamePk_url
        self.schedule_url = schedule_url
        #gamestate is coming from the schedule landing page, not the game specific boxscore
        self.gamestate = Gatherer.get_gamestate(self.gamePk, self.schedule_url) #may need to set as unknown on init - tbd
        self.payloads = {}
        self.is_active = False
