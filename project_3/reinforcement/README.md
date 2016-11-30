#Project 3: Reinforcement learning

![alt text](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/sp14/reinforcement/capsule.png "Pacman")

Pacman seeks reward.
Should he eat or should he run?
When in doubt, Q-learn.

##Table of contents

##Introduction

In this project, you will implement value iteration and Q-learning. You will test your agents first on Gridworld (from class), then apply them to a simulated robot controller (Crawler) and Pacman.

As in previous projects, this project includes an autograder for you to grade your solutions on your machine. This can be run on all questions with the command:

    python autograder.py
  
It can be run for one particular question, such as q2, by:

    python autograder.py -q q2

It can be run for one particular test by commands of the form:

    python autograder.py -t test_cases/q2/1-bridge-grid
  
See the autograder tutorial in Project 0 for more information about using the autograder.

The code for this project contains the following files, which are available in a [zip archive](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/sp14/reinforcement/reinforcement.zip):

The entire project description can also be downloaded as a pdf from [here](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/sp14/reinforcement/docs/Project-3.pdf).

**Edited files:**

|   File   |  Description   |
|----------|----------------|
|valueIterationAgents.py	|A value iteration agent for solving known MDPs.|
|qlearningAgents.py	|Q-learning agents for Gridworld, Crawler and Pacman.|
|analysis.py	|A file to put your answers to questions given in the project.|

**Files you should read but NOT edit:**

|   File   |  Description   |
|----------|----------------|
|mdp.py	|Defines methods on general MDPs.|
|learningAgents.py	|Defines the base classes ValueEstimationAgent and QLearningAgent, which your agents will extend.|
|util.py	|Utilities, including util.Counter, which is particularly useful for Q-learners.|
|gridworld.py	|The Gridworld implementation.|
|featureExtractors.py	|Classes for extracting features on (state,action) pairs. Used for the approximate Q-learning agent (in qlearningAgents.py).|

**Files you can ignore:**

|   File   |  Description   |
|----------|----------------|
|environment.py	|Abstract class for general reinforcement learning environments. Used by gridworld.py.|
|graphicsGridworldDisplay.py	|Gridworld graphical display.|
|graphicsUtils.py	|Graphics utilities.|
|textGridworldDisplay.py	|Plug-in for the Gridworld text interface.|
|crawler.py	|The crawler code and test harness. You will run this but not edit it.|
|graphicsCrawlerDisplay.py	|GUI for the crawler robot.|
|autograder.py	|Project autograder|
|testParser.py	|Parses autograder test and solution files|
|testClasses.py	|General autograding test classes|
|test_cases/	|Directory containing the test cases for each question|
|reinforcementTestClasses.py	|Project 3 specific autograding test classes|

**Files to Edit and Submit:** You will fill in portions of **valueIterationAgents.py**, **qlearningAgents.py**, and **analysis.py** during the assignment. You should submit these files with your code and comments. Please do not change the other files in this distribution or submit any of our original files other than these files.

**Evaluation:** Your code will be autograded for technical correctness. Please do not change the names of any provided functions or classes within the code, or you will wreak havoc on the autograder.

**Getting Help:** You are not alone! If you find yourself stuck on something, take advantage of our piazza discussion forum.

**Discussion:** Please be careful not to post spoilers.

##MDPs

To get started, run Gridworld in manual control mode, which uses the arrow keys:

python gridworld.py -m
You will see the two-exit layout from class. The blue dot is the agent. Note that when you press up, the agent only actually moves north 80% of the time. Such is the life of a Gridworld agent!

You can control many aspects of the simulation. A full list of options is available by running:

    python gridworld.py -h
  
The default agent moves randomly

    python gridworld.py -g MazeGrid
  
You should see the random agent bounce around the grid until it happens upon an exit. Not the finest hour for an AI agent.

Note: The Gridworld MDP is such that you first must enter a pre-terminal state (the double boxes shown in the GUI) and then take the special 'exit' action before the episode actually ends (in the true terminal state called **TERMINAL_STATE**, which is not shown in the GUI). If you run an episode manually, your total return may be less than you expected, due to the discount rate (**-d** to change; 0.9 by default).

Look at the console output that accompanies the graphical output (or use **-t** for all text). You will be told about each transition the agent experiences (to turn this off, use **-q**).

As in Pacman, positions are represented by **(x,y)** Cartesian coordinates and any arrays are indexed by **[x][y]**, with **'north'** being the direction of increasing y, etc. By default, most transitions will receive a reward of zero, though you can change this with the living reward option **(-r)**.

##Questions

###Question 1 (6/6 points) 

Write a value iteration agent in **ValueIterationAgent**, which has been partially specified for you in **valueIterationAgents.py**. Your value iteration agent is an offline planner, not a reinforcement learning agent, and so the relevant training option is the number of iterations of value iteration it should run (option **-i**) in its initial planning phase. **ValueIterationAgent** takes an MDP on construction and runs value iteration for the specified number of iterations before the constructor returns.

Value iteration computes k-step estimates of the optimal values, Vk. In addition to running value iteration, implement the following methods for **ValueIterationAgent** using Vk.

* **computeActionFromValues(state)** computes the best action according to the value function given by **self.values**.

