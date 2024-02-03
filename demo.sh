conda activate ml_env

cd search

# DFS
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs --frameTime 0.02

# BFS
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs --frameTime 0.02

# UCS
# Explain the cost function 
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs --frameTime 0.02

# A*
python pacman.py -l bigMaze -z .5 -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic

# Manual play to prove the other way is worse
python pacman.py -l mediumMaze

# A* Corners
python pacman.py -l mediumCorners -p AStarCornersAgent -z 0.5

# Food Heuristic
# distance between futhrermost dots + distance to closer fruit
# distance between furthermost dots will be traveled in either case
# it's better to go to the closer one first 


# UCS food
python pacman.py -l trickySearch -p SearchAgent -a fn=ucs,prob=FoodSearchProblem,heuristic=foodHeuristic
# [SearchAgent] using function ucs
# Path found with total cost of 60 in 15.3 seconds
# Search nodes expanded: 16688
# Pacman emerges victorious! Score: 570
# Score:        570.0

# A* Food
# SearchAgent] using function astar and heuristic foodHeuristic
# Path found with total cost of 60 in 3.9 seconds
# Search nodes expanded: 7553
# Score:        570.0

python pacman.py -l testSearch -p AStarFoodSearchAgent


# [SKIPPABLE] Find the closest food using BFS and head for it
python pacman.py -l bigSearch -p ClosestDotSearchAgent -z .5 --frameTime 0.02



# --- MULTIAGET ---
cd ../multiagent

# Reflex agent taking the best movement calculating the best move
# Taking in account: 
#   - food in radius 
#   - ghosts position
#   - ghosts running
python pacman.py --frameTime 0.02 -p ReflexAgent -k 2

# MINIMAX using the game score
python autograder.py -q q2


# --- Machine learning ---

# Qlearning for 2000 episodes on smallGrid
# Average Score: 499.7
# Scores:        503.0, 502.0, 499.0, 499.0, 503.0, 501.0, 495.0, 495.0, 501.0, 499.0
# Win Rate:      10/10 (1.00)
python pacman.py --replay replays/qLearn-small-2000-ep         

# Approximate QLearning on big grid
# Average Score: 1326.2
# Scores:        1308.0, 1329.0, 1329.0, 1346.0, 1335.0, 1318.0, 1323.0, 1313.0, 1333.0, 1328.0
# Win Rate:      10/10 (1.00)
# Record:        Win, Win, Win, Win, Win, Win, Win, Win, Win, Win
python pacman.py --replay replays/qLearn-50-ep
python pacman.py --replay replays/qLearn-500-ep
