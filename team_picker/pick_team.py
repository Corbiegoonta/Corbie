from send_whatsapp.src import sender, utils
from dotenv import load_dotenv
import numpy as np
import pandas as pd
import os
import argparse
import random
import datetime




def retrieve_players():
    df = load_player_data()
    players = df["player_name"].tolist()
    print(players)

    return players

def retrieve_win_rates(list_of_players: list):
    df = load_player_data()
    win_rates = []
    for player in list_of_players:
        win_rates.append(df.loc[df['player_name'] == player, 'points_win_rate'].values[0]) 
    print(win_rates)

    return win_rates

def init_player_data():
    # df = load_player_data()
    df = dict()
    df["player_name"] = []
    df["wins"] = []
    df["losses"] = []
    df["draws"] = []
    df["win_rate"] = []
    df["number_of_games_played"] = []
    df = pd.DataFrame(df)
    df.to_csv('player_info.csv', index=False)

def init_team_data():
    df = pd.DataFrame(columns=["team_coloured", "team_white"])
    df.to_csv('team_info.csv', index=False)

def init_weekly_player_list():
    df = pd.DataFrame(columns=["player_name"])
    df.to_csv('list_of_players.csv', index=False)
    pass

def load_weekly_players():
    df = pd.read_csv('list_of_players.csv')
    weekly_players = df["player_name"].tolist()
    return weekly_players

def load_player_data():
    df = pd.read_csv('player_info.csv')
    print(df)
    return df

def add_player(player_name: str):
    df = load_player_data()
    print("add_player")
    print(df.loc[df.index.max()])
    df.loc[df.index.max()+1] = [player_name, 0, 0, 0, 0, 0, 0, 0]
    # print(df.loc[df.index.max()+1])
    # df.append({'player_name':player_name, 'wins':0, 'losses':0, 'draws':0, 'win_rate':0, 'number_of_games_played':0, 'points':0, 'points_win_rate':0}, ignore_index=True)
    print(df)
    df.to_csv('player_info.csv', index=False)
    # df["player_name"] = player_name
    pass

def remove_player(player_name: str):
    df = load_player_data()
    df.loc[df['player_name'] == player_name] = None
    df.to_csv('player_info.csv', index=False)

def store_teams(team_1=[], team_2=[]):
    df = pd.DataFrame(columns=["team_1", "team_2"])
    df["team_1"] = team_1
    df["team_2"] = team_2
    df.to_csv('team_players.csv', index=False)
    pass

def get_player_stats(player_name: str):
    df = pd.read_csv('player_info.csv')
    player_stats = df.loc[df['player_name'] == player_name]
    print(f"Player Name: {player_name}\nWins: {player_stats['wins'].values[0]}\nLosses: {player_stats['losses'].values[0]}\nDraws: {player_stats['draws'].values[0]}\nWin Rate: {player_stats['win_rate'].values[0]*100}%\nPoints Win Rate: {player_stats['points_win_rate'].values[0]*100}%\nNumber of Games Played: {player_stats['number_of_games_played'].values[0]}")

def merge_player(player_names: list, true_name: str):
    df = load_player_data()
    player_stats = df.loc[df['player_name'].isin(player_names)]
    wins = player_stats["wins"].sum()
    losses = player_stats["losses"].sum()
    draws = player_stats["draws"].sum()
    number_of_games_played = player_stats["number_of_games_played"].sum()
    win_rate = wins/number_of_games_played
    points = player_stats["points"].sum()
    points_win_rate = points/number_of_games_played * 3
    df.loc[df['player_name'] == true_name, 'wins'] = wins
    df.loc[df['player_name'] == true_name, 'losses'] = losses
    df.loc[df['player_name'] == true_name, 'draws'] = draws
    df.loc[df['player_name'] == true_name, 'win_rate'] = win_rate
    df.loc[df['player_name'] == true_name, 'number_of_games_played'] = number_of_games_played
    df.loc[df['player_name'] == true_name, 'points'] = points
    df.loc[df['player_name'] == true_name, 'points_win_rate'] = points_win_rate
    df.to_csv('player_info.csv', index=False)  

def connect_to_whatsapp(message_to_send: str, type_of_contact: str, contact: str):
    load_dotenv()
    hour_time = datetime.datetime.now().hour
    minute_time = datetime.datetime.now().minute
    send_message = sender.WhatsAppMessageSender(
        mode='contact',
        phone_number=os.getenv('MY_PHONE_NUMBER'),
        message=message_to_send, 
        time_hour=hour_time,
        time_minute=minute_time+1
        )
    send_message.execute()
    # print(hour_time)
    # print(minute_time)