* **computeQValueFromValues(state, action)** returns the Q-value of the (state, action) pair given by the value function given by **self.values**.

These quantities are all displayed in the GUI: values are numbers in squares, Q-values are numbers in square quarters, and policies are arrows out from each square.

Important: Use the "batch" version of value iteration where each vector Vk is computed from a fixed vector Vk-1 (like in lecture), not the "online" version where one single weight vector is updated in place. This means that when a state's value is updated in iteration k based on the values of its successor states, the successor state values used in the value update computation should be those from iteration k-1 (even if some of the successor states had already been updated in iteration k). The difference is discussed in [Sutton & Barto](http://www.cs.ualberta.ca/~sutton/book/ebook/node41.html) in the 6th paragraph of chapter 4.1.

Note: A policy synthesized from values of depth k (which reflect the next k rewards) will actually reflect the next k+1 rewards (i.e. you return pik+1). Similarly, the Q-values will also reflect one more reward than the values (i.e. you return Qk+1).

You should return the synthesized policy pik+1.

Hint: Use the **util.Counter** class in **util.py**, which is a dictionary with a default value of zero. Methods such as **totalCount** should simplify your code. However, be careful with **argMax**: the actual argmax you want may be a key not in the counter!

Note: Make sure to handle the case when a state has no available actions in an MDP (think about what this means for future rewards).

To test your implementation, run the autograder:

    python autograder.py -q q1
    
The following command loads your **ValueIterationAgent**, which will compute a policy and execute it 10 times. Press a key to cycle through values, Q-values, and the simulation. You should find that the value of the start state **(V(start)**, which you can read off of the GUI) and the empirical resulting average reward (printed after the 10 rounds of execution finish) are quite close.

    python gridworld.py -a value -i 100 -k 10
    
Hint: On the default BookGrid, running value iteration for 5 iterations should give you this output:

    python gridworld.py -a value -i 5

![alt text](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/sp14/reinforcement/value.png "value iteration with k=5")

Grading: Your value iteration agent will be graded on a new grid. We will check your values, Q-values, and policies after fixed numbers of iterations and at convergence (e.g. after 100 iterations).


###Question 2 (1/1 point) 

**BridgeGrid** is a grid world map with the a low-reward terminal state and a high-reward terminal state separated by a narrow "bridge", on either side of which is a chasm of high negative reward. The agent starts near the low-reward state. With the default discount of 0.9 and the default noise of 0.2, the optimal policy does not cross the bridge. Change only ONE of the discount and noise parameters so that the optimal policy causes the agent to attempt to cross the bridge. Put your answer in **question2()** of** analysis.py**. (Noise refers to how often an agent ends up in an unintended successor state when they perform an action.) The default corresponds to:

    python gridworld.py -a value -i 100 -g BridgeGrid --discount 0.9 --noise 0.2
    
![alt text](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/sp14/reinforcement/value-q2.png "value iteration with k=100")

Grading: We will check that you only changed one of the given parameters, and that with this change, a correct value iteration agent should cross the bridge. To check your answer, run the autograder:

    python autograder.py -q q2
    
###Question 3 (5/5 points) 

Consider the **DiscountGrid** layout, shown below. This grid has two terminal states with positive payoff (in the middle row), a close exit with payoff +1 and a distant exit with payoff +10. The bottom row of the grid consists of terminal states with negative payoff (shown in red); each state in this "cliff" region has payoff -10. The starting state is the yellow square. We distinguish between two types of paths: (1) paths that "risk the cliff" and travel near the bottom row of the grid; these paths are shorter but risk earning a large negative payoff, and are represented by the red arrow in the figure below. (2) paths that "avoid the cliff" and travel along the top edge of the grid. These paths are longer but are less likely to incur huge negative payoffs. These paths are represented by the green arrow in the figure below.

![alt text](https://s3-us-west-2.amazonaws.com/cs188websitecontent/projects/sp14/reinforcement/value-q2.png "DiscountGrid")


In this question, you will choose settings of the discount, noise, and living reward parameters for this MDP to produce optimal policies of several different types. Your setting of the parameter values for each part should have the property that, if your agent followed its optimal policy without being subject to any noise, it would exhibit the given behavior. If a particular behavior is not achieved for any setting of the parameters, assert that the policy is impossible by returning the string **'NOT POSSIBLE'**.

Here are the optimal policy types you should attempt to produce:

1. Prefer the close exit (+1), risking the cliff (-10)
2. Prefer the close exit (+1), but avoiding the cliff (-10)
3. Prefer the distant exit (+10), risking the cliff (-10)
4. Prefer the distant exit (+10), avoiding the cliff (-10)
5. Avoid both exits and the cliff (so an episode should never terminate)

To check your answers, run the autograder:

    python autograder.py -q q3

**question3a()** through **question3e()** should each return a 3-item tuple of (discount, noise, living reward) in **analysis.py**.
Note: You can check your policies in the GUI. For example, using a correct answer to 3(a), the arrow in (0,1) should point east, the arrow in (1,1) should also point east, and the arrow in (2,1) should point north.

Note: On some machines you may not see an arrow. In this case, press a button on the keyboard to switch to qValue display, and mentally calculate the policy by taking the arg max of the available qValues for each state.

Grading: We will check that the desired policy is returned in each case.
