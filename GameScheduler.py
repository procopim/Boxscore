#!/usr/bin/env python
import re, requests, json
'''
@brief GameScheduler: Abstract Object that acts as source of game day identification
@details contains a list of the day's gamePKs, and a list of created URLs to those gamePK payloads. 
@detail init args: valid NHL API schedule link that begins with "https://statsapi.web.nhl.com/api/v1/schedule"
@detail package dependencies: re, requests, json
'''

class GameScheduler:
    '''
    @brief GameScheduler Constructor: arg must be valid NHL API schedule
    @detail dependency: regex
    @detail types:  date::str; url::str; gamePks::unordered-list(str); boxscore_urls::unordered-list(str)
    '''
    def __init__(self, url):
        '''checks if url is valid'''
        match = re.match("https://statsapi.web.nhl.com/api/v1/schedule", url)
        if match:
            self.url = url
        else:
            raise Exception("not a valid NHL API daily schedule link")

        self.date = self.__get_date(url)
        self.gamePks = self.__game_id_parser(url)
        self.boxscore_urls = self.__boxscore_url_builder(self.gamePks)
   
    '''
    @brief private Function to return date string from NHL API daily schedule URL
    '''
    def __get_date(self, url):
        match = re.search("date=.+", url)
        return match.string.split("date=")[1]
    
    '''
    @brief private Function that returns a list of game IDs 
    @details Game IDs are derived from GamePk field, within [dates][games] hierarchy
    @details arg: nhl api daily schedule, e.g. https://statsapi.web.nhl.com/api/v1/schedule?date=2021-11-24
    '''
    def __game_id_parser(self, schedule_link):
        
        #add in error detection if NOT a valie schedule link
        schedule_dict = GameScheduler.get_json(schedule_link)
        # index 0 is where the lone dict is, within list 
        schedule_dict2 = schedule_dict["dates"][0] 
        #dict of all GamePks i.e. Game IDs, for that night
        games_dict = schedule_dict2["games"] 

        gameID_list = []
        for i in games_dict:

            gameID_list.append(i["gamePk"])

        return gameID_list

    '''
    * @brief private Function that returns a list of string URLs
    * @details URLs are boxscores for a given NHL game
    * @details items in list returned as string e.g. https://statsapi.web.nhl.com/api/v1/game/2021020292/boxscore
    '''
    def __boxscore_url_builder(self, gamePk_list):
        template_url =  "https://statsapi.web.nhl.com/api/v1/game/"

        boxscore_url_list = []

        for ID in gamePk_list:
            boxscore_url_list.append(template_url+str(ID)+"/boxscore")

        return boxscore_url_list
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