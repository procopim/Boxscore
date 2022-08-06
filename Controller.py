#!/usr/bin/env python
import GameScheduler, Gatherer, nhlURLmaker

if __name__ == "__main__":
    main()

def main():

    todays_date = nhlURLmaker.todays_date()
    todays_url = nhlURLmaker.api_url_maker()
    #create GameSchedule object, which contains the day's gamePKs and corresponding boxscore URL
    Schedule = GameScheduler(todays_url)
    Game_urls_to_hit = Schedule.boxscore_urls # a list
    Games = Schedule.gamePks #a list 

    #globals; keep in mind you have global vars for every gamePk
    end_of_night_flag = False
    global_game_cnt = len(Games)

    
    #create Gatherer objects for each game in the schedule
    game_dict = {}
    for gameID,gameURL in zip(Games,Game_urls_to_hit):
        #exec func executes the string, which is formatted using str.format method
        exec("{0}={1}".format(game_dict[gameID],Gatherer(gameID,gameURL,todays_url)))
    
    #capture game payload every 30 secs until game is Final
        
    try:
        while not end_of_night_flag == False:
            #each gameID is a variable in memory with its GATHERER obj as value; so loop through them and check gamestate
            for game in Games:
                if not game.gamestate == "Final":    
                    game.is_active == True
                    game.set_payload_entry()
                
                #game is Final
                game.is_active = False
                Games.pop()
                global_game_cnt+-=1
            
            if global_game_cnt == 0:
                end_of_night_flag == False
            
    except:
        print "something went wrong"  
