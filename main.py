def print_as_tree(xs, ind=0):
    for i in xs:
        if type(i) != list:
            print(" "*ind, i)
        else:
            print_as_tree(i, ind+2)


#////////////#


def give_spaces_and_split(program):

    # first we give spaces to the brackets, because we want to split them by space
    program = program.replace(")", " ) ").replace("(", " ( ")
    # for the strings, we replace the spaces with underscores (_) not to be confused when spaces when splitting
    is_string = False
    for i in range(len(program)):
        # assuming we are using "" quotes for strings
        if program[i] == '"':
            is_string = not is_string
        elif program[i] == " ":
            if is_string:
                program = list(program)
                program[i] = "_"
                program = "".join(program)

    if is_string:
        raise SyntaxError('String did not end, expected "')
    program = program.split()

    # replace the underscores with spaces again
    for i in range(len(program)):
        program[i] = program[i].replace("_", " ")

    return program


def is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def is_float(s):
    try:
        float(s)
        return True
    except:
        return False


def is_string(s):
    return s[0] == '"' and s[-1] == '"'


def is_variable(s):
    return is_float(s) or is_int(s) or is_string(s)


def check_types(subTree):
    return not is_variable(subTree[0])


def treefy(tokens, i=0):
    while i < len(tokens):
        if tokens[i] == "(":
            i += 1
            command_tokens = []
            if i > len(tokens):
                raise SyntaxError('unexpected EOF')
            while tokens[i] != ")":
                subTree, i = treefy(tokens, i)
                while True:
                    if type(subTree) == list and len(subTree) == 1:
                        subTree = subTree[0]
                    else:
                        break

                # check if the first token of the command is a function, in case there is more than 1 token
                if type(subTree) == list:
                    type_check_result = check_types(subTree)

                    if not type_check_result:
                        print(subTree)
                        raise SyntaxError('Wrong types at token '+str(i))

                command_tokens.append(subTree)
            return command_tokens, i+1

        elif tokens[i] == ")":
            raise SyntaxError('unexpected  ) at char '+str(i))

        else:
            return tokens[i], i+1


def read_program(program):
    # this turns the program string into a list, by spalcing the brackets and then spliting by space,
    program_tokens = give_spaces_and_split(program)

    # this part makes a command like " add 1 2  " into " ( add 1 2 )", to be valid
    if program_tokens[0] != "(":
        program_tokens = ["("] + program_tokens + [")"]

    result, lastIndex = treefy(program_tokens)

    if lastIndex != len(program_tokens):
        raise SyntaxError(
            'there is an error, probably an extra command or variable or bracket at the right hand side')

    return result


if __name__ == "__main__":

    program = ' first ( list (1) (+ 2 "ad ada") 9  '
    program = "(first (list 1 (+ 2 3) 9))"
    tree = read_program(program)
    print(tree)
    print_as_tree(tree)
