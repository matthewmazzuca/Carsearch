#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

'''
rushhour STATESPACE
'''
#   You may add only standard python imports---i.e., ones that are automatically
#   available on CDF.
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

from search import *
from random import randint
import copy

##################################################
# The search space class 'rushhour'              #
# This class is a sub-class of 'StateSpace'      #
##################################################

class Vehicle:
    def __init__(self, name, x, y, length, is_horizontal, is_goal, board_width, board_height):
        self.name = name
        self.x = x
        self.y = y
        self.length = length
        self.is_horizontal = is_horizontal
        self.is_goal = is_goal
        self.board_width = board_width
        self.board_height = board_height

    def head_location(self):
        return [self.x, self.y]

    def tail_location(self):
        if self.is_horizontal:
            return [(self.x + self.length) % board_width, self.y]
        else: #Is vertical
            return [self.x, (self.y + self.length) % board_height]

class rushhour(StateSpace):
    def __init__(self, vehicle_list, goal_entrance, goal_direction, board_size, action, gval, parent):
#IMPLEMENT
        """Initialize a rushhour search state object."""
        super().__init__(action, gval, parent)
        self.vehicle_list = vehicle_list
        self.goal_entrance = goal_entrance
        self.goal_direction = goal_direction
        self.board_width = board_size[1]
        self.board_height = board_size[0]
        self.board_size = board_size

    def successors(self):
#IMPLEMENT
        '''Return list of rushhour objects that are the successors of the current object'''
        successor_list = []
        for index in range(len(self.vehicle_list)):
            current_vehicle = self.vehicle_list[index]
            if self.vehicle_can_move_forward(current_vehicle):
                new_vehicle = copy.deepcopy(current_vehicle)
                self.vehicle_list.remove(current_vehicle)
                new_vehicle_list = copy.deepcopy(self.vehicle_list)
                new_vehicle_list.append(new_vehicle)
                self.vehicle_list.insert(index, current_vehicle)
                action_string = ""
                if new_vehicle.is_horizontal:
                    new_vehicle.x = (current_vehicle.x - 1) % self.board_width
                    action_string = "move_vehicle(" + new_vehicle.name + ", W)"
                else: #Is vertical
                    new_vehicle.y = (current_vehicle.y - 1) % self.board_height
                    action_string = "move_vehicle(" + new_vehicle.name + ", N)"
                successor_list.append(rushhour(new_vehicle_list, self.goal_entrance, self.goal_direction, self.board_size,
                    action_string, self.gval + 1, self))
            if self.vehicle_can_move_backward(current_vehicle):
                new_vehicle = copy.deepcopy(current_vehicle)
                self.vehicle_list.remove(current_vehicle)
                new_vehicle_list = copy.deepcopy(self.vehicle_list)
                new_vehicle_list.append(new_vehicle)
                self.vehicle_list.insert(index, current_vehicle)
                if new_vehicle.is_horizontal:
                    new_vehicle.x = (current_vehicle.x + 1) % self.board_width
                    action_string = "move_vehicle(" + new_vehicle.name + ", E)"
                else: #Is vertical
                    new_vehicle.y = (current_vehicle.y + 1) % self.board_height
                    action_string = "move_vehicle(" + new_vehicle.name + ", S)"
                successor_list.append(rushhour(new_vehicle_list, self.goal_entrance, self.goal_direction, self.board_size,
                    action_string, self.gval + 1, self))
        return successor_list
    
    def vehicle_can_move_forward(self, vehicle):
        for car in self.vehicle_list:
            if vehicle.name != car.name:
                moved_vehicle = copy.deepcopy(vehicle)
                if vehicle.is_horizontal:
                    moved_vehicle.x = (vehicle.x - 1) % self.board_width
                    if set(self.vehicle_occupied_spaces(moved_vehicle)).intersection(set(self.vehicle_occupied_spaces(car))):
                        return False
                else: #Vehicle is vertical
                    moved_vehicle.y = (vehicle.y - 1) % self.board_height
                    if set(self.vehicle_occupied_spaces(moved_vehicle)).intersection(set(self.vehicle_occupied_spaces(car))):
                        return False
        return True
    
    def vehicle_can_move_backward(self, vehicle):
        for car in self.vehicle_list:
            if vehicle.name != car.name:
                moved_vehicle = copy.deepcopy(vehicle)
                if vehicle.is_horizontal:
                    moved_vehicle.x = (vehicle.x + 1) % self.board_width
                    if set(self.vehicle_occupied_spaces(moved_vehicle)).intersection(set(self.vehicle_occupied_spaces(car))):
                        return False
                else: #Vehicle is vertical
                    moved_vehicle.y = (vehicle.y + 1) % self.board_height
                    if set(self.vehicle_occupied_spaces(moved_vehicle)).intersection(set(self.vehicle_occupied_spaces(car))):
                        return False
        return True
    
    def vehicle_occupied_spaces(self, vehicle):
        #Returns a list of spaces which the vehicle is occupying
        #in the format [(x1,y1),(x2,y2),...,(xn,yn)]
        occupied_spaces = []
        if vehicle.is_horizontal:
            for i in range(vehicle.length):
                occupied_spaces.append(((vehicle.x + i) % self.board_width, vehicle.y))
        else:
            for i in range(vehicle.length):
                occupied_spaces.append((vehicle.x, (vehicle.y + i) % self.board_height))
        return occupied_spaces
    
    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''
        key_string = self.goal_entrance, ";", self.goal_direction, ";", self.board_width, ";", self.board_height, ";"
        for vehicle in self.vehicle_list:
            key_string += vehicle.name, ";", vehicle.x, ";", vehicle.y, ";", vehicle.length, ";", vehicle.is_horizontal, ";", vehicle.is_goal, ";"
        return key_string
    
    def print_state(self):
        #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
        #and in generating sample trace output.
        #Note that if you implement the "get" routines
        #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
        #properly, this function should work irrespective of how you represent
        #your state.

        if self.parent:
            print("Action= \"{}\", S{}, g-value = {}, (From S{})".format(self.action, self.index, self.gval, self.parent.index))
        else:
            print("Action= \"{}\", S{}, g-value = {}, (Initial State)".format(self.action, self.index, self.gval))

        print("Vehicle Statuses")
        for vs in sorted(self.get_vehicle_statuses()):
            print("    {} is at ({}, {})".format(vs[0], vs[1][0], vs[1][1]), end="")
        board = get_board(self.get_vehicle_statuses(), self.get_board_properties())
        print('\n')
        print('\n'.join([''.join(board[i]) for i in range(len(board))]))

