import numpy as np


# TODO create matrix

class Cell:
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def get_coords(self):
        return (self.col, self.line)


#
# class Block_Cell(Cell):
#     def __init__(self, line, col):
#         Cell.__init__(line=line, col= col)


class Succsess_Cell(Cell):
    def __init__(self, line, col, bonus):
        Cell.__init__(self, line=line, col=col)
        self.bonus = bonus


class Defeat_Cell(Cell):
    def __init__(self, line, col, punishment):
        Cell.__init__(self, line=line, col=col)
        self.punishment = punishment


class Rules:
    # alt_moves_dict = {  # what to do if original move is unavailable
    #     'top': ['left', 'right'],
    #     'right': ['top', 'bot'],
    #     'bot': ['left', 'right'],
    #     'left': ['top', 'bot']
    # }
    moves_dirs = {
        'top': (-1, 0),
        'right': (0, 1),
        'bot': (1, 0),
        'left': (0, -1)
    }


class Move:
    def __init__(self, dirs_and_probabilities_dict):
        # self.dir_name = dir_name
        self.moves_dict = dirs_and_probabilities_dict  # inserting direction and probabilities


class Field:
    def __init__(self, rules, cols, lines, moves, blocked_cells_list, succsess_cells_list, defeat_cells_list):
        self.rules = rules
        self.moves = moves
        self.cols = cols
        self.lines = lines
        self.np_matrix = np.zeros(shape=(len(self.moves), lines * cols, lines * cols))
        # as generating square transition matrices for each of M possible transitions
        self.blocked_cells = blocked_cells_list
        pass

    def index_from_coords(self, x, y):
        return y * self.cols + x

    def coords_from_index(self, index):
        return (index % self.cols, index // self.cols)

    def position_is_possible(self, final_position):
        if 0 <= final_position[0] < self.cols and \
                                0 <= final_position[1] < self.lines and \
                        final_position not in self.blocked_cells:
            return True
        else:
            return False

    def fill_transition_matrix(self):
        for move_indx in range(len(self.moves)):  # switching over moves
            for y in range(self.lines):
                for x in range(self.cols):
                    start_position_indx = self.index_from_coords(x=x, y=y)

                    for transition_name in self.moves[move_indx].moves_dict:
                        exactly_this_transition_prob = self.moves[move_indx].moves_dict[transition_name]
                        if exactly_this_transition_prob <= 0: continue  # case of absent probability
                        transition_offset = self.rules.moves_dirs[transition_name]
                        final_position_coords = (x + transition_offset[0], y + transition_offset[1])
                        final_position_indx = self.index_from_coords(x=final_position_coords[0],
                                                                     y=final_position_coords[1])

                        if self.position_is_possible(final_position_coords):
                            self.np_matrix[move_indx][start_position_indx][
                                final_position_indx] += exactly_this_transition_prob
                        else:  # case of impossible final_transition
                            self.np_matrix[move_indx][start_position_indx][
                                start_position_indx] += exactly_this_transition_prob


                            # if (x,y) == (1, 2):
                            #     self.np_matrix[move_indx][x][y] = move_indx

        pass

    def get_transition_matrix(self):
        return self.np_matrix

    def pretty_print(self):
        for m in range(len(self.moves)):
            print(" FOR MOVE #" + str(m) + "<== trbl")
            for k in range(self.cols * self.lines):
                print("from cell" + str(self.coords_from_index(k)))
                for x in range(self.cols):
                    line = ""
                    for y in range(self.lines):
                        line += str(self.np_matrix[m][k][self.index_from_coords(x=x, y=y)]) + " "
                    print(line)

        pass


list_of_blocked_cells = [(1, 1)]  # coords
finish_list = []  # good_endgame
death_list = []  # bad andgame

move_top = Move(dirs_and_probabilities_dict={'top': 0.8, 'bot': 0.0, 'left': 0.1, 'right': 0.1})
move_right = Move(dirs_and_probabilities_dict={'top': 0.1, 'bot': 0.1, 'left': 0.0, 'right': 0.8})
move_bot = Move(dirs_and_probabilities_dict={'top': 0.0, 'bot': 0.8, 'left': 0.1, 'right': 0.1})
move_left = Move(dirs_and_probabilities_dict={'top': 0.1, 'bot': 0.1, 'left': 0.8, 'right': 0.0})

field_object = Field(Rules(),
                     cols=4,
                     lines=3,
                     moves=[move_top, move_right, move_bot, move_left],
                     blocked_cells_list=list_of_blocked_cells,
                     succsess_cells_list=finish_list,
                     defeat_cells_list=death_list)

field_object.fill_transition_matrix()

field_object.pretty_print()

# print(field_object.np_matrix)



print(1 < 2 < 3)

print(10 % 3, 10 // 3)

c1 = field_object.index_from_coords(2, 3)
c2 = field_object.coords_from_index(c1)
print(c1)
print(c2)
