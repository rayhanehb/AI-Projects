# AI-Projects
## Sliding puzzle solver: 
hrd.py
## checkers endgame solver
**file** : checkers.py


**TO RUN FILE:** python3 checkers_solver.py --inputfile input.txt --outputfile output.txt

**Description:**

The Checkers Endgame Solver is a Python-based program designed to assist checkers (draughts) enthusiasts and players in optimizing their endgame strategies. In the game of checkers, the endgame phase involves complex tactical maneuvers, and this solver aims to provide an efficient and interactive tool to analyze and learn from various endgame scenarios.

**Features:**

**Alpha-Beta Pruning Algorithm:** The solver utilizes the Alpha-Beta pruning algorithm to explore the game tree efficiently, identifying optimal moves and strategies. <br>
**Heuristic Evaluation:** Board states are evaluated based on factors such as piece count, king pieces, and board positioning, providing valuable insights into the game's progression. <br>
**Iterative Deepening Search:** The program handles intricate endgame scenarios with limited computation time, ensuring that it remains a practical tool for players. <br>
**State Caching:** To enhance performance, the solver employs state caching, allowing it to store and retrieve previously evaluated positions. <br>
**User-Friendly Interface:** The solver offers an interactive platform, enabling players to input their endgame scenarios and receive step-by-step solutions. <br>
Create an input file (e.g., input.txt) following the format below:

**Input File Format (Example):**

.......b <br>
..r...b. <br>
........ <br>
R...b.b. <br>
........ <br>
..r..... <br>
...r.... <br>
....B... <br>

**In the input file:**

Use '.' to represent empty squares on the checkers board.<br>
Use 'r' for red pieces (normal) and 'R' for red kings.<br>
Use 'b' for black pieces (normal) and 'B' for black kings.<br>


## HMM part of speech tagging
tagger.py
