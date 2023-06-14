import argparse
import copy
import sys
import time
import math

cache = {} # you can use this to implement state caching!

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board, parent=None):

        self.board = board

        self.width = 8
        self.height = 8
        self.parent = parent

    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")
    

    '''This function returns a list of possible successor states for the current state.'''
    def get_successors(self, player):
        successors_reg = []
        successors_jump = []
        jump_prev=False
        if player in ['r', 'R']:
            player_pieces = ['r', 'R']
        else:
            player_pieces = ['b', 'B']
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] in player_pieces:
                    succ_list,flag = (self.get_moves(i, j, player,jumped=False, jumps=[], overall_jumps=[],moves=[])) # get all possible moves for the current piece  
                    if flag == True:
                        successors_jump.extend(succ_list)
                    if flag == False:
                        successors_reg.extend(succ_list)
        if len(successors_jump) > 0:
            return successors_jump
        else:
            return successors_reg
    '''This function returns a list of possible moves for a given piece. if the piece can jump and capture it will only return those moves'''
    
    def make_move(self, i, j, player, direction):
        new_board = copy.deepcopy(self.board)
        moved_to = []
        if direction == 'top_right':
            new_board[i+1][j+1] = player
            new_board[i][j] = '.'
            moved_to.append((i+1,j+1))
        elif direction == 'top_left':
            new_board[i+1][j-1] = player
            new_board[i][j] = '.'
            moved_to.append((i+1,j-1))
        elif direction == 'bottom_right':
            new_board[i-1][j+1] = player
            new_board[i][j] = '.'
            moved_to.append((i-1,j+1))
        elif direction == 'bottom_left':
            new_board[i-1][j-1] = player
            new_board[i][j] = '.'
            moved_to.append((i-1,j-1))

        for pos in moved_to:
            x,y = pos
            if pos[0]==0 and player =='r':
                new_board[x][y]='R'
                king_flag = True
            elif pos[0]==7 and player =='b':
                new_board[x][y]='B'
                king_flag = True
        #print new_board
        # new_display(new_board)
        #create a new state with the new board
        return State(new_board, self)
        # return new_board
    
    '''function to modify the board given a jump and capture move. take arguments of the current board, the piece to move, the direction to move in, and the piece to capture'''
   

    def black_moves(self, i, j, king=False):
        moves = []
        if king == False:
            player = 'b'
        else:
            player = 'B'

        if i+1 < self.height and j+1 < self.width:
                    if self.board[i+1][j+1] == '.':
                        #move diagonally forward one space to the right
                       move = self.make_move(i, j, player, 'top_right')
                       moves.append(State(move.board, self))
        if i+1 < self.height and j-1 >= 0:
            if self.board[i+1][j-1] == '.':
                #move diagonally forward one space to the left
                move = self.make_move(i, j, player, 'top_left')
                moves.append(State(move.board, self))
        if king == True:
            if i-1 >= 0 and j+1 < self.width:
                if self.board[i-1][j+1] == '.':
                    #move diagonally backwards one space to the right
                    move = self.make_move(i, j, player, 'bottom_right')
                    moves.append(State(move.board, self))
            if i-1 >= 0 and j-1 >= 0:
                if self.board[i-1][j-1] == '.':
                    #move diagonally backwards one space to the left
                    move = self.make_move(i, j, player, 'bottom_left')
                    moves.append(State(move.board, self))
        return moves

    def red_moves(self, i, j, king=False):
        moves = []
        if king == False:
            player = 'r'
        else:
            player = 'R'

        if i-1 >= 0 and j+1 < self.width:
            if self.board[i-1][j+1] == '.':
                #move diagonally forward one space to the right
                move = self.make_move(i, j, player, 'bottom_right')
                moves.append(State(move.board, self))
        if i-1 >= 0 and j-1 >= 0:
            if self.board[i-1][j-1] == '.':
                #move diagonally forward one space to the left
                move =(self.make_move(i, j, player, 'bottom_left'))
                moves.append(State(move.board, self))
        if king == True:
            if i+1 < self.height and j+1 < self.width:
                if self.board[i+1][j+1] == '.':
                    #move diagonally backwards one space to the right
                    move=(self.make_move(i, j, player, 'top_right'))
                    moves.append(State(move.board, self))
            if i+1 < self.height and j-1 >= 0:
                if self.board[i+1][j-1] == '.':
                    #move diagonally backwards one space to the left
                    move = (self.make_move(i, j, player, 'top_left'))
                    moves.append(State(move.board, self))
        return moves
    
    '''recursive function red_jump to check multi jumps'''
    def black_jumps(self, i, j, king=False, jumps=None, current_jump_list=None, board=None, king_flag=False,parent=None):
        if jumps is None:
            jumps = []
        if current_jump_list is None:
            current_jump_list = []
        if board is None:
            board = self.board
        if parent is None:
            parent = self.parent

        opp_char = ['r', 'R']
        if king:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            player = 'B'
        else:
            directions = [(1, 1), (1, -1)]
            player = 'b'

        # check for jumps in all directions
        for direction in directions:
            next_i = i + 2 * direction[0]
            next_j = j + 2 * direction[1]
            over_i = i + direction[0]
            over_j = j + direction[1]

            if next_i >= 0 and next_j >= 0 and next_i < self.height and next_j < self.width and self.board[over_i][over_j] in opp_char and self.board[next_i][next_j] == '.':
                # create a new board for each possible jump
                new_board = copy.deepcopy(self)
                new_board,king_flag = new_board.make_jump(i, j, player, direction)

                # add the jump to the list of jumps
                jumps.append(((i, j), direction))
               

                # recurse with the new board and current_jump_list
                new_board.black_jumps(next_i, next_j, king=king, jumps=None, current_jump_list=current_jump_list,board=board,king_flag=king_flag,parent=parent)

        if  len(jumps) > 0:
            # if this piece is not a king and there are jumps available, return the current_jump_list
            return current_jump_list
        
        # otherwise, append the current board to the current_jump_list and return it
        if self.board != board:
            current_jump_list.append(State(self.board, parent))
        return current_jump_list


    def red_jumps(self, i, j, king=False, jumps=None, current_jump_list=None, board=None, king_flag=False,parent=None):
        if jumps is None:
            jumps = []
        if current_jump_list is None:
            current_jump_list = []
        if board is None:
            board = self.board
        if parent is None:
            parent = self.parent

        opp_char = ['b', 'B']
        if king:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            player = 'R'
        else:
            directions = [(-1, 1), (-1, -1)]
            player = 'r'
        
        # check for jumps in all directions
        for direction in directions:
            next_i = i + 2 * direction[0]
            next_j = j + 2 * direction[1]
            over_i = i + direction[0]
            over_j = j + direction[1]

            if next_i >= 0 and next_j >= 0 and next_i < self.height and next_j < self.width and self.board[over_i][over_j] in opp_char and self.board[next_i][next_j] == '.':
                # create a new board for each possible jump
                new_board = copy.deepcopy(self)
                new_board,king_flag = new_board.make_jump( i, j, player, direction)

                # add the jump to the list of jumps
                jumps.append(((i, j), direction))
                # print("calling red_jumps with next_i=", next_i, "next_j=", next_j, "jumps=", jumps, "current_jump_list=", current_jump_list, "king_flag=", king_flag)
                # recurse with the new board and current_jump_list
                new_board.red_jumps(next_i, next_j, king=king, jumps=None, current_jump_list=current_jump_list, board=board, king_flag=king_flag, parent=parent)

        if len(jumps) > 0:
            # if this piece is not a king and there are jumps available, return the current_jump_list
            return current_jump_list
      

        # otherwise, append the current board to the current_jump_list and return it
        if self.board != board:
            current_jump_list.append(State(self.board, parent))
        return current_jump_list
    

    def get_moves(self, i, j, player, jumped=False, jumps=[], overall_jumps=[],moves=[]):
        # moves = []
        # jumps = []
        if player in ['b','B']:
            if self.board[i][j] == 'b':
                #call function to return all possible moves for a red piece
                if jumped == False:
                    moves.extend(self.black_moves(i,j,king=False))
                #check for jumps
                #call red_jumps() function
                jumps.extend(self.black_jumps(i,j,king=False))
            elif self.board[i][j] == 'B':
                #call function to return all possible moves for a red piece
                if jumped == False:
                    moves.extend(self.black_moves(i,j,king=True))
                jumps.extend(self.black_jumps(i,j,king=True))
        elif player in ['r','R']:
            if self.board[i][j] == 'r':
                #call function to return all possible moves for a red piece
                if jumped == False:
                    moves.extend(self.red_moves(i,j,king=False))
                #check for jumps
                #call red_jumps() function
                jumps.extend(self.red_jumps(i,j,king=False))
            elif self.board[i][j] == 'R':
                #call function to return all possible moves for a red piece
                if jumped == False:
                    moves.extend(self.red_moves(i,j,king=True))
                jumps.extend(self.red_jumps(i,j,king=True))

        if len(jumps)!=0:
            return jumps, True
        else:
            return moves, False
        
    '''terminal function to check if all the pieces on the board belongs to the same player by looping through the board'''
  
    def is_terminal_state(self,player):
        players = set()
        if len(self.get_successors(player))==0:
            return True
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != '.':
                    players.add(self.board[i][j].lower())
                    if len(players) > 1:
                        return False
        
        return True

    '''finds winner given terminal state'''
    def terminal_utility(self,mega_player,player,depth):
        # if self.is_terminal_state(player) == True: 
            # for i in range(self.height):
            #     for j in range(self.width):
            #         if self.board[i][j] != '.' and self.board[i][j].lower() != mega_player:
            #             # return float('-inf')
            #             return (-100000*(depth+1))
            # return (100000*(depth+1))
        #count the number of pieces on the board for each player
        r_count = 0
        b_count = 0
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j].lower() == 'r':
                    r_count += 1
                elif self.board[i][j].lower() == 'b':
                    b_count += 1

        if mega_player == 'r':
            if r_count == 0:
                return -99999*(depth+1)
            elif b_count == 0:
                return 99999*(depth+1)
        elif mega_player == 'b':
            if r_count == 0:
                return 99999*(depth+1)
            elif b_count == 0:
                return -99999*(depth+1)
        if player == mega_player:
            return -99999*(depth+1)
        elif player != mega_player:
            return 99999*(depth+1)


    
    #if you reached a terminal state and its the other persons turn then you win otherwise you lose Megaplayer == player
    def get_utility(self, player):
        utility = 0
        opp_char = get_opp_char(player)
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == player.lower():
                    utility += 1
                elif self.board[i][j] == player.upper():
                    utility += 2
                if self.board[i][j] == opp_char[0]:
                    utility -= 1
                elif self.board[i][j] == opp_char[1]:
                    utility -= 2
        return utility
    
    def make_jump(self, i, j, player, direction):
        new_board = copy.deepcopy(self.board)
        jumped_over = []  # to keep track of jumped-over pieces
        king_flag = False
        row, col = direction
        if row == -1 and col == 1:  # top right
            new_board[i-2][j+2] = player
            new_board[i][j] = '.'
            new_board[i-1][j+1] = '.'
            jumped_over.append((i-2, j+2))
        elif row == -1 and col == -1:  # top left
            new_board[i-2][j-2] = player
            new_board[i][j] = '.'
            new_board[i-1][j-1] = '.'
            jumped_over.append((i-2, j-2))
        elif row == 1 and col == 1:  # bottom right
            new_board[i+2][j+2] = player
            new_board[i][j] = '.'
            new_board[i+1][j+1] = '.'
            jumped_over.append((i+2, j+2))
        elif row == 1 and col == -1:  # bottom left
            new_board[i+2][j-2] = player
            new_board[i][j] = '.'
            new_board[i+1][j-1] = '.'
            jumped_over.append((i+2, j-2))

        #loop through jumped_over and check if red piece is at i=0 or black piece is at i=7
        for pos in jumped_over:
            x,y = pos
            if pos[0]==0 and player =='r':
                new_board[x][y]='R'
                king_flag = True
            elif pos[0]==7 and player =='b':
                new_board[x][y]='B'
                king_flag = True
            # Promote the piece to a king if it reaches the last row for its color


        new_board = State(new_board, self)
        return new_board, king_flag


    
    
