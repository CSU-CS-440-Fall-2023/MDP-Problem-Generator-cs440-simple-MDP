import sys
import argparse
import copy
'''
This script creates grids of varying sizes of the types discussed in class.

Cell numbering convention is the same as the one used in class slides and class notes

The two absorbing states are referred to as the goal state and the deadend state.

As input to the program, you need to give the following:

  grid_size             Size of the grid, will be grid_size x grid_size (Visualization currently assumes a value less than 100)

  goal_x                X coordinate of the goal state

  goal_y                Y coordinate of the goal state

  deadend_x             X coordinate of the deadend state

  deadend_y             Y coordinate of the deadend state

  slipping_probability  Probability of staying in the same state

  discount_factor       Discount factor

  stopping_criteria     Stopping criteria (value iteration stops when bellman residue is less than this value

  generate_problem_statement If this flag is set, the program will generate a problem statement in the current directory (set true by default)
  
  solve_using_value_iteration If this flag is set, the program will solve the problem using value iteration (set false by default)


Example usage:


To generate a problem statement

python gen_grid_basic..py --grid_size 5 --goal_x 4 --goal_y 4 --deadend_x 1 --deadend_y 1 --slipping_probability 0.01 --discount_factor 0.99 --stopping_threshold 0.01 --generate_problem_statement

To solve the problem using value iteration

python gen_grid_basic..py --grid_size 5 --goal_x 4 --goal_y 4 --deadend_x 1 --deadend_y 1 --slipping_probability 0.01 --discount_factor 0.99 --stopping_threshold 0.01 --solve_using_value_iteration
'''


def visualize_grid(grid_size, goal_x, goal_y, deadend_x, deadend_y, current_values = None, policy = None):
    ## Print the cells of the grid
    # Print the top row
    print(" " + "------- " * (grid_size) + " ")
    for i in range(grid_size-1, -1, -1):
        # Print the left column
        print("|", end="")
        for j in range(grid_size):
            if i == goal_y and j == goal_x:
                print("  Goal ", end="")
            elif i == deadend_y and j == deadend_x:
                print("Deadend", end="")

            else:
                if current_values is not None:
                    print ("{0:.5f}".format(current_values[j][i]), end="")
                elif policy is not None:
                    print("   " + policy[j][i] + "   ", end="")
                else:
                    grid_x = j
                    grid_y = i
                    if grid_x < 10:
                        grid_x_str = " " + str(grid_x)
                    else:
                        grid_x_str = str(grid_x)
                    if grid_y < 10:
                        grid_y_str = " " + str(grid_y)
                    else:
                        grid_y_str = str(grid_y)
                    print("(" + grid_x_str + "," + grid_y_str + ")", end="")
            if j < grid_size - 1:
                print("|", end="")
        if i < grid_size - 1:
            print("|")
        else:
            print("|")
    # Print the bottom row
    print(" " + "------- " * (grid_size) + " ")

def value_iteration(current_values, grid_size, goal_x, goal_y, deadend_x, deadend_y, slipping_probability, discount_factor):
    next_values = copy.deepcopy(current_values)
    # actions up, down, left, right
    actions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    max_residue = -1000
    for x in range(grid_size):
        for y in range(grid_size):
            if (x == goal_x and y == goal_y) or (x == deadend_x and y == deadend_y):
                continue
            else:
                max_value = -1000
                for act_delta in actions:
                    next_state = (x + act_delta[0], y + act_delta[1])
                    if next_state[0] < 0 or next_state[0] >= grid_size or next_state[1] < 0 or next_state[1] >= grid_size:
                        next_transitions = [(1, (x, y),0)]
                    else:
                        if (next_state[0] == goal_x and next_state[1] == goal_y):
                            next_reward = 1
                        elif (next_state[0] == deadend_x and next_state[1] == deadend_y):
                            next_reward = -1
                        else:
                            next_reward = 0
                        next_transitions = [(1-slipping_probability, next_state, next_reward), (slipping_probability, (x, y), 0)]
                    value = 0
                    for prob, state, reward in next_transitions:
                        value += prob * (reward + discount_factor * current_values[state[0]][state[1]])
                    if value > max_value:
                        max_value = value
                next_values[x][y] = max_value
                residue = abs(max_value - current_values[x][y])
                if residue > max_residue:
                    max_residue = residue
    return next_values, max_residue


def find_policy(current_values, grid_size, goal_x, goal_y, deadend_x, deadend_y, slipping_probability, discount_factor):
    # actions up, down, left, right
    actions = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    action_names = ["U", "D", "L", "R"]
    policy = [["" for i in range(grid_size)] for j in range(grid_size)]
    for x in range(grid_size):
        for y in range(grid_size):
            if (x == goal_x and y == goal_y) or (x == deadend_x and y == deadend_y):
                continue
            else:
                max_value = -1000
                max_act_id = -1
                curr_act_id = 0
                for act_delta in actions:
                    next_state = (x + act_delta[0], y + act_delta[1])
                    if next_state[0] < 0 or next_state[0] >= grid_size or next_state[1] < 0 or next_state[
                        1] >= grid_size:
                        next_transitions = [(1, (x, y), 0)]
                    else:
                        if (next_state[0] == goal_x and next_state[1] == goal_y):
                            next_reward = 1
                        elif (next_state[0] == deadend_x and next_state[1] == deadend_y):
                            next_reward = -1
                        else:
                            next_reward = 0
                        next_transitions = [(1 - slipping_probability, next_state, next_reward),
                                            (slipping_probability, (x, y), 0)]
                    value = 0
                    for prob, state, reward in next_transitions:
                        value += prob * (reward + discount_factor * current_values[state[0]][state[1]])
                    if value > max_value:
                        max_value = value
                        max_act_id = curr_act_id
                    curr_act_id += 1
                policy[x][y] = action_names[max_act_id]

    return policy



