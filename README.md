# MDP-Problem-Generator-cs440-simple-MDP
Allows you to create an instance of the problem we talked about in the class, solve it along with each solution step.

## gen_grid_basic.py

This script creates grids of varying sizes of the types discussed in class.

Cell numbering convention is the same as the one used in class slides and class notes

The two absorbing states are referred to as the goal state and the deadend state.

As input to the program, you need to give the following:

  ```grid_size             Size of the grid, will be grid_size x grid_size (Visualization currently assumes a value less than 100)

  goal_x                X coordinate of the goal state

  goal_y                Y coordinate of the goal state

  deadend_x             X coordinate of the deadend state

  deadend_y             Y coordinate of the deadend state

  slipping_probability  Probability of staying in the same state

  discount_factor       Discount factor

  stopping_criteria     Stopping criteria (value iteration stops when bellman residue is less than this value

  generate_problem_statement If this flag is set, the program will generate a problem statement in the current directory (set true by default)

  solve_using_value_iteration If this flag is set, the program will solve the problem using value iteration (set false by default)
```

Example usage:

```
To generate a problem statement

python gen_grid_basic.py --grid_size 5 --goal_x 4 --goal_y 4 --deadend_x 1 --deadend_y 1 --slipping_probability 0.01 --discount_factor 0.99 --stopping_threshold 0.01 --generate_problem_statement

To solve the problem using value iteration

python gen_grid_basic.py --grid_size 5 --goal_x 4 --goal_y 4 --deadend_x 1 --deadend_y 1 --slipping_probability 0.01 --discount_factor 0.99 --stopping_threshold 0.01 --solve_using_value_iteration
```
