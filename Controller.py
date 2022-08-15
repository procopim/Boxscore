#!/usr/bin/env python
import traceback
import GameScheduler, Gatherer, nhlURLmaker, time

def main():
    print "Begin NHL Game payload collection service..."
    #todays_date = nhlURLmaker.todays_date() #commented out for testing purposes:
    todays_date = "2022-03-24"
    print "today's date: {}".format(todays_date)
    todays_url = nhlURLmaker.api_url_maker(todays_date)
    print "today's URL: {}".format(todays_url)
    #create GameSchedule object, which contains the day's gamePKs and corresponding boxscore URL
    Schedule = GameScheduler.GameScheduler(todays_url)
    Game_urls_to_hit = Schedule.boxscore_urls # a list
    Games = Schedule.gamePks #a list 

    #globals; keep in mind you have global vars for every gamePk
    end_of_night_flag = None
    global_game_cnt = len(Games)

    
    #create Gatherer objects for each game in the schedule
    game_dict = {}
    print "creating gatherer objects for all games... "
    for gameID in Games:
        game_dict[gameID] = None 
    for gameID, gameURL in zip(Games,Game_urls_to_hit):
        #exec func executes the string, which is formatted using str.format method
        game_dict[gameID] = Gatherer.Gatherer(gameID,gameURL,todays_url)
        check = lambda v: v if game_dict.__contains__(v) else "Error"
        print "object created with game ID: {0}, and game URL: {1}".format(check(gameID),game_dict[gameID].gamePk_url)      

    while not end_of_night_flag == True:
        #time.sleep(25) #capture game payload every 30 secs until game is Final
        try:
            #each gameID is a variable in memory with its GATHERER obj as value; so loop through them and check gamestate
            print "active games remaining: {}".format(global_game_cnt)
            for game in Games:
                time.sleep(1)
                if not game_dict[game].gamestate == "Final":    
                    game_dict[game].is_active == True
                    game_dict[game].set_payload_entry()
                    print "gameID: {} is still ongoing".format(game)
                
                #game is Final
                game_dict[game].is_active = False
                Games.pop()
                global_game_cnt-=1
                print "gameID: {} has ended".format(game)
            
            if global_game_cnt == 0:
                end_of_night_flag = True
            #print "active games remaining: {}".format(global_game_cnt)
        except Exception:
            traceback.print_exc()
            #print "something went wrong"  

if __name__ == "__main__":
    main()