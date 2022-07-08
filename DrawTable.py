from datetime import date
from Data import Info


# Given the records, title, field names and their widths,
# Show the data in a tabular format on console
def showCustomTable(records, title, fieldinfo):

    records = processDates(records)
    fields, widths = fieldsAndWidths(fieldinfo)
    fullWidth = sum(widths) + (len(widths)-1)*3 + 2
    fstring = createFormat(widths)

    print()
    print('=' * fullWidth)
    print(("{0:^%s}" % str(fullWidth)).format(title.upper()))
    print('=' * fullWidth)
    print(fstring.format(*fields))
    print('-' * fullWidth)

    for rec in records:
        print(fstring.format(*rec))
    print('=' * fullWidth)
    print()


# Change the format of dates in records
def processDates(records):
    Output = []
    for rec in records:
        rec2 = []
        for col in rec:
            elem = col
            if type(col) == date:
                elem = col.strftime('%d.%m.%Y')
            rec2.append(elem)
        Output.append(rec2)
    return Output


# Extract fields names and widths
def fieldsAndWidths(fieldinfo):
    fields = []
    widths = []
    for field in fieldinfo:
        if type(field) == str:
            fields.append(field)
            w = Info.fieldWidth[field]
            widths.append(w)
        elif type(field) == tuple or type(field) == list:
            fields.append(field[0])
            widths.append(field[1])
        else:
            print("!!! Invalid type in fieldinfo !!!")
            break
    return fields, widths


# Create the format string
def createFormat(widths):
    strng = " {%d:^%d} " % (0, widths[0])
    cols = [strng]
    for i in range(1, len(widths)):
        w = widths[i]
        strng = "| {%d:^%d} " % (i, w)
        cols.append(strng)
    fstring = ''.join(cols)
    return fstring
