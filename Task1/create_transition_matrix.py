import numpy as np


class Cell:
    def __init__(self, line, col):
        self.line = line
        self.col = col

    def get_coords(self):
        return (self.col, self.line)


class Succsess_Cell(Cell):
    def __init__(self, line, col, bonus):
        Cell.__init__(self, line=line, col=col)
        self.bonus = bonus


class Defeat_Cell(Cell):
    def __init__(self, line, col, punishment):
        Cell.__init__(self, line=line, col=col)
        self.punishment = punishment


class Rules:
    moves_dirs = {
        'top': (-1, 0),
        'right': (0, 1),
        'bot': (1, 0),
        'left': (0, -1)
    }


class Move:
    def __init__(self, dirs_and_probabilities_dict):
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
        self.succsess_cells_list = succsess_cells_list
        self.defeat_cells_list = defeat_cells_list
        pass

    def index_from_coords(self, y, x):
        return y * self.cols + x

    def coords_from_index(self, index):
        return (index // self.cols, index % self.cols)

    def position_is_blocked(self, position):
        return position in self.blocked_cells

    def position_is_possible(self, final_position):
        return 0 <= final_position[0] < self.lines and \
               0 <= final_position[1] < self.cols and \
               not self.position_is_blocked(final_position)

    def is_terminal_state(self, y_coord, x_coord):
        return (y_coord, x_coord) in self.succsess_cells_list or (y_coord, x_coord) in self.defeat_cells_list

    def fill_transition_matrix(self):

        # filing special cells to preserv "Markov" matrix --- contraidcts to decision method
        # for a in range(len(self.moves)):
        #     for el in self.blocked_cells:
        #         self.np_matrix[a][self.index_from_coords(x=el[1], y=el[0])][self.index_from_coords(x=el[1], y=el[0])] = 1
        #     for el in self.defeat_cells_list:
        #         self.np_matrix[a][self.index_from_coords(x=el[1], y=el[0])][self.index_from_coords(x=el[1], y=el[0])] = 1
        #     for el in self.succsess_cells_list:
        #         self.np_matrix[a][self.index_from_coords(x=el[1],y= el[0])][self.index_from_coords(x=el[1], y=el[0])] = 1

        for move_indx in range(len(self.moves)):  # switching over moves
            for y in range(self.lines):
                for x in range(self.cols):

                    start_coords = (y, x)
                    start_position_indx = self.index_from_coords(x=x, y=y)
                    if self.is_terminal_state(x_coord=x, y_coord=y) or self.position_is_blocked((y, x)):
                        continue

                    for transition_name in self.moves[move_indx].moves_dict:
                        exactly_this_transition_prob = self.moves[move_indx].moves_dict[transition_name]
                        if exactly_this_transition_prob <= 0: continue  # case of absent probability
                        transition_offset = self.rules.moves_dirs[transition_name]
                        final_position_coords = (y + transition_offset[0], x + transition_offset[1])
                        final_position_indx = self.index_from_coords(x=final_position_coords[1],
                                                                     y=final_position_coords[0])

                        if self.position_is_possible(final_position_coords):
                            self.np_matrix[move_indx][start_position_indx][
                                final_position_indx] += exactly_this_transition_prob
                        else:  # case of impossible final_transition
                            self.np_matrix[move_indx][start_position_indx][
                                start_position_indx] += exactly_this_transition_prob

    def get_transition_matrix(self):
        return self.np_matrix

    def pretty_print(self):
        for m in range(len(self.moves)):
            print("============ FOR MOVE #" + str(m) + "<== T_R_B_L ===clockwise====")
            for k in range(self.cols * self.lines):
                print("===== from cell" + str(self.coords_from_index(k)))
                for y in range(self.lines):

                    line = ""
                    for x in range(self.cols):
                        if (y, x) == (1, 1):
                            line += " *  "
                            continue
                        line += str(self.np_matrix[m][k][self.index_from_coords(x=x, y=y)]) + " "
                    print(line)


list_of_blocked_cells = [(1, 1)]  # coords
finish_list = [(0, 3)]  # good_endgame
death_list = [(1, 3)]  # bad andgame

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

np.save('T', field_object.get_transition_matrix())
# print(field_object.get_transition_matrix())
