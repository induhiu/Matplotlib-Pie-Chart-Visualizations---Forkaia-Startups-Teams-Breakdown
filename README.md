# Pie Chart Startup Composition Visualizations
## Description
Pie chart visualizations of the number of people requesting to join a given team per startup in the FORKAIA ecosystem.

## Datasets used
Datasets used are the "TEAM VISUALIZATION.xlsx" and "DATA DICTIONARY.xlsx" files. The former includes the startups different interns requested to work for and the subteams interested in for each of those startups. The latter provides the subteams to be found within each of the five teams: Business, Creative, Data, Developers and Project Management.

## Main procedure
The preprocessing involved cleaning the startups data and removing entries that were not startups but rather subteams. All unique startups were then extracted and all teams associated with their specific subteams. Each startup was associated with the 5 major teams as well. For each member who voiced interest in a startup and a team(s) within it, the count of that team within that startup was increased.

## Results
The visualizations can be found in the "Startup Visualizations" folder. Each pie chart contains a legend at the bottom right with different colors for different teams. The datasets used and well-documented code are provided as well.
 
Below is a sample pie chart visualization:

![](https://github.com/induhiu/Forkaia--Data-Visualization/blob/master/Startup%20Visualizations/INSOLAR.png)
