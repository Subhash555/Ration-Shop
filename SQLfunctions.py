from datetime import date

from SQLqueries import *
from DrawTable import showCustomTable
from Data import Info


# Find customer ID from name
def FindCustID(name):
    result = CustomerDetails(name)
    ids = [i[0] for i in result]
    rows = len(result)
    if rows == 1:
        return ids[0]
    elif rows > 1:
        print(f"Database contains {rows} customers with name: {name}, please confirm- ")
        showCustomTable(result, 'Confirm Customer', ('CustID', 'Name', 'Category', 'Phone'))
        custId = input("Enter CustID of correct customer from above: ")
        while custId not in ids:
            custId = input("Enter CustID FROM THE ABOVE given: ")
        return custId
    else:
        return -1


# Show a formatted table on console
def showTable(table):
    if table not in Info.tables:
        print(f"Unknown table: {table} ")
        return
    cursor.execute(f"select * from {table} ")
    records = cursor.fetchall()
    title = table
    fieldInfo = Info.fields[table]
    showCustomTable(records, title, fieldInfo)


# Show all the tables
def showAll():
    for t in Info.tables:
        showTable(t)


# Check whether the products specified in order are offered at store
# If offered, find their product IDs
def ValidateProdName(order):
    products = listProducts()
    validName = True
    for i in range(len(order)):
        prodName = order[i][0].lower()
        if prodName not in products:
            if validName:
                print(f"{prodName}", end='')
                validName = False
            else:
                print(f", {prodName}", end='')
        else:
            prodId = selectQueryOne('prodid', 'products', 'prodname', prodName)
            order[i][0] = prodId
    if not validName:
        print(": not offered here.")
    return validName, order


# Check whether the order is as per the limit of that BPL customer
# Show in tabular form
def checkOrderLimit(custid, order):
    category = selectQueryOne('category', 'customers', 'custid', custid)
    members = selectQueryOne('members', 'carddetails', 'custid', custid)
    table = []
    inLimit = True
    for item in order:
        prodId = item[0]
        quantity = item[1]
        prodname = selectQueryOne('prodname', 'products', 'prodid', prodId)
        limit = find_limit(prodId, category) * members
        row = [prodname, quantity]
        if quantity <= limit:
            row.append(f"(\u2264 {limit}) \u2705")
        else:
            row.append(f"(\u2264 {limit}) \u2716")
            inLimit = False
        table.append(row)
    showCustomTable(table, 'Order Limit Check', ('ProdName', 'Quantity', ('Under limit', 11)))
    return inLimit


# Check whether the ordered items are available enough
# Show in tabular form
def checkOrderStock(order):
    table = []
    inStock = True
    for item in order:
        prodId = item[0]
        quantity = item[1]
        prodname = selectQueryOne('prodname', 'products', 'prodid', prodId)
        stock = selectQueryOne('stock', 'products', 'prodid', prodId)
        row = [prodname, quantity]
        if quantity <= stock:
            row.append(f"(\u2264 {stock}) \u2705")
        elif stock == 0:
            row.append("--OOS--")   # Out Of Stock
            inStock = False
        else:
            row.append(f"(\u2264 {stock}) \u2716")
            inStock = False
        table.append(row)
    showCustomTable(table, 'Order Stock Check', ('ProdName', 'Quantity', ('Available', 13)))
    return inStock


# Process order- Record the ordered items, quantity, person, date
def RecordOrder(custid, order):
    # orders & orderdetails
    today = date.today()
    ordId = InsertOrders(custid, today)
    records = [[ordId, *item] for item in order]
    InsertOrderDetails(records)


# Process order- Update the stock after the removal of items
def UpdateStock(order):
    # products & units
    for item in order:
        prodId = item[0]
        prodName = selectQueryOne('prodname', 'products', 'prodid', prodId)
        quantity = item[1]
        UpdateProducts(prodId, quantity)
        remaining = quantity
        while remaining:
            batchNo = FindUnit(prodId)
            remaining = UpdateUnits(batchNo, remaining, prodName)


def ShowBill(custid, order):
    category = selectQueryOne('category', 'customers', 'custid', custid)
    BPL = False
    if category in Info.BPLs:
        BPL = True
    table = []
    total = 0
    for item in order:
        prodId = item[0]
        prodName = selectQueryOne('prodname', 'products', 'prodid', prodId)
        quantity = item[1]
        mrp = selectQueryOne('mrp', 'products', 'prodid', prodId)
        if BPL:
            discount = find_discount(prodId, category)
        else:
            discount = 0
        rate = mrp * (1-discount/100)
        amount = round(rate * quantity, 2)
        total += amount
        if BPL:
            table.append([prodName, mrp, quantity, discount, amount])
        else:
            table.append([prodName, mrp, quantity, amount])
    if BPL:
        fieldInfo = ('ProdName', 'MRP', 'Quantity', 'Discount', ('Amount', 7))
    else:
        fieldInfo = ('ProdName', 'MRP', 'Quantity', ('Amount', 7))
    showCustomTable(table, 'Order Bill', fieldInfo)
    return total