def alpha_beta(state, depth, player, explored):

    v = max_value(state, depth, -math.inf, math.inf, player,player, explored)
    # print(v)
    final_board = v[1]
    # new_display(final_board)
    #  print("#####")
    while final_board.parent is not state:
        # new_display(final_board)
        final_board = final_board.parent
    
        
    return final_board


def max_value(state, depth, alpha, beta, player, mega_player, explored):
    if state.is_terminal_state(player):
        return state.terminal_utility(mega_player,player,depth), state
    elif depth ==0:
        return state.get_utility(mega_player), state

    value = -math.inf
    best_state = None
    v = (value, best_state)
    successors = state.get_successors(player)
    if len(successors)==0:
        print("HI")
   
    # print(successors)
    opp = get_opp_char(player)[0]
    #print all the boards in successors

    successors.sort(key=lambda x: x.get_utility(player), reverse=True) # sort successors by utility in descending order
    for child_state in successors:
        # if child_state in explored:
        #     continue
        child_state.parent = state
        # new_display(child_state)
        ab_ret = min_value(child_state, depth-1, alpha, beta, opp,mega_player,explored)
        if ab_ret[0] >= v[0]:
            v= ab_ret
            #best_state = child_state
        if v[0] >= beta:
            return v
        alpha = max(alpha, v[0])

        if v[1] ==None: 
            print("here")
        
    return v

            ### if v>+beta: return v, alpha = max(alpha,v)
       
