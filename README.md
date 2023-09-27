# AI-Projects
## Sliding puzzle solver: 
hrd.py


## HMM part of speech tagging
**TO RUN FILE:** python3 pos_tagger.py --trainingfiles training1.txt training2.txt --testfile test.txt --outputfile output.txt

**Description:**

The Part-of-Speech (POS) Tagger is a Python-based program that enhances text analysis accuracy by assigning POS tags to words in a given text. This tool aids in optimizing data processing workflows and improving the performance of AI-driven applications that rely on linguistic analysis.

**Features:**

Statistical POS Tagging: The tagger employs statistical models and machine learning techniques to assign accurate POS tags to words, facilitating advanced natural language processing tasks.
Emission and Transition Probabilities: The program calculates emission and transition probabilities, enhancing tagging precision and adaptability to various text domains.
Viterbi Algorithm: Utilizing the Viterbi algorithm, the tagger efficiently predicts the most likely sequence of POS tags for input sentences.
Interactive Usage: Users can apply the POS tagger to their text data, providing valuable insights for tasks such as information retrieval, sentiment analysis, and more.
Create an input file (e.g., test.txt) with the text you want to analyze. The program will generate an output file (e.g., output.txt) with the assigned POS tags for each word.

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








