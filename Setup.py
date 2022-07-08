# Run sql statements from CreateDB.sql to create database
def CreateDB():
    with open("CreateDB.sql", 'r') as reader:
        statements = reader.read()
        iterator = cursor.execute(statements, multi=True)
        for _rubbish in iterator:
            pass


# Run sql statements from SampleDB.sql to fill in sample data
def SampleDB():
    with open("SampleDB.sql", 'r') as reader:
        statements = reader.read()
        iterator = cursor.execute(statements, multi=True)
        for _rubbish in iterator:
            pass
        conn.commit()


# Load the MySQL root password from Password.txt
def LoadPassword():
    with open("Password.txt", 'r') as reader:
        pswrd = reader.read()
    return pswrd


# Try importing connector module
try:
    import mysql.connector
except ImportError as e:
    print("!! Please download mysql.connector module for this program to work !!")
    print("Error:", e)
    exit()

else:

    secret = LoadPassword()
    try:
        # Connect to MySQL
        print("Connecting to MySQL: ", end='')
        conn = mysql.connector.connect(host="localhost", user="root", password=secret)
        cursor = conn.cursor(buffered=True)
        print("Done")

    except mysql.connector.Error as e:
        # Authentication error- access denied
        if e.errno == 1045:
            if secret == 'S@mpleP@ssword':
                print("\n!! Please update Password.txt file with your MySQL root password !!")
            else:
                print("\n!! Possibly wrong password !!")
                print("Error:", e.msg)
        # Unexpected error
        else:
            print("Unexpected error:", e.msg)
        exit()

    # Connected Successfully to MySQL
    # Create database and fill in sample data if doesn't exist already
    else:
        print("Finding database: ", end='')
        cursor.execute("show schemas")
        for sch in cursor:
            if sch[0] == "ration_store_group31":
                cursor.execute("use ration_store_group31")
                print("Done /- \n")
                break
        else:
            print("Not found")

            print("Creating database: ", end='')
            CreateDB()
            print("Done")
            print("Inserting sample data: ", end='')
            SampleDB()
            print("Done /- \n")
