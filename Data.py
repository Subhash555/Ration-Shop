class Info:

    tables = ('products', 'customers', 'subsidy', 'carddetails', 'units', 'orders', 'orderdetails')

    BPLs = ("BPL-1", "BPL-2")

    # tableFields
    fields = {
        'products': ('ProdID', 'ProdName', 'MRP', 'Stock'),
        'customers': ('CustID', 'Name', 'Category', 'Phone'),
        'subsidy': ('ProdID', 'Category', 'Discount', 'Maximum'),
        'carddetails': ('CustID', 'CardNo', 'Members', 'Claimed'),
        'units': ('BatchNo', 'ProdID', 'DOM', 'Expiry', 'Size'),
        'orders': ('OrdID', 'CustID', 'Date'),
        'orderdetails': ('OrdID', 'ProdID', 'Quantity')
    }

    fieldWidth = {
        'ProdID': 6, 'ProdName': 15, 'MRP': 6, 'Stock': 7,
        'CustID': 6, 'Name': 15, 'Category': 8, 'Phone': 10,
        'Discount': 8, 'Maximum': 7,
        'CardNo': 6, 'Members': 7, 'Claimed': 7,
        'BatchNo': 7,  'DOM': 10, 'Expiry': 10, 'Size': 7,
        'OrdID': 6, 'Date': 10,
        'Quantity': 8
    }

    # to be removed
    # formats = {
    #     'products': (" {0:^6} | {1:^15} | {2:^6} | {3:^5} ", 43),
    #     'customers': (" {0:^6} | {1:^15} | {2:^8} | {3:^10} ", 50),
    #     'subsidy': (" {0:^6} | {1:^8} | {2:^8} | {3:^7} ", 40),
    #     'carddetails': (" {0:^6} | {1:^6} | {2:^7} | {3:^7} ", 37),
    #     'units': (" {0:^7} | {1:^6} | {2:^10} | {3:^10} | {4:^5} ", 52),
    #     'orders': (" {0:^6} | {1:^6} | {2:^10} ", 30),
    #     'orderdetails': (" {0:^6} | {1:^6} | {2:^8} ", 28)
    # }
