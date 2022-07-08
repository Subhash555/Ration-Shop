from Setup import *


# Function to run classic select query
def selectQueryOne(field, table, against, value):
    sql = f"select {field} from {table} where {against} = '{value}'"
    cursor.execute(sql)
    (result,) = cursor.fetchone()
    return result


# Find the limit on a particular product for a particular BPL category
def find_limit(prodid, category):
    sql = f"select maximum from subsidy " \
          f"where prodid = '{prodid}' and category = '{category}'"
    cursor.execute(sql)
    (limit,) = cursor.fetchone()
    return limit


# Find the discount on a particular product for a particular BPL category
def find_discount(prodid, category):
    sql = f"select discount from subsidy " \
          f"where prodid = '{prodid}' and category = '{category}'"
    cursor.execute(sql)
    (discount,) = cursor.fetchone()
    return discount


# Get all fields of customers
def CustomerDetails(name):
    sql = "select * from customers where name = (%s)"
    val = (name,)
    cursor.execute(sql, val)
    result = cursor.fetchall()
    return result


# Customers currently in the (sample) database
def CurrentCustomers():
    cursor.execute("select name from customers")
    result = cursor.fetchall()
    return result


# List the offered products
def listProducts():
    sql = "select prodname from products"
    cursor.execute(sql)
    prods = cursor.fetchall()
    prods = [i[0].lower() for i in prods]
    return prods


# Insert into orders
def InsertOrders(custid, today):
    sql = "insert into orders (custid, date) values (%s, %s)"
    val = (custid, today)
    cursor.execute(sql, val)
    conn.commit()
    return cursor.lastrowid


# Insert into orderdetails
def InsertOrderDetails(records):
    sql = "insert into orderdetails values (%s, %s, %s)"
    cursor.executemany(sql, records)
    conn.commit()


# Update stock of products
def UpdateProducts(prodId, quantity):
    sql = "update products set stock = stock - (%s) where prodid = (%s)"
    cursor.execute(sql, (quantity, prodId))
    conn.commit()


# Find the oldest unit of a product
def FindUnit(prodId):
    cursor.execute("create or replace view useful as "
                   f"select * from units where prodid = {prodId}")
    cursor.execute("create or replace view old as "
                   "select * from useful where expiry = "
                   "(select min(expiry) from useful)")
    cursor.execute("select batchno from old "
                   "where size = (select min(size) from old)")
    (batchNo,) = cursor.fetchone()
    cursor.fetchall()
    return batchNo


# Update the stock of the particular unit
def UpdateUnits(batchNo, remaining, prodname):
    cursor.execute(f"select size from units where batchno = '{batchNo}'")
    (size,) = cursor.fetchone()
    if size <= remaining:
        remaining -= size
        cursor.execute(f"delete from units where batchno = '{batchNo}'")
        conn.commit()
        print(f"A unit of {prodname} just emptied.")
        return remaining
    cursor.execute(f"update units set size = size - {remaining} where batchno = '{batchNo}'")
    conn.commit()
    return 0


# Update the Claim status of a BPL
def UpdateClaim(custid):
    sql = "update carddetails set claimed = 1 where custid = (%s)"
    cursor.execute(sql, (custid,))
    conn.commit()


# Restore to Sample Database
def RestoreSampleDB():
    cursor.execute("drop schema ration_store_group31")
    conn.commit()
    CreateDB()
    SampleDB()
