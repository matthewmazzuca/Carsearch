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
# The search space class 'rushhour'             #
# This class is a sub-class of 'StateSpace'      #
##################################################
class Car:
  def __init__(self, iden, loc, is_horizontal, length, is_goal, board_size):
    # board dim and loc are tuples
    self.iden = iden
    self.loc = loc
    self.x = self.loc[0]
    self.y = self.loc[1]
    self.is_horizontal = is_horizontal
    self.length = length
    self.is_goal = is_goal
    self.board_size = board_size
    self.board_width = board_size[0]
    self.board_height = board_size[1]

    if self.is_horizontal:
      self.end_x = self.x + (self.length-1)
      self.end_y = self.y
    else:
      self.end_x = self.x
      self.end_y = self.y + self.length-1

class rushhour(StateSpace):
    def __init__(self, action, gval, vehicles, goal_loc, goal_orient, board_size, parent = None ):
      StateSpace.__init__(self, action, gval, parent)
      self.vehicles = vehicles
      self.goal_loc = goal_loc
      self.goal_orient = goal_orient
      self.board_size = board_size



    def successors(self):
#IMPLEMENT
        '''Return list of rushhour objects that are the successors of the current object'''

        successors = []

        for car in self.vehicles:
          if self.check_collision_forward(car):
            curr = car
            new = self.move_forward(curr)
            new_vehicles = copy.deepcopy(self.vehicles)

            for i in range(len(new_vehicles)):
              if new_vehicles[i].iden == curr.iden:
                new_vehicles[i] = new

            if car.is_horizontal:
              action = "move_vehicle(" + new.iden + ", W)"
            else:
              action = "move_vehicle(" + new.iden + ", N)"
            # print(self.gval)

            successors.append(rushhour(action, self.gval+1, new_vehicles, 
                          self.goal_loc, self.goal_orient, self.board_size, self))
          

          if self.check_collision_backward(car):
            curr = car
            new = self.move_backward(curr)
            new_vehicles = copy.deepcopy(self.vehicles)

            for i in range(len(new_vehicles)):
              if new_vehicles[i].iden == curr.iden:
                new_vehicles[i] = new

            if car.is_horizontal:
              action = "move_vehicle(" + new.iden + ", E)"
            else:
              action = "move_vehicle(" + new.iden + ", S)"
            # print(self.gval)

            successors.append(rushhour(action, self.gval+1, new_vehicles, 
                          self.goal_loc, self.goal_orient, self.board_size, self))
          

        return successors


          # if curr.



    def check_back(self, vehicle):
      # check back of car to see if it can go backwards
      if vehicle.is_horizontal:
        if vehicle.x == vehicle.board_width:
          return False
        else:
          return True
      else:
        if vehicle.y == vehicle.board_height:
          return False
        else:
          return True


    def check_forward(self, vehicle):
      # check if vehicle will hit wall going forward

      if vehicle.is_horizontal:
        if vehicle.x == 0:
          return False
        else:
          return True
      else:
        if vehicle.y == 0:
          return False
        else:
          return True

    def check_collision(self, args=0):
      # check for collisions given all cars
      # check for changes in forward/backward
      if args != 0:
        cars = []
        for arg in args:
          cars.append(arg)
      else:
        cars = self.vehicles

      # normal iteration

      spaces = []
      for car in cars:
        temp = self.taken_spaces(car)
        for i in temp:
          if i in spaces:
            return False
          else:
            spaces.append(i)

      return True

    def check_collision_forward(self, vehicle):
      # check for collisions given all cars forward
      testing = [ ]
      for car in self.vehicles:
        if car.iden == vehicle.iden:
          testing.append(self.move_forward(vehicle))
        else:
          testing.append(car)

      return self.check_collision(testing)

    def check_collision_backward(self, vehicle):
      # check for collisions given all cars backward
      testing = [ ]
      for car in self.vehicles:
        if car.iden == vehicle.iden:
          testing.append(self.move_backward(vehicle))
        else:
          testing.append(car)

      return self.check_collision(testing)

    def move_forward(self, vehicle):

      # copy vehicle structure
      new_vehicle = copy.deepcopy(vehicle)
      # for testing
      # print(new_vehicle.loc)
      # print(new_vehicle.x, new_vehicle.y)

      if vehicle.is_horizontal:
        new_vehicle.x = (new_vehicle.x - 1) % self.board_size[0]
        new_vehicle.loc = ((new_vehicle.loc[0]-1) % self.board_size[0], new_vehicle.loc[1])
        new_vehicle.end_x = (new_vehicle.end_x - 1) % self.board_size[0]
      else:
        new_vehicle.y = (new_vehicle.y + 1) % self.board_size[1]
        new_vehicle.loc = (new_vehicle.loc[0], (new_vehicle.loc[1] + 1) % self.board_size[1]) 
        new_vehicle.end_y = (new_vehicle.end_y + 1) % self.board_size[1]


      return new_vehicle

    def move_backward(self, vehicle):

      new_vehicle = copy.deepcopy(vehicle)

      if vehicle.is_horizontal:
        new_vehicle.x = (new_vehicle.x + 1) % self.board_size[0]
        new_vehicle.loc = ((new_vehicle.loc[0] + 1) % self.board_size[0], new_vehicle.loc[1])
        new_vehicle.end_x = (new_vehicle.end_x + 1) % self.board_size[0]
      else:
        new_vehicle.y = (new_vehicle.y - 1) % self.board_size[1]
        new_vehicle.loc = (new_vehicle.loc[0], (new_vehicle.loc[1]-1) % self.board_size[1])
        new_vehicle.end_y = (new_vehicle.end_y - 1) % self.board_size[1]

      return new_vehicle


    def taken_spaces(self, vehicle):
      # to return list of tuples representing taken vehicles
      ret_list = []
      if vehicle.is_horizontal:
        for i in range(vehicle.length):
          ret_list.append((vehicle.x + i, vehicle.y))
      else:
        for i in range(vehicle.length):
          ret_list.append((vehicle.x, vehicle.y + i))

      return ret_list

    def hashable_state(self):
