# Treasure Map PotA
This project is a treasure map puzzle for the players of the Princes of the Apocalypse D&D campaign. The idea is simple. The players possess a map of the area with a number of ancient dwarven runes on them. The location of these symbols on the map is dependent on the location of the map itself. It is up to the players to figure the following things out:
1. The runes move based on their own location (either their horizontal, vertical location or both)
2. The runes move in circles
3. Each rune has a 'true' location.
    - The true location of the runes that correspond to a metal reveal themselves when the map touches that metal.

## GUI 
A GUI is provided that generates the map and all the icons based on a dragable player location. The true locations can be toggled on and off in the sidebar. See below for an example screenshot. The true locations are shown in white. The player icon is on the road near Triboar (top-left).

To use the GUI simply drag the player icon to the correct location and press export in the bottom right to save the new map.

<img src="images/Screenshot.png" alt="screenshot" width="600"/>



## Installation
In order to install make sure you have python 3 installed. Clone this repository and run the following command in the terminal

```pip install -r requirements.txt```

## Running the program
Open the directory in which you have installed the program in a terminal and run the command

```python app.py```

Simple as that.