def min_value(state, depth, alpha, beta, player, mega_player, explored):

   
    if state.is_terminal_state(player):
        return state.terminal_utility(mega_player,player,depth), state
    elif depth ==0:
        return state.get_utility(mega_player), state
        
    value = math.inf
    best_state = None
    v = (value, best_state)
    opp = get_opp_char(player)[0]
    successors = state.get_successors(player)
    if len(successors)==0:
        print("HI")
    
    # print(successors)
    successors.sort(key=lambda x: x.get_utility(player), reverse=False) # sort successors by utility in ascending order
    for child_state in successors: #generate state with turn not player (turn changes every call)
        # if child_state in explored:
        #     continue
        # new_display(child_state)
        child_state.parent  = state
        ab_ret = max_value(child_state, depth-1, alpha, beta, opp,mega_player,explored)
        if ab_ret[0] <= v[0]:
            v = ab_ret

        if v[0]<= alpha:
                return v
        beta = min(beta,v[0])

        if v[1] ==None: 
            print("here")
    return v

'''
def find_best_move(state, depth, alpha, beta, maximizingPlayer, player):
    _, best_state = alpha_beta(state, depth, alpha, beta, maximizingPlayer, player)
    moves = []
    while best_state.parent is not None:
        moves.append(best_state.board)
        best_state = best_state.parent
    moves.append(best_state.board)
    moves.reverse()
    return moves
'''
'''
def iterative_deepening_search(state, depth, alpha, beta, maximizingPlayer, player):
    max_depth = 5
    cache = {}
    explored_states = set()
    while True:
        _, best_state = alpha_beta(state, max_depth, alpha, beta, maximizingPlayer, player, explored_states)
        if best_state.is_terminal_state():
            return best_state
        state = best_state
        new_display(state)
        explored_states.add(state)
        max_depth += 1

'''
def play(state,turn,depth):
    path =[]
    path.append(state)
    i=0
    while not state.is_terminal_state(turn):
        state = alpha_beta(state, depth, turn, set())
        turn = get_next_turn(turn)
        path.append(state)
        print(i)
        new_display(state)
        i+=1
    return path

   


