# This function gets a name of a file that contains samples of x,y,dx,dy and returns (in a list):
# 1) Whether the file is valid or not
# 2) If the information is written in rows or in columns
# 3) The data in a list format
def valid_file_and_organization_checker(filename):
    is_file_valid = True
    file_operator = open(filename, 'r')
    data = file_operator.readlines()
    for row_index in range(0, 4):
        data[row_index] = data[row_index].lower()
    for row_index in range(len(data)):
        data[row_index] = data[row_index].strip().split()
    # At this point I have the variable data that is a nested list
    for row_index in range(
            len(data)):  # in case that there are extra spaces between the different values this will remove them
        for column_index in range(len(data[row_index])):
            data[row_index][column_index] = data[row_index][column_index].strip()

    if ("x" in data[0]) and ("y" in data[0]) and ("dx" in data[0]) and (
            "dy" in data[0]):  # if True it means the data is in columns
        file_organization = "columns"
        # Finding the index where the table ends:
        for i in range(len(data)):
            if data[i] == []:
                end_index = i
                break

        # Checking if there is the same number of values for x,y,dx,dy:
        for row_index in range(1, end_index):
            if len(data[row_index]) != 4:
                is_file_valid = False
                print("Input file error: Data lists are not the same length")
                break

        # Checking if the values are numbers:
        if is_file_valid:
            for row_index in range(1, end_index):
                for column_index in range(len(data[row_index])):
                    try:
                        data[row_index][column_index] = float(data[row_index][column_index])
                    except:
                        is_file_valid = False
                        break
        if not is_file_valid:
            print("Input file error: Not all the values are numbers")

        # checking if dy and dx are bigger than 0:
        if is_file_valid:
            for column_index in range(len(data[0])):
                if data[0][column_index] == 'dy':
                    dy_col_index = column_index
                elif data[0][column_index] == 'dx':
                    dx_col_index = column_index
            for row_index in range(1, end_index):
                if (float(data[row_index][dx_col_index]) <= 0) or (float(data[row_index][dy_col_index]) <= 0):
                    is_file_valid = False
                    print("Input file error: Not all uncertainties are positive.")
                    break

    elif (("x" in data[0]) or ("y" in data[0]) or ("dx" in data[0]) or ("dy" in data[0])) and (
            ("x" in data[1]) or ("y" in data[1]) or ("dx" in data[1]) or ("dy" in data[1])) and (
            ("x" in data[2]) or ("y" in data[2]) or ("dx" in data[2]) or ("dy" in data[2])) and (
            ("x" in data[3]) or ("y" in data[3]) or ("dx" in data[3]) or ("dy" in data[3])):
        # if True it means that the data is in rows
        file_organization = "rows"
        # checking if there is the same number of values for x,y,dx,dy:
        for row_index in range(1, 4):
            if len(data[row_index]) != len(data[0]):
                is_file_valid = False
                print("Input file error: Data lists are not the same length")
                break

        # checking if all the values are numbers:
        if is_file_valid:
            for row_index in range(4):
                for column_index in range(1, len(data[row_index])):
                    try:
                        data[row_index][column_index] = float(data[row_index][column_index])
                    except:
                        is_file_valid = False
                        break
        if not is_file_valid:
            print("Input file error: Not all the values are numbers")

        # checking if dy and dx are bigger than 0:
        if is_file_valid:
            for row_index in range(4):
                if ('dx' in data[row_index]) or ('dy' in data[row_index]):
                    for column_index in range(1, len(data[row_index])):
                        if float(data[row_index][column_index]) <= 0:
                            is_file_valid = False
                            print("Input file error: Not all uncertainties are positive.")
                            break

    return [is_file_valid, file_organization, data]
    file_operator.close()