#IMPLEMENT
        '''Return a data item that can be used as a dictionary key to UNIQUELY represent the state.'''

        string = "\n" + "\n"  + "=========New State=========" + "\n" + \
                "- - - - - - -Global Parameters - - - - - - -" + "\n" \
                "goal location: " + str(self.goal_loc) + ";"+ "\n" + \
                "goal direction: " + str(self.goal_orient) + ";" + "\n" + \
                "board width: " + str(self.board_size[0]) + ";" + "\n" + \
                "board height: " + str(self.board_size[1]) + ";" + "\n" + \
                "- - - - - - - - - - - - - - - - - - - - - - -" + "\n" + \
                "Car Id" + "\t" + "X" + "\t" + "Y" + "\t" + "length" + "\t" + "Horz?" + "\t" + "Is_goal?" + "\n"
        for car in self.vehicles:
            string += str(car.iden) + "\t" + str(car.x) + "\t" +  str(car.y) + "\t" + str(car.length) + "\t" + str(car.is_horizontal) + "\t" + str(car.is_goal) + "\t" + "\n"
        return string

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
           Where <name> is the name of the robot (a string)
                 <loc> is a location (a pair (x,y)) indicating the front of the vehicle,
                       i.e., its length is counted in the positive x- or y-direction
                       from this point
                 <length> is the length of that vehicle
                 <is_horizontal> is true iff the vehicle is oriented horizontally
                 <is_goal> is true iff the vehicle is a goal vehicle

        '''
        status_list = []
        for car in self.vehicles:
            status_list.append([car.iden, (car.x, car.y), car.length, car.is_horizontal, car.is_goal])
        return status_list

    def get_board_properties(self):
#IMPLEMENT
        '''Return (board_size, goal_entrance, goal_direction)
           where board_size = (m, n) is the dimensions of the board (m rows, n columns)
                 goal_entrance = (x, y) is the location of the goal
                 goal_direction is one of 'N', 'E', 'S' or 'W' indicating
                                the orientation of the goal
        '''
        return(self.board_size, self.goal_loc, self.goal_orient)

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
    #1. Proceeding in the first direction, let m1 =
    #   number of moves required to get to the goal if it were unobstructed
    #2. Proceeding in the second direction, let m2 =
    #   number of moves required to get to the goal if it were unobstructed
    #
    #Our heuristic value is the minimum of m1 and m2 over all goal vehicles.
    #You should implement this heuristic function exactly, even if it is
    #tempting to improve it.
    # self.goal_loc = goal_loc
    #   self.goal_orient = goal_orient
    #   self.board_size = board_size

    min_moves = max(state.goal_loc[0], state.goal_loc[1])

    for vehicle in state.vehicles:
        if vehicle.is_goal:
            #check if it is oriented correctly
            if state.goal_orient is 'N' and not vehicle.is_horizontal:

                if state.goal_loc[0] is vehicle.x: #Same column
                    m1 = abs(vehicle.y - state.goal_loc[1])
                    m2 = state.board_size[1] - m1
                    min_moves = min(min_moves, m1, m2)

            elif state.goal_orient is 'S' and not vehicle.is_horizontal:

                if state.goal_loc[0] is vehicle.x: #Same column
                    m1 = abs((vehicle.y + vehicle.length - 1) % state.board_size[0] - state.goal_loc[1])
                    m2 = state.board_size[1] - m1
                    min_moves = min(min_moves, m1, m2)

            elif state.goal_orient is 'W' and vehicle.is_horizontal:

                if state.goal_loc[1] is vehicle.y: #Same row
                    m1 = abs(vehicle.x - state.goal_entrance[0])
                    m2 = state.board_size[0] - m1
                    min_moves = min(min_moves, m1, m2)

            elif state.goal_orient is 'E' and vehicle.is_horizontal:

                if state.goal_loc[1] is vehicle.y: #Same row
                    m1 = abs((vehicle.x + vehicle.length - 1) % state.board_size[1] - state.goal_loc[0])
                    m2 = state.board_size[0] - m1
                    min_moves = min(min_moves, m1, m2)

    return min_moves


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
    # self, iden, loc, is_horizonal, length, is_goal, board_size

    # self, action, gval, vehicles, goal_loc, goal_orient, board_size, 
    # parent = None 

    # self, vehicle_list, goal_entrance, goal_direction, board_size, action, gval, parent
        # s = make_init_state((7, 7), [['gv', (1, 1), 2, True, True],
        #       ['1', (3, 1), 2, False, False],
        #       ['3', (4, 4), 2, False, False]], (4, 1), 'E')

    ret_list = []
    for v in vehicle_list:
        temp = Car(v[0], v[1], v[3], v[2], v[4], board_size)
        ret_list.append(temp)
        # print(temp.iden, temp.loc, temp.start_x, temp.start_y,
        #       temp.is_horizonal, temp.length, temp.is_goal,
        #       temp.board_size, temp.board_width, temp.board_height,
        #       temp.end_x, temp.end_y)

    # return
    # return rushhour(formatted_vehicle_list, goal_entrance, goal_direction, board_size, "START", 0, None)
    return rushhour("START", 0, ret_list, goal_entrance, goal_direction, board_size, None)

    


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
    se.trace_on(1)
    final = se.search(init_state, rushhour_goal_fn, heur_min_moves)
# if __name__ == '__main__':
#     s = make_init_state((7, 7), [['gv', (1, 1), 2, True, True],
#               ['1', (3, 1), 2, False, False],
#               ['3', (4, 4), 2, False, False]], (4, 1), 'E')
#     print(s.vehicles,
#       s.goal_loc,
#       s.goal_orient,
#       s.board_size
# )
#     for v in s.vehicles:
#       print(v.iden)
    # print(s.check_collision_forward(s.vehicles[0])) 
 