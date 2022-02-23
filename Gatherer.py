'''
to be used by a controller that calls Gatherer's set_payload_entry function, until gamestate = Final

@brief Gatherer: Abstract Data Type - contains gamePk payloads
@detail each gamePk (reps an NHL game) will have a Gatherer ADT for each

'''

class Gatherer:
    import time       
        
    def get_gamestate(self):
        self.gamestate = GameScheduler.get_gamestate(self.gamePk, self.schedule_url)
        return self.gamestate

    def set_payload_entry(self):

        timestamp = time.time()
        # convert to datetime
        date_time = datetime.fromtimestamp(timestamp)
        # convert timestamp to string in HH:MM:SS
        str_time = date_time.strftime("%H:%M:%S")

        self.payloads.setdefault(str_time, self.get_payload())

    def get_payload(self):
        return GameScheduler.get_json(self.gamePk_url)
        
    def __init__(self, gamePk, gamePk_url, schedule_url):
        self.gamePk = gamePk
        self.gamePk_url = gamePk_url
        self.schedule_url = schedule_url
        self.gamestate = self.get_gamestate()
        self.payloads = {}   