# Inputted order must match the said format and turn it into form of records
def ValidateFormat(orderstr):
    list1 = list(map(str.strip, orderstr.split(',')))
    list2 = [list(map(str.strip, i.split(' '))) for i in list1]
    try:
        list3 = [list((i[0], float(i[1]))) for i in list2]
        for item in list3:
            quantity = item[1]
            if quantity <= 0:
                print("Quantity should be a POSITIVE number. \n")
                return -1
        return list3
    except IndexError:
        print("Wrong FORMAT. Correct example- Wheat 10, Rice 20 \n")
    except ValueError:
        print("Quantity should to be NUMERIC. \n")
    return -1


# Validate option inputted
def validOption(lower, upper):
    opt = input("Option No. : ")
    valid = False
    values = range(lower, upper + 1)
    while not valid:
        if not opt.isdigit():
            opt = input("Option NUMBER : ")
        elif int(opt) not in values:
            opt = input("VALID Option No. : ")
        else:
            valid = True
    return opt
