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


def split_two(eq, c1, c2):
    """
    divides the elements in eq into 2 lists, splitting them around c1 and c2
    :param eq: arbitrary string
    :param c1: a character to split around
    :param c2: a character to split around
    :return: 2 lists, each containing all the elements that appear after c1 (list1) or c2 (list2)
    """
    list1, list2 = list(), list()
    split1 = eq.split(c1)
    for part in split1:
        temp = part.split(c2)
        if len(temp) == 1:
            list1.append(part)
        else:
            for index, new_part in enumerate(temp):
                if new_part == "":
                    continue
                elif index == 0:
                    list1.append(new_part)
                else:
                    list2.append(new_part)
    return list1, list2


def solve_equation(equation_string):
    """
    receives a string that represents an equation system and solves it
    for example:    2x+3y=1;y+3=x
    :param equation_string: a string that represents an equation system
    :return: string containing the solution
    """
    equation_data = arrange_system_equation_data(equation_string)  # arranges the data in 2 tuples - 1 for each eq

    eq1d = list(equation_data[0])  # first eq data
    eq2d = list(equation_data[1])  # second eq data
    eq2d = eq1d + eq2d  # concatenate both equations
    solution = solve_simple_equation(eq2d[0], eq2d[1], eq2d[2], eq2d[3], eq2d[4], eq2d[5])  # get x,y solution
    re_string = "x: " + str(solution[0]) + "\ny: " + str(solution[1])  # format output string
    return re_string


def arrange_system_equation_data(equation_string):
    """
    receives a string that represents an equation system and extracts the coefficients out of each equation
    for example:    2x+3y=1;y+3=x
    :param equation_string: a string that represents an equation system
    :return: tuple of all six coefficients in each side
    """
    equation1, equation2 = equation_string.split(';')  # split data string into 2 distinct equations
    equation1_data = arrange_equation_data(equation1)  # get the A, B, C for the first equation
    equation2_data = arrange_equation_data(equation2)  # get the A, B, C for the second equation
    return equation1_data, equation2_data  # return them one after the other


def raw_data_into_eq_data(data_list, mode, a, b, c):  # mode 1 => add, mode -1 => reduce
    """
    calculates coefficients from a list of all the elements in one half of a side
    :param data_list: all the elements in one of the equation sides after being broken down to parts
    :param mode: adding or reducing
    :param a: old coefficient
    :param b: old coefficient
    :param c: old c oefficient
    :return: new coefficients after taking care of a half of one side
    """
    for element in data_list:
        if element == 'x':  # "x"
            a += mode
        elif element == 'y':  # "y"
            b += mode
        elif element[-1] == 'x':  # "ax"
            a += mode*int(element[:-1])
        elif element[-1] == 'y':  # "by"
            b += mode*int(element[:-1])
        elif len(element) > 0:  # "c"
            c += mode*int(element)
    return a, b, c


def arrange_equation_data(equation):
    """
    takes an equation and moves all the elements into the left side of the equal sign and returns the new coefficients 
    :param equation: equation for example: 2x+3y=1
    :return: tuple of all three coefficients after moving them to the left side
    """
    a, b, c = [0]*3  # initialize A, B, C to 0
    left, right = equation.split('=')
    eq_data = list(split_two(left, '+', '-'))  # data for equation 1
    temp = list(split_two(right, '+', '-'))  # data for equation 2
    temp.reverse()
    eq_data += temp
    for index, data in enumerate(eq_data):
        a, b, c = raw_data_into_eq_data(data, even_or_odd(index), a, b, c)
    return a, b, c


def even_or_odd(number):
    """
    checks %2 of a number
    :param number: int to check if its even or odd
    :return: 1 if even, -1 if odd
    """
    if number % 2 == 0:
        return 1
    else:
        return -1
# correct way to test the math part of things:
# print solve_equation(raw_input("Insert Equation System Data: "))




