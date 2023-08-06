class Machine:
    def __init__(self):
        self.__alphabet = []
        self.__states = {}
        self.__program = {}
        self.__initial_state = ""

    def set_alphabet(self, new_alpha):
        self.__alphabet = new_alpha

    def set_states(self, new_states):
        self.__initial_state = new_states[0]
        for state in new_states:
            self.__states[state] = False

    def set_halting_states(self, halting_states):
        for state in halting_states:
            self.__states[state] = True

    def is_symbol(self, to_check):
        return to_check and self.__alphabet.__contains__(to_check)

    def is_state(self, to_check):
        return to_check and self.__states.__contains__(to_check)

    @staticmethod
    def is_direction(to_check):
        return to_check and ["L", "R"].__contains__(to_check.upper())

    def is_halt(self, state):
        if not self.is_state(state):
            raise ValueError("The state is not a state of the turing machine (state not in self.states)")
        return self.__states[state]

    def set_program(self, new_program):
        self.__program = new_program

    def get_program(self):
        return self.__program

    def get_first_state(self):
        return self.__initial_state

    def get_states(self):
        return self.__states

    def get_alphabet(self):
        return self.__alphabet

    def get_blank(self):
        return self.__alphabet[0]
