#Project 1: Search in pacman 

##Introduction
In this project, Pacman agent will find paths through his maze world, both to reach a particular location and to collect food efficiently. 

General search algorithms are were built to apply them to Pacman scenarios.

This project includes an autograder for you to grade your answers on your machine. This can be run with the command:

    python autograder.py

The code for this project consists of several Python files.

**Edited files:**

|   File   |  Description   |
|----------|----------------|
|search.py	      |Where all search algorithms reside.   |
|searchAgents.py	|Where all search-based agents reside. |


**Files you should read but NOT edit:**

|   File   |  Description   |
|----------|----------------|
|pacman.py	|The main file that runs Pacman games. This file describes a Pacman GameState type, which you use in this project.|
|game.py	|The logic behind how the Pacman world works. This file describes several supporting types like AgentState, Agent, Direction, and Grid.|
|util.py	|Useful data structures for implementing search algorithms.|


**Supporting files you can ignore:**

|   File   |  Description   |
|----------|----------------|
|graphicsDisplay.py	|Graphics for Pacman|
|graphicsUtils.py	|Support for Pacman graphics|
|textDisplay.py	|ASCII graphics for Pacman|
|ghostAgents.py	|Agents to control ghosts|
|keyboardAgents.py	|Keyboard interfaces to control Pacman|
|layout.py	|Code for reading layout files and storing their contents|
|autograder.py	|Project autograder|
|testParser.py	|Parses autograder test and solution files|
|testClasses.py	|General autograding test classes|
|test_cases/	|Directory containing the test cases for each question|
|searchTestClasses.py |Project 1 specific autograding test classes|

##Run

You should be able to play a game of Pacman by typing the following at the command line:

    python pacman.py
    
Pacman lives in a shiny blue world of twisting corridors and tasty round treats. Navigating this world efficiently will be Pacman's first step in mastering his domain.

The simplest agent in searchAgents.py is called the GoWestAgent, which always goes West (a trivial reflex agent). This agent can occasionally win:

    python pacman.py --layout testMaze --pacman GoWestAgent
    
But, things get ugly for this agent when turning is required:

    python pacman.py --layout tinyMaze --pacman GoWestAgent
    
If Pacman gets stuck, you can exit the game by typing `CTRL-c` into your terminal.

Note that pacman.py supports a number of options that can each be expressed in a long way (e.g., --layout) or a short way (e.g., -l). You can see the list of all options and their default values via:

    python pacman.py -h

Also, all of the commands that appear in this project also appear in commands.txt, for easy copying and pasting. In UNIX/Mac OS X, you can even run all these commands in order with bash commands.txt.

Note: if you get error messages regarding Tkinter, see [this page](http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter).
