def elfish_computer(instruction_sequence):
    instruction_ptr = 0
    while True:
        instruction = instruction_sequence[instruction_ptr]
        if instruction == 1:
            execute_operation(instruction_ptr, instruction_sequence, "add")
            instruction_ptr += 4
        elif instruction == 2:
            execute_operation(instruction_ptr, instruction_sequence, "mult")
            instruction_ptr += 4
        elif instruction == 99:
            instruction_ptr += 1
            break
        else:
            print("Illegal instruction detected, stopping execution.")
            break


def execute_operation(instruction_ptr, intcode, operator):
    ptr_a = intcode[instruction_ptr + 1]
    ptr_b = intcode[instruction_ptr + 2]
    value_a = intcode[ptr_a]
    value_b = intcode[ptr_b]
    output_location = intcode[instruction_ptr + 3]

    if operator == "add":
        intcode[output_location] = value_a + value_b
    elif operator == "mult":
        intcode[output_location] = value_a * value_b
    else: # place for future ops, day3 :pepelaugh:
        pass


def brute_force(instruction_sequence):
    for i in range(0, len(instruction_sequence)):
        for j in range(0, len(instruction_sequence)):
            # create a copy of input list so it is a fresh start each loop
            temporary = instruction_sequence.copy()
            temporary[1] = i
            temporary[2] = j
            # parse instruction set with i and j as 1st and 2nd elements
            elfish_computer(temporary)
            if temporary[0] == 19690720:
                print(temporary)
                break


code = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,1,6,23,27,1,27,5,31,2,31,10,35,2,35,6,39,1,39,5,43,2,43,9,47,1,47,6,51,1,13,51,55,2,9,55,59,1,59,13,63,1,6,63,67,2,67,10,71,1,9,71,75,2,75,6,79,1,79,5,83,1,83,5,87,2,9,87,91,2,9,91,95,1,95,10,99,1,9,99,103,2,103,6,107,2,9,107,111,1,111,5,115,2,6,115,119,1,5,119,123,1,123,2,127,1,127,9,0,99,2,0,14,0]
brute_force(code)

