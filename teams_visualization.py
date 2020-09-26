''' Ian Nduhiu 
    Task: Data Visualization
'''

# Necessary imports
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import pandas as pd
import numpy as np
from itertools import chain

# Datasets being used in form of panda dataframes
data_dictionary = pd.read_excel("DATA DICTIONARY.xlsx")
member_and_teams = pd.read_excel("TEAM VISUALIZATION.xlsx")

def main():
    ''' The main function that serves as entry point. Calls the functions that 
        extract the data, find count of people per team per startup, 
        and visualizes the results '''
    # Get a list of all unique startups and a dictionary that
    # associates each team with all of its respective subteams
    startups, teams_and_subteams = extract_data()

    # Call team_count function that increases the team's count
    # for each team a member is part of, for each startup they 
    # are part of
    startups_team_counts = team_count(startups, teams_and_subteams)

    # Produce pie chart visualizations for each startup
    visualize(startups_team_counts)


def extract_data():
    ''' Extracts and cleans startups data while also building a dictionary
        used to associate subteams with their appropriate team '''
    # First: Get all unique startups
    # Getting values from STARTUP column, splitting them into lists
    # and flattening the list of lists into a unique list
    temp_list = [x.split(', ') for x in member_and_teams["STARTUP"].values]
    startups = list(set(chain.from_iterable(temp_list)))
    
    # Cleaning data by removing not-startups
    to_remove = ["DEVELOPMENT TEAM - App | Web | Mobile", 
                 "DATA SCIENCE TEAM - Data Science | Business Analytics",
                 "PM - Project Management",
                 "BUSINESS TEAM - Marketing | Finance | BD",
                 "CREATIVE TEAM - Design | Content"]
    for bad in to_remove:
        startups.remove(bad)

    # Store startups in a dictionary of dictionaries
    startups = {startup:{"BUSINESS TEAM":0, "CREATIVE TEAM":0, "DATA TEAM":0, 
                         "DEVELOPERS TEAM":0, "PM":0} 
                         for startup in startups 
                         if startup != "DATA SCIENCE ARMY"}
    startups["DATA SCIENCE ARMY"] = 0  # DSA has no subteams
    
    # Second: Need a way to navigate the data dictionary by associating
    # subteams with their respective team. With each team as a key, store its
    # respective subteams in a dictionary as the values
    teams = [team.strip() for team in data_dictionary["TEAM"].unique()]
    teams_and_subteams = {}
    for team in teams:
        specific_team = data_dictionary[data_dictionary['TEAM'] == team]
        teams_and_subteams[team] = [team[:-1]  # to remove comma at the end
                                for team in specific_team["SUBTEAM"].values]
        
    return (startups, teams_and_subteams)


def team_count(startups, teams_and_subteams):
    ''' Updates the teams' member counts within each startup by iterating
        member by member and checking which startups they are part of, and
        what teams they work in '''
    # List of startups and teams each member is part of
    # Remove spaces in teams to match data dictionary formatting
    member_startups = member_and_teams["STARTUP"].values 
    member_teams = member_and_teams["TEAMS"].values
    member_teams = [team.replace(" ", '') for team in member_teams]

    # Go through startups and teams for each member(each index)
    # and update the startup's teams as necessary
    # Exception made for Data Science army as it is one big team
    for member in range(len(member_teams)):
        for startup in member_startups[member].split(', '):
            if startup == "DATA SCIENCE ARMY":
                startups["DATA SCIENCE ARMY"] += 1
            else:
                for team in member_teams[member].split(','):
                    for key in teams_and_subteams:
                        if team in teams_and_subteams[key]:
                            startups[startup][key] += 1
        
    return startups


def visualize(startups_team_counts):
    ''' Creates and saves a pie chart for each startup showing the
        number of members for each team '''
    teams = ["BUSINESS TEAM", "CREATIVE TEAM", "DATA TEAM", 
              "DEVELOPERS TEAM", "PM"]  # to be used as labels
    curr_dir = "C:\\Users\\nderi\\FORKAIA\\Project 1 - Data Visualization" +\
                 "\\Startup Visualizations\\"
    for startup in startups_team_counts:
        if startup != "DATA SCIENCE ARMY":
            # Numbers for each team
            number_per_team = [startups_team_counts[startup][team] 
                                for team in teams]

            # Create pie chart with team counts as sizes
            _, ax1 = plt.subplots()
            wedges, _, autotexts = ax1.pie(number_per_team, 
                autopct=lambda pct: func(pct, number_per_team), shadow=True)
            ax1.legend(wedges, [team.split()[0] for team in teams], title="Teams", 
                    loc="lower right", bbox_to_anchor=(0.62, -0.167, 0.5, 1))
            plt.setp(autotexts, size=8, weight="bold")
            ax1.axis('equal')
            ax1.set_title(startup)
            plt.savefig(curr_dir + startup + '.png')
            plt.close()
        else:
            # Exception for Data Science Army - one big team
            _, ax1 = plt.subplots()
            army_size = [startups_team_counts[startup]]
            ax1.pie(army_size, autopct=lambda pct: func(pct, number_per_team), shadow=True)
            ax1.axis('equal')
            ax1.set_title(startup)
            plt.savefig(curr_dir + startup + '.png')
            plt.close()


def func(pct, allvals):
    ''' Returns a formatted string that allows pie chart to display both
        percentages and actual count of members in each team '''
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%\n({:d} people)".format(pct, absolute)

if __name__ == "__main__":
    main()