#Data accessor routines.

    def get_vehicle_statuses(self):
#IMPLEMENT
        '''Return list containing the status of each vehicle
           This list has to be in the format: [vs_1, vs_2, ..., vs_k]
           with one status list for each vehicle in the state.
           Each vehicle status item vs_i is itself a list in the format:
                 [<name>, <loc>, <length>, <is_horizontal>, <is_goal>]
           Where <name> is the name of the vehicle (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle
        '''
        status_list = []
        for vehicle in self.vehicle_list:
            status_list.append([vehicle.name, (vehicle.x, vehicle.y), vehicle.length, vehicle.is_horizontal, vehicle.is_goal])
        return status_list
    
    def get_board_properties(self):
#IMPLEMENT
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return(self.board_size, self.goal_entrance, self.goal_direction)

#############################################
# heuristics                                #
#############################################


def heur_zero(state):
    '''Zero Heuristic use to make A* search perform uniform cost search'''
    return 0


def heur_min_moves(state):
#IMPLEMENT
    '''rushhour heuristic'''
    #We want an admissible heuristic. Getting to the goal requires
    #one move for each tile of distance.
    #Since the board wraps around, there are two different
    #directions that lead to the goal.
    #NOTE that we want an estimate of the number of ADDITIONAL
    #     moves required from our current state
    #1. Proceeding in the first direction, let MOVES1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let MOVES2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of MOVES1 and MOVES2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
    minimum_moves = max(state.board_size[0], state.board_size[1])
    for vehicle in state.vehicle_list:
        if vehicle.is_goal:
            #check if it is oriented correctly
            if state.goal_direction is 'N' and not vehicle.is_horizontal:
                if state.goal_entrance[0] is vehicle.x: #Same column
                    moves1 = abs(vehicle.y - state.goal_entrance[1])
                    moves2 = state.board_height - moves1
                    minimum_moves = min(minimum_moves, moves1, moves2)
            elif state.goal_direction is 'S' and not vehicle.is_horizontal:
                if state.goal_entrance[0] is vehicle.x: #Same column
                    moves1 = abs((vehicle.y + vehicle.length - 1) % state.board_size[0] - state.goal_entrance[1])
                    moves2 = state.board_height - moves1
                    minimum_moves = min(minimum_moves, moves1, moves2)
            elif state.goal_direction is 'W' and vehicle.is_horizontal:
                if state.goal_entrance[1] is vehicle.y: #Same row
                    moves1 = abs(vehicle.x - state.goal_entrance[0])
                    moves2 = state.board_width - moves1
                    minimum_moves = min(minimum_moves, moves1, moves2)
            elif state.goal_direction is 'E' and vehicle.is_horizontal:
                if state.goal_entrance[1] is vehicle.y: #Same row
                    moves1 = abs((vehicle.x + vehicle.length - 1) % state.board_size[1] - state.goal_entrance[0])
                    moves2 = state.board_width - moves1
                    minimum_moves = min(minimum_moves, moves1, moves2)
    return minimum_moves

def rushhour_goal_fn(state):
#IMPLEMENT
    '''Have we reached a goal state'''
    return not heur_min_moves(state)