parser = argparse.ArgumentParser(description="Process the input parameters.")

# Inputs
parser.add_argument("--grid_size", type=int, help="Size of the grid, will be grid_size x grid_size")

# Goal state x, y coordinates
parser.add_argument("--goal_x", type=int, help="X coordinate of the goal state")
parser.add_argument("--goal_y", type=int, help="Y coordinate of the goal state")

# Deadend state x, y coordinates
parser.add_argument("--deadend_x", type=int, help="X coordinate of the deadend state")
parser.add_argument("--deadend_y", type=int, help="Y coordinate of the deadend state")

# Slipping probability -- probability you will stay in the same state
parser.add_argument("--slipping_probability", type=float, help="Probability of staying in the same state")

# Discount factor
parser.add_argument("--discount_factor", type=float, help="Discount factor")

# Stopping threshold
parser.add_argument("--stopping_threshold", type=float, help="Stopping threshold")

# Flags
parser.add_argument("--generate_problem_statement", action="store_true", help="Generate the problem statement", default=True)
parser.add_argument("--solve_using_value_iteration", action="store_true", help="Solve the problem using value iteration", default=False)

args = parser.parse_args()

grid_size = args.grid_size
goal_x = args.goal_x
goal_y = args.goal_y
deadend_x = args.deadend_x
deadend_y = args.deadend_y
slipping_probability = args.slipping_probability
discount_factor = args.discount_factor
stopping_threshold = args.stopping_threshold
print_problem_statement = args.generate_problem_statement
solve_using_value_iteration = args.solve_using_value_iteration


# Make sure goal and deadend are not the same
assert not (goal_x == deadend_x and goal_y == deadend_y), "Goal and deadend cannot be the same"



# Make sure goal and dead end are inside the cells
assert goal_x < grid_size and goal_y < grid_size, "Goal state is outside the grid"

assert deadend_x < grid_size and deadend_y < grid_size, "Deadend state is outside the grid"

# Make sure the discount factor is between 0 and 1
assert discount_factor >= 0 and discount_factor < 1, "Discount factor must be between 0 and 1"

if print_problem_statement:
    print ("\n\n#### Problem statement ####")
    print (" Consider the following MDP problem:  You have a grid of size " + str(grid_size) + " x " + str(grid_size) + ".")
    print (" There are two absorbing states: one is the goal state, and the other is the deadend state.")
    print (" The goal state is at (" + str(goal_x) + ", " + str(goal_y) + ") and the deadend state is at (" + str(deadend_x) + ", " + str(deadend_y) + ").")
    print (" You receive a reward of 1 when you enter the goal state from another state, and a reward of -1 when you enter the deadend state from another state.")
    print (" You receive a reward of 0 for all other transitions including transitions from the absorber state to the same absorber state.")
    print (" The transition probabilities are as follows: ")
    print(" You have four actions: up, down, left, right. ")
    print (" 1. For any non-absorber state, when you take an action, there is a " + str(slipping_probability) + " probability that you will stay in the same state.")
    print(" 2. For any non-absorber state, when you take an action, there is a " + str((1-slipping_probability)) + " probability that you will move in the direction you intended (provided it's possible).")
    print(" 3. For absorbing states, the probability of staying in the same state is 1, regardless of the action you take.")
    print (" The discount factor is " + str(discount_factor) + ".")
    print (" The stopping threshold is " + str(stopping_threshold) + ". (i.e. stop when the maximum difference between the values of two successive iterations is less than " + str(stopping_threshold) + ")")
    print ("#### End of problem statement ####\n")

print("## Grid ##")
visualize_grid(grid_size, goal_x, goal_y, deadend_x, deadend_y)
# initialize values to zero
init_values = [[0 for i in range(grid_size)] for j in range(grid_size)]

# To avoid infinite loop, adding a maximum number of iterations
max_iterations = 10000


if solve_using_value_iteration:
    print("## Initial values ##")
    visualize_grid(grid_size, goal_x, goal_y, deadend_x, deadend_y, init_values)

    print ("\n\n#### Value iteration ####\n")
    current_values = copy.deepcopy(init_values)
    for i in range(max_iterations):
        print("Iteration " + str(i))
        next_values, max_residue = value_iteration(current_values, grid_size, goal_x, goal_y, deadend_x, deadend_y, slipping_probability, discount_factor)
        if max_residue < stopping_threshold:
            print("Stopping threshold reached after " + str(i) + " iterations")
            current_values = copy.deepcopy(next_values)
            break
        current_values = copy.deepcopy(next_values)
        print("Values after iteration " + str(i))
        visualize_grid(grid_size, goal_x, goal_y, deadend_x, deadend_y, current_values)
        print("Max residue: " + str(max_residue))
    print("Final values")
    visualize_grid(grid_size, goal_x, goal_y, deadend_x, deadend_y, current_values)
    final_policy = find_policy(current_values, grid_size, goal_x, goal_y, deadend_x, deadend_y, slipping_probability, discount_factor)
    print("Final policy")
    visualize_grid(grid_size, goal_x, goal_y, deadend_x, deadend_y, policy=final_policy)