# This function gets a list of measurements and a list of dy values and calculates the average.
# The lists should contain only numbers and they should have the same length.
def average_calculator(list_of_measurements, dy_list):
    sum_of_denominator = 0
    sum_of_numerator = 0
    for i in range(len(dy_list)):
        sum_of_denominator = sum_of_denominator + 1 / ((dy_list[i]) ** 2)
        sum_of_numerator = sum_of_numerator + list_of_measurements[i] / ((dy_list[i]) ** 2)
    average = sum_of_numerator / sum_of_denominator
    return average


def search_best_parameter(filename):
    # Input file handling: In this part of the function, the function gets a name of a file and extracts the data out
    # of it. The function needs to get X,dx,Y,dy values (doesn't matter if it's in a row or a column / small or
    # capital letters / order of the arguments) and also needs to get what x and y represent. If there is a problem
    # in the data it will raise an error.
    validity_organization_data = valid_file_and_organization_checker(filename)
    if validity_organization_data[0]:
        # In this part the function extracts the data to a dictionary in which the keys are x, y, dx, dy and the
        # values are the measurements.
        data_dict = {}
        if validity_organization_data[1] == "rows":
            for row_num in range(0, 4):
                data_dict[validity_organization_data[2][row_num][0]] = validity_organization_data[2][row_num][
                                                                       1:len(validity_organization_data[2][row_num])]
        else:
            # Finding the index where the table ends:
            for i in range(len(validity_organization_data[2])):
                if validity_organization_data[2][i] == []:
                    end_index = i
                    break
            for column_index in range(len(validity_organization_data[2][0])):
                data_dict[validity_organization_data[2][0][column_index]] = []
                for row_index in range(1, end_index):
                    data_dict[validity_organization_data[2][0][column_index]].append(
                        validity_organization_data[2][row_index][column_index])

        # This turns all the numbers that appear in the last two lines (a,b) into floats:
        for i in range(len(validity_organization_data[2][-1])):
            try:
                validity_organization_data[2][-1][i] = float(validity_organization_data[2][-1][i])
            except:
                continue
        for i in range(len(validity_organization_data[2][-2])):
            try:
                validity_organization_data[2][-2][i] = float(validity_organization_data[2][-2][i])
            except:
                continue

        # At this part of the function, the function creates lists of all the possible a and b values.
        a_initial = validity_organization_data[2][-2][1]
        a_final = validity_organization_data[2][-2][2]
        a_step = validity_organization_data[2][-2][3]
        b_initial = validity_organization_data[2][-1][1]
        b_final = validity_organization_data[2][-1][2]
        b_step = validity_organization_data[2][-1][3]
        optional_a_list = [a_initial]
        optional_b_list = [b_initial]
        if a_initial < a_final:
            while optional_a_list[-1] < a_final:
                optional_a_list.append(optional_a_list[-1] + a_step)
        else:
            while optional_a_list[-1] > a_final:
                optional_a_list.append(optional_a_list[-1] + a_step)
        if b_initial < b_final:
            while optional_b_list[-1] < b_final:
                optional_b_list.append(optional_b_list[-1] + b_step)
        else:
            while optional_b_list[-1] > b_final:
                optional_b_list.append(optional_b_list[-1] + b_step)
        optional_a_list = optional_a_list[0:-1]
        optional_b_list = optional_b_list[0:-1]
        # Fitting function and definitions: In this part of the function, the function finds the best a and b for
        # minimized chi2 and calculates the value of chi2_reduced.
        # At the end of all the calculations the function prints the results.
        N = len(data_dict['x'])  # N = number of measurements
        optional_chi2_list = []  # This list will contain the temporary minimized chi2 for each combination of a and b.
        for a in optional_a_list:
            for b in optional_b_list:
                chi2 = 0
                for i in range(N):
                    chi2 = chi2 + ((data_dict['y'][i] - a * data_dict['x'][i] - b) / (data_dict['dy'][i])) ** 2
                optional_chi2_list.append([chi2, a, b])
        optional_chi2_list.sort()
        minimized_chi2 = optional_chi2_list[0][0]
        best_a = optional_chi2_list[0][1]
        best_b = optional_chi2_list[0][2]
        chi2_reduced = minimized_chi2 / (N - 2)
        output = "a = {} +- {}\nb = {} +- {}\nchi2 = {}\nchi2_reduced = {}".format(best_a, a_step, best_b, b_step,
                                                                                   minimized_chi2, chi2_reduced)
        print(output)

        # Plotting part:
        from matplotlib import pyplot
        # Linear plot:
        fitted_y_arguments = []
        for i in range(N):
            fitted_y_arguments.append(best_a * data_dict['x'][i] + best_b)
        # Creating a strings with the label of x and y:
        for i in range(
                len(validity_organization_data[2])):  # Finding the index of the row where the axises are written:
            if len(validity_organization_data[2][i]) >= 2:
                if validity_organization_data[2][i][1] == 'axis:':
                    if validity_organization_data[2][i][0] == 'x':
                        x_label_index = i
                    else:
                        y_label_index = i
        y_label = ""
        for i in range(2, len(validity_organization_data[2][y_label_index])):
            y_label = y_label + validity_organization_data[2][y_label_index][i] + " "
        y_label.strip()
        x_label = ""
        for i in range(2, len(validity_organization_data[2][x_label_index])):
            x_label = x_label + validity_organization_data[2][x_label_index][i] + " "
        x_label.strip()
        # Plotting:
        pyplot.plot(data_dict['x'], fitted_y_arguments, 'r-')  # plotting y=ax+b in red line
        pyplot.errorbar(data_dict['x'], data_dict['y'], yerr=data_dict['dy'], xerr=data_dict['dx'],
                        fmt='b,')  # plotting x,y dots as error bars in blue dots
        pyplot.ylabel(y_label)
        pyplot.xlabel(x_label)
        pyplot.savefig("linear_fit.svg", format="svg")  # saving the plot as svg file under the name "linear_fit.svg".
        pyplot.show()  # presenting the output
        # Chi2 as function of a plot:
        new_optional_chi2_list = []
        for a in optional_a_list:
            chi2 = 0
            for i in range(N):
                chi2 = chi2 + ((data_dict['y'][i] - a * data_dict['x'][i] - best_b) / (data_dict['dy'][i])) ** 2
            new_optional_chi2_list.append(chi2)
        # Plotting:
        y_label = "chi2(b = {})".format(best_b)
        pyplot.plot(optional_a_list, new_optional_chi2_list, 'b-')  # plotting chi2 as function of a in blue line
        pyplot.ylabel(y_label)
        pyplot.xlabel("a")
        pyplot.savefig("numeric_sampling.svg",
                       format="svg")  # saving the plot as svg file under the name "numeric_sampling.svg".
        pyplot.show()  # presenting the output