def process_match_day():

    last_result = pd.read_csv('team_players.csv')
    player_record = pd.read_csv('player_info.csv')
    conf_check = True
    if not last_result.empty:
        while conf_check is True:
            update_result = input("Would you like to update the result of the last match? Yes or No?\n").lower()
            if update_result == "no":
                check = input("Are you sure you don't want to update the result of the last match? If it is not updated, the player list will be overwritten.\n").lower()
                if check == "yes":
                    break
                elif check == "no":
                    continue
                else:
                    print("Invalid input. Please input Yes or No.")
            elif update_result == "yes":
                last_match_result = input("Which team won the last match? Team 1, Team 2 or Draw?\n").lower()
                team_1 = last_result["team_1"].tolist()
                team_2 = last_result["team_2"].tolist()
                if last_match_result == "team 1":
                    for player in team_1:
                        player_record.loc[player_record['player_name'] == player, 'wins'] += 1
                        player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
                        player_record.loc[player_record['player_name'] == player, 'points'] += 3
                        player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
                        player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
                    for player in team_2:
                        player_record.loc[player_record['player_name'] == player, 'losses'] += 1
                        player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
                        player_record.loc[player_record['player_name'] == player, 'points'] += 0
                        player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
                        player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
                elif last_match_result == "team 2":
                    for player in team_2:
                        player_record.loc[player_record['player_name'] == player, 'wins'] += 1
                        player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
                        player_record.loc[player_record['player_name'] == player, 'points'] += 3
                        player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
                        player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
                    for player in team_1:
                        player_record.loc[player_record['player_name'] == player, 'losses'] += 1
                        player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
                        player_record.loc[player_record['player_name'] == player, 'points'] += 0
                        player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
                        player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
                elif last_match_result == "draw":
                    for player in (team_1 + team_2):
                        player_record.loc[player_record['player_name'] == player, 'draws'] += 1
                        player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] += 1
                        player_record.loc[player_record['player_name'] == player, 'points'] += 3
                        player_record.loc[player_record['player_name'] == player, 'win_rate'] = player_record.loc[player_record['player_name'] == player, 'wins']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played']
                        player_record.loc[player_record['player_name'] == player, 'points_win_rate'] = player_record.loc[player_record['player_name'] == player, 'points']/player_record.loc[player_record['player_name'] == player, 'number_of_games_played'] * 3
                else:
                    print("Invalid input. Please input Team 1, Team 2 or Draw.")
                player_record.to_csv('player_info.csv', index=False)     
                store_teams()
            else:
                print("Invalid input. Please input Yes or No.")
            conf_check = False
    store_teams()
    operation = True
    while operation is True:
        option = int(input("Would you like to do today? Please choose a number.\n1. Add a player\n2. Remove a player\n3. Merge players\n4. Pick a team\n5. Exit"))
        if type(option) == int and option in [1, 2, 3, 4]:
            if option == 1:
                player_name = input("Please enter the name of the player you would like to add.\n")
                add_player(player_name)
                operation = False
            elif option == 2:
                player_name = input("Please enter the name of the player you would like to remove.\n")
                remove_player(player_name)
                operation = False
            elif option == 3:
                player_names = input("Please enter the names of the players you would like to merge. Please separate them with a comma.\n").split(",")
                true_name = input("Please enter the name of the player you would like to merge them into.\n")
                merge_player(player_names, true_name)
                operation = False
            elif option == 5:
                break
            elif option == 4:
                players_this_week = load_weekly_players()
                players_on_record = retrieve_players()

                for player in players_this_week:
                    if player not in players_on_record:
                        add_player(player)

                win_rates = retrieve_win_rates(players_this_week)
                print(win_rates)
            
                for player, win_rate in zip(players_this_week, win_rates):
                    print(f"{player} has a win rate of {win_rate}.")

                team_1 = []
                team_1_rating = []
                team_2 = []
                team_2_rating = []

                counter = 0
                for number in range(len(players_this_week)):
                    if counter % 2 == 0:
                        team = team_1
                        player_ratings = team_1_rating
                        team_rating = np.mean(team_1_rating)
                        opp_team_rating = np.mean(team_2_rating)
                    else:
                        team = team_2
                        player_ratings = team_2_rating
                        team_rating = np.mean(team_2_rating)
                        opp_team_rating = np.mean(team_1_rating)
                    switch = True
                    if team_rating > opp_team_rating:
                        temp_players = []
                        while switch is True:
                            player = random.choice(players_this_week)
                            rating_index = players_this_week.index(player)
                            rating = win_rates[rating_index]
                            temp_players.append(player)
                            print(player)
                            print(f"Rating: {rating}")
                            print(f"Opponent Rating: {opp_team_rating}")
                            print(f"Min Win Rate: {min(win_rates)}")
                            if (opp_team_rating < min(win_rates)) or (opp_team_rating == min(win_rates)):
                                switch = False
                            elif rating < opp_team_rating:
                                switch = False
                            elif len(set(temp_players)) == len(players_this_week):
                                switch = False
                    elif team_rating < opp_team_rating:
                        temp_players = []
                        while switch is True:
                            player = random.choice(players_this_week)
                            rating_index = players_this_week.index(player)
                            rating = win_rates[rating_index]
                            temp_players.append(player)
                            print(2)
                            print(player)
                            print(f"Rating: {rating}")
                            print(f"Opponent Rating: {opp_team_rating}")
                            print(f"Min Win Rate: {min(win_rates)}")
                            if (opp_team_rating < max(win_rates)) or (opp_team_rating == max(win_rates)):
                                switch = False
                            elif rating > opp_team_rating:
                                switch = False
                            elif len(set(temp_players)) == len(players_this_week):
                                switch = False
                    else:
                        player = random.choice(players_this_week)
                    team.append(player)
                    print(player)
                    print(players_this_week)
                    print(win_rates)
                    rating_index = players_this_week.index(player)
                    rating = win_rates[rating_index]
                    player_ratings.append(float(rating))
                    players_this_week.remove(player)
                    del win_rates[rating_index]
                    counter += 1
                
                store_teams(team_1, team_2)

                print(f"Team 1: {team_1} has an average win rate of {np.mean(team_1_rating)}")
                print(f"Team 2: {team_2} has an average win rate of {np.mean(team_2_rating)}")
            operation = False
        else:
            print("This is an invalid input. Please input an integer between 1 and 4.")

if __name__ == "__main__":
    start_time = datetime.datetime.now()
    print("Code started at: " + str(start_time))
    # place code here
    # store_teams()
    process_match_day()
    end_time = datetime.datetime.now()
    print("Code ended at: " + str(end_time))
    runtime = end_time - start_time
    print(f"Code ran in {runtime/60} minutes and {runtime} seconds.")

# enforce equal length constraint
# true team balance