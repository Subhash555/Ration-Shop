# Ration Store Console Interface

from SQLfunctions import *
from Functions import *


# Check for returning customer
def newCustomer():
    newCust = input("New Customer (y/n) ? ").lower()
    validInput = False
    while not validInput:
        if newCust.startswith('y'):
            print("New customer routine to be implemented")
            exit()
        elif newCust.startswith('n'):
            validInput = True
        else:
            newCust = input("YES or NO ? ").lower()
    return False  # if old customer


# Find Customer ID
def FindCustomer():
    found = False
    while not found:
        name = input("Enter name (Card holder's if BPL): ")
        custId = FindCustID(name)
        if custId == -1:
            print("Could not find by that name")
        else:
            return custId


# Get Category of customer
def GetCategory(custId):
    category = selectQueryOne("category", 'customers', 'custid', custId)
    return category


# Check if the BPL customer already claimed
def ClaimCheck(custId):
    claimed = selectQueryOne("claimed", 'carddetails', 'custid', custId)
    print("Claimed:", claimed)
    if claimed:
        print("Sorry, your category type is BPL, who can claim only once")
        exit()
        # Allow to know when he/she claimed
        print()


# Show all the products offered
def ShowProducts():
    print("\nProducts offered: ", end='')
    products = listProducts()
    for prod in products:
        print(prod, end=' ')
    print()


# Receive order and validate
def GetOrder(custId, category):

    validOrder = False
    order = None
    while not validOrder:
        orderStr = input("\nEnter your order in the format- \n< prod1 quantity, prod2 quantity, ... > : \n")
        order = ValidateFormat(orderStr)
        if order == -1:
            print("Kindly re-enter your order.")
            continue

        # Check if the product names are valid
        validProd, order = ValidateProdName(order)
        if not validProd:
            print("Some products mentioned are NOT OFFERED here. \n"
                  "Kindly re-enter your order.")
            continue

        # Check whether the order crosses the limit of BPL customer
        if category in Info.BPLs:
            inLimit = checkOrderLimit(custId, order)
            if not inLimit:
                print("Some product's quantity in your order EXCEEDED your limit. \n "
                      "Kindly re-enter your order.")
                continue

        # Check whether the ordered items are available enough
        inStock = checkOrderStock(order)
        if not inStock:
            print("Some products are NOT AVAILABLE enough. \n"
                  "Kindly re-enter your order.")
            continue

        validOrder = True

    return order


def Restore():
    choice = input("Restore to Sample Database (y/n) ? ").lower()
    validInput = False
    while not validInput:
        if choice.startswith('y'):
            print("Restoring the Sample Database: ", end='')
            RestoreSampleDB()
            print("Done")
            return
        elif choice.startswith('n'):
            return
        else:
            choice = input("YES or NO ? ").lower()

# Execution flow starts continues from here after setup
def main():
    print("\nWelcome to Suprasidh Ration Store \n")

    Restore()
    # showAll()

    print("Customers in sample database: ", end='')
    for cust in CurrentCustomers():
        print(cust[0], end=' ')
    print()

    custId = newCustomer()
    if not custId:
        custId = FindCustomer()

    category = GetCategory(custId)
    print("Category:", category)

    if category in Info.BPLs:
        ClaimCheck(custId)

    ShowProducts()

    # Receive order
    order = GetOrder(custId, category)
    print("\nOrder validated, now processing ...")

    # Process order

    print("Recording the order: ", end='')
    RecordOrder(custId, order)
    print("Done")

    print("Updating the stock: ", end='')
    UpdateStock(order)
    print("Done")

    if category in Info.BPLs:
        UpdateClaim(custId)
        print("Updated customer's claim status")

    # Generate bill
    total = ShowBill(custId, order)
    print("Total amount: INR", total)
    print("Thank You, visit again !!")
    # showAll()


# Run
try:
    main()
except Exception:
    raise
finally:
    conn.close()
