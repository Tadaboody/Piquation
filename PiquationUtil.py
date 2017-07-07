def solve_simple_equation(a1, b1, c1, a2, b2, c2):
    """
    solves the solution of the equation system: 
    a1x + b1y + c = 0
    a2x + b2x + c = 0
    :param a1: first coefficient for x
    :param b1: first coefficient for y
    :param c1: first free element
    :param a2: second coefficient for x 
    :param b2: second coefficient for y
    :param c2: second free element
    :return: 
    """
    a1, b1, c1, a2, b2, c2 = make_float([a1, b1, c1, a2, b2, c2])
    x = (-c1 + (b1*c2)/b2)/(a1 - (b1*a2)/b2)
    y = (-c2 - a2*x)/b2
    return x, y


def make_float(number_list):
    """
    turns all the numbers in number_list into floats
    :param number_list: list of numbers
    :return: list of floats
    """
    for index, number in enumerate(number_list[:]):
        number_list[index] = float(number)
    return number_list


def solve_equation(equation_string):
    """
    receives a string that represents an equation system and solves it
    for example:    2x+3y=1;y+3=x
    :param equation_string: a string that represents an equation system
    :return: tuple containing the solution
    """
    equation_data = arrange_system_equation_data(equation_string)

    eq1d = list(equation_data[0])
    eq2d = list(equation_data[1])
    eq2d.extend(eq1d)
    solution = solve_simple_equation(eq2d[0], eq2d[1], eq2d[2], eq2d[3], eq2d[4], eq2d[5])
    re_string = "x: " + str(solution[0]) + "\ny: " + str(solution[1])
    return re_string


def arrange_system_equation_data(equation_string):
    equation1, equation2 = equation_string.split(';')
    equation1_data = arrange_equation_data(equation1)
    equation2_data = arrange_equation_data(equation2)
    return equation1_data, equation2_data


def arrange_equation_data(equation):
    a, b, c = [0]*3
    left, right = equation.split('=')
    left_parts = left.split('+')
    for part in left_parts:
        if len(part) == 1:
            if part == 'x':
                a = 1
            elif part == 'y':
                b = 1
            else:
                c = int(part)
        elif len(part) == 2:
            if part[1] == 'x':
                a = int(part[0])
            elif part[1] == 'y':
                b = int(part[0])
            else:
                c = -int(part[1])
        else:
            neg_parts = part.split('-')
            for index, new_part in enumerate(neg_parts):
                if len(new_part) == 1:
                    if index == 0:
                        if new_part == 'x':
                            a = 1
                        elif new_part == 'y':
                            b = 1
                        else:
                            c = int(new_part)
                    else:
                        if new_part == 'x':
                            a = -1
                        elif new_part == 'y':
                            b = -1
                        else:
                            c = -int(new_part)
                else:
                    if index == 0:
                        if new_part[1] == 'x':
                            a = int(new_part[0])
                        else:
                            b = int(new_part[0])
                    else:
                        if new_part[1] == 'x':
                            a = -int(new_part[0])
                        else:
                            b = -int(new_part[0])
    # right
    right_parts = right.split('+')
    for part in right_parts:
        if len(part) == 1:
            if part == 'x':
                a = -1
            elif part == 'y':
                b = -1
            else:
                if c == 0:
                    c = int(part)
        elif len(part) == 2:
            if part[1] == 'x':
                a = -int(part[0])
            elif part[1] == 'y':
                b = -int(part[0])
            else:
                c = -int(part)
        else:
            neg_parts = part.split('-')
            for index, new_part in enumerate(neg_parts):
                if len(new_part) == 1:
                    if index == 0:
                        if new_part == 'x':
                            a = -1
                        elif new_part == 'y':
                            b = -1
                        else:
                            c = -int(new_part)
                    else:
                        if new_part == 'x':
                            a = 1
                        elif new_part == 'y':
                            b = 1
                        else:
                            c = int(new_part)
                elif len(new_part) != 0:
                    if index == 0:
                        if new_part[1] == 'x':
                            a = -int(new_part[0])
                        else:
                            b = -int(new_part[0])
                    else:
                        if new_part[1] == 'x':
                            a = int(new_part[0])
                        else:
                            b = int(new_part[0])
    return a, b, c

raw_data = raw_input("Insert Equation System Data: ")
print solve_equation(raw_data)

#print arrange_equation_data("-3=-2y+x")
#print solve_simple_equation(-1, 1, -3, -2, 1, -1)

