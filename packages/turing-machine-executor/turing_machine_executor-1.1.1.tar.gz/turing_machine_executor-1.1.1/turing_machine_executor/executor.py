import turing_machine_executor.machine


class Executor:
    def __init__(self, turing_machine, input_tape):
        self.__machine = turing_machine
        self.__output = [turing_machine.get_blank()] + input_tape + [turing_machine.get_blank()]

    def exec(self, step_by_step=False):
        program = self.__machine.get_program()
        current_state = self.__machine.get_first_state()
        i = 0
        if step_by_step:
            self.print_tape(self.__output, i, str(current_state) + ":", True)
        while not self.__machine.is_halt(current_state):
            read = self.__output[i]
            direction = program[(read, current_state)][1]
            self.__output[i] = program[(read, current_state)][0]
            current_state = program[(read, current_state)][2]
            i = i + 1 if direction == "R" else i - 1
            if i >= len(self.__output):
                self.__output += ([self.__machine.get_blank()] * (i - len(self.__output) + 1))
            if step_by_step:
                self.print_tape(self.__output, i, str(current_state) + ":", True)

    def get_output(self):
        return self.__output

    def print_tape(self, tape, index=-1, beginning_string="", print_all_blanks=False):
        if beginning_string:
            print(beginning_string, end=" ")
        printed_something = False
        for char in tape:
            if char != self.__machine.get_blank() or print_all_blanks or printed_something:
                print(char, end="")
        print()
        if index != -1:
            print(" " * len(beginning_string), end="")
            print(" " * (index + 1), end="")
            print("^")