def fit_linear(filename):
    # Input file handling: In this part of the function, the function gets a name of a file and extracts the data out
    # of it. The function needs to get X,dx,Y,dy values (doesn't matter if it's in a row or a column / small or
    # capital letters / order of the arguments) and also needs to get what x and y represent. If there is a problem
    # in the data it will raise an error.
    validity_organization_data = valid_file_and_organization_checker(filename)
    if validity_organization_data[0]:
        # In this part the function extracts the data to a dictionary in which the keys are x, y, dx, dy and the
        # values are the measurements.
        data_dict = {}
        if validity_organization_data[1] == "rows":
            for row_num in range(0, 4):
                data_dict[validity_organization_data[2][row_num][0]] = validity_organization_data[2][row_num][
                                                                       1:len(validity_organization_data[2][row_num])]
        else:
            # Finding the index where the table ends:
            for i in range(len(validity_organization_data[2])):
                if validity_organization_data[2][i] == []:
                    end_index = i
                    break
            for column_index in range(len(validity_organization_data[2][0])):
                data_dict[validity_organization_data[2][0][column_index]] = []
                for row_index in range(1, end_index):
                    data_dict[validity_organization_data[2][0][column_index]].append(
                        validity_organization_data[2][row_index][column_index])

        # Fitting function and definitions: In this part of the function, the function calculates the value of chi2,
        # chi2_reduced, a, b, da and db.
        # At the end of all the calculations the function prints the results.
        N = len(data_dict['x'])  # N = number of measurements
        xy_list = data_dict['x'].copy()
        for i in range(len(xy_list)):
            xy_list[i] = xy_list[i] * data_dict['y'][i]
        x2_list = data_dict['x'].copy()
        for i in range(len(x2_list)):
            x2_list[i] = x2_list[i] ** 2
        dy2_list = data_dict['dy'].copy()
        for i in range(len(dy2_list)):
            dy2_list[i] = dy2_list[i] ** 2
        a = (average_calculator(xy_list, data_dict['dy']) - (
                average_calculator(data_dict['x'], data_dict['dy']) * average_calculator(data_dict['y'],
                                                                                         data_dict['dy']))) / (
                    average_calculator(x2_list, data_dict['dy']) - (
                average_calculator(data_dict['x'], data_dict['dy'])) ** 2)
        b = average_calculator(data_dict['y'], data_dict['dy']) - a * average_calculator(data_dict['x'],
                                                                                         data_dict['dy'])
        da = (average_calculator(dy2_list, data_dict['dy']) / (N * (average_calculator(x2_list, data_dict['dy']) - (
            average_calculator(data_dict['x'], data_dict['dy'])) ** 2))) ** 0.5
        db = ((average_calculator(dy2_list, data_dict['dy']) * average_calculator(x2_list, data_dict['dy'])) / (N * (
                average_calculator(x2_list, data_dict['dy']) - (
            average_calculator(data_dict['x'], data_dict['dy'])) ** 2))) ** 0.5
        chi2 = 0
        for i in range(N):
            chi2 = chi2 + ((data_dict['y'][i] - a * data_dict['x'][i] - b) / (data_dict['dy'][i])) ** 2
        chi2_reduced = chi2 / (N - 2)
        output = "a = {} +- {}\nb = {} +- {}\nchi2 = {}\nchi2_reduced = {}".format(a, da, b, db, chi2, chi2_reduced)
        print(output)

        # Plotting part:
        from matplotlib import pyplot
        fitted_y_arguments = []
        for i in range(N):
            fitted_y_arguments.append(a * data_dict['x'][i] + b)
        # Creating a strings with the label of x and y:
        for i in range(
                len(validity_organization_data[2])):  # Finding the index of the row where the axises are written:
            if len(validity_organization_data[2][i]) >= 2:
                if validity_organization_data[2][i][1] == 'axis:':
                    if validity_organization_data[2][i][0] == 'x':
                        x_label_index = i
                    else:
                        y_label_index = i
        y_label = ""
        for i in range(2, len(validity_organization_data[2][y_label_index])):
            y_label = y_label + validity_organization_data[2][y_label_index][i] + " "
        y_label.strip()
        x_label = ""
        for i in range(2, len(validity_organization_data[2][x_label_index])):
            x_label = x_label + validity_organization_data[2][x_label_index][i] + " "
        x_label.strip()
        # Plotting:
        pyplot.plot(data_dict['x'], fitted_y_arguments, 'r-')  # plotting y=ax+b in red line
        pyplot.errorbar(data_dict['x'], data_dict['y'], yerr=data_dict['dy'], xerr=data_dict['dx'],
                        fmt='b,')  # plotting x,y dots as error bars in blue dots
        pyplot.ylabel(y_label)
        pyplot.xlabel(x_label)
        pyplot.savefig("linear_fit.svg", format="svg")  # saving the plot as svg file under the name "linear_fit.svg".
        pyplot.show()  # presenting the output


# main program:

filename = input("Write the name of the file that contains the data:")
fit_linear(filename)
search_best_parameter(filename)