def make_init_state(board_size, vehicle_list, goal_entrance, goal_direction):
#IMPLEMENT
    '''Input the following items which specify a state and return a rushhour object
       representing this initial state.
         The state's its g-value is zero
         The state's parent is None
         The state's action is the dummy action "START"
       board_size = (m, n)
          m is the number of rows in the board
          n is the number of columns in the board
       vehicle_list = [v1, v2, ..., vk]
          a list of vehicles. Each vehicle vi is itself a list
          vi = [vehicle_name, (x, y), length, is_horizontal, is_goal] where
              vehicle_name is the name of the vehicle (string)
              (x,y) is the location of that vehicle (int, int)
              length is the length of that vehicle (int)
              is_horizontal is whether the vehicle is horizontal (Boolean)
              is_goal is whether the vehicle is a goal vehicle (Boolean)
      goal_entrance is the coordinates of the entrance tile to the goal and
      goal_direction is the orientation of the goal ('N', 'E', 'S', 'W')

   NOTE: for simplicity you may assume that
         (a) no vehicle name is repeated
         (b) all locations are integer pairs (x,y) where 0<=x<=n-1 and 0<=y<=m-1
         (c) vehicle lengths are positive integers
    '''

    # self, name, x, y, length, is_horizontal, is_goal, board_width, board_height
    formatted_vehicle_list = []
    for vehicle in vehicle_list:
        formatted_vehicle_list.append(Vehicle(vehicle[0], vehicle[1][0], vehicle[1][1],
            vehicle[2], vehicle[3], vehicle[4], board_size[1], board_size[0]))
    return rushhour(formatted_vehicle_list, goal_entrance, goal_direction, board_size, "START", 0, None)
    

########################################################
#   Functions provided so that you can more easily     #
#   Test your implementation                           #
########################################################


def get_board(vehicle_statuses, board_properties):
    #DO NOT CHANGE THIS FUNCTION---it will be used in auto marking
    #and in generating sample trace output.
    #Note that if you implement the "get" routines
    #(rushhour.get_vehicle_statuses() and rushhour.get_board_size())
    #properly, this function should work irrespective of how you represent
    #your state.
    (m, n) = board_properties[0]
    board = [list(['.'] * n) for i in range(m)]
    for vs in vehicle_statuses:
        for i in range(vs[2]):  # vehicle length
            if vs[3]:
                # vehicle is horizontal
                board[vs[1][1]][(vs[1][0] + i) % n] = vs[0][0]
                # represent vehicle as first character of its name
            else:
                # vehicle is vertical
                board[(vs[1][1] + i) % m][vs[1][0]] = vs[0][0]
                # represent vehicle as first character of its name
    # print goal
    board[board_properties[1][1]][board_properties[1][0]] = board_properties[2]
    return board


def make_rand_init_state(nvehicles, board_size):
    '''Generate a random initial state containing
       nvehicles = number of vehicles
       board_size = (m,n) size of board
       Warning: may take a long time if the vehicles nearly
       fill the entire board. May run forever if finding
       a configuration is infeasible. Also will not work any
       vehicle name starts with a period.

       You may want to expand this function to create test cases.
    '''

    (m, n) = board_size
    vehicle_list = []
    board_properties = [board_size, None, None]
    for i in range(nvehicles):
        if i == 0:
            # make the goal vehicle and goal
            x = randint(0, n - 1)
            y = randint(0, m - 1)
            is_horizontal = True if randint(0, 1) else False
            vehicle_list.append(['gv', (x, y), 2, is_horizontal, True])
            if is_horizontal:
                board_properties[1] = ((x + n // 2 + 1) % n, y)
                board_properties[2] = 'W' if randint(0, 1) else 'E'
            else:
                board_properties[1] = (x, (y + m // 2 + 1) % m)
                board_properties[2] = 'N' if randint(0, 1) else 'S'
        else:
            board = get_board(vehicle_list, board_properties)
            conflict = True
            while conflict:
                x = randint(0, n - 1)
                y = randint(0, m - 1)
                is_horizontal = True if randint(0, 1) else False
                length = randint(2, 3)
                conflict = False
                for j in range(length):  # vehicle length
                    if is_horizontal:
                        if board[y][(x + j) % n] != '.':
                            conflict = True
                            break
                    else:
                        if board[(y + j) % m][x] != '.':
                            conflict = True
                            break
            vehicle_list.append([str(i), (x, y), length, is_horizontal, False])

    return make_init_state(board_size, vehicle_list, board_properties[1], board_properties[2])


def test(nvehicles, board_size):
    s0 = make_rand_init_state(nvehicles, board_size)
    se = SearchEngine('astar', 'full')
    #se.trace_on(2)
    final = se.search(s0, rushhour_goal_fn, heur_min_moves)
    
def case_test(init_state, method = None):
    if method is None:
        method = 'astar'
    se = SearchEngine(method, 'full')
    final = se.search(init_state, rushhour_goal_fn, heur_min_moves)
