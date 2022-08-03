#!/usr/bin/env python
import GameScheduler, Gatherer, nhlURLmaker.py

if __name__ == "__main__":
    main()

def main():
    todays_date = nhlURLmaker.todays_date()
    todays_url = nhlURLmaker.api_url_maker()
    #GameScheduler = GameScheduler()