def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

'''function to write solution steps to file'''
def write_to_file(path, filename):
    # open the file for writing
    with open(filename, 'w') as file:
        # for each row in the board
        for boards in path:
            for row in boards.board:
                # convert the row to a string
                row_str = ''.join(row)
                # write the row to the file
                file.write(row_str + '\n')
            file.write('\n')

# def find_path(temp):
#     while temp.parent != None:
#         '''backtrack through the parent of each state and add it to the path'''
#         path.append(temp)
#         temp = temp.parent
#     path.append(temp)
#     path = path[::-1]
#     return path

def new_display(board):
    for row in board.board:
        for square in row:
            print(square, end="")
        print("")
    print("")

if __name__ == '__main__':
    

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    # initial_board = read_from_file('checkers2.txt')
    state = State(initial_board)
    # state.display()
    # print('*****')
    # terminal = state.is_terminal()
    # util = state.terminal_utility('r')
    # total_util = state.get_utility('r')
    # print(terminal)
    # print(util)
    # a = state.get_successors('r')
    # new_display(a[0])
    # print(len(a))
    # #use new_display() to print each board in a
    # for board in a:
    #     new_display(board)

    # set the initial values for depth, alpha, beta, and maximizingPlayer
    depth = 7


    alpha = -math.inf
    beta = math.inf
    maximizingPlayer = True

   
    # # print the sequence of boards that leads to the best move
    # print(best_move)


    turn = 'r'
    player = 'r'
    # alpha_beta(state, depth, turn, set())
    time1 = time.time()
    path = play(state,player, depth)
    write_to_file(path, args.outputfile)
    time2 = time.time()
    print(time2-time1)
    ctr = 0


    # sys.stdout = open(args.outputfile, 'w')

    # sys.stdout = sys.__stdout__

