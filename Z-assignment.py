"""
Part 2. (This part is new)
Part A: Create a function that will accept 2 parameters: 
* id: integer key value for the table entry to be changed.
* data: a dictionary of values to be updated.


Note that you will need to also have a function to allow you to find the id of the entry you want changed
Part B:Create a function that will allow you to search for a current user based on a certain criteria.  The search should display the data for all of the matches so you can select the correct ID for the entry you want to update

Part C: Create a function that will display the values for the entry that has been selected, and allow the user to choose a value to edit.  Once they are finished, they can send the data to Part A to update the values.  A menu system would be useful here.
"""


import sqlite3

file = 'dbase.db'
connection = sqlite3.connect(file)
print(connection)

cursor = connection.cursor()
cursor.execute("drop table if exists customers")
cursor.execute("drop table if exists pets")
cursor.execute("drop table if exists visits")

cursor = connection.cursor()
query = """
create table if not exists customers (
    id integer primary key autoincrement,
    fname text,
    lname text,
    phoneNum text,
    email text,
    address text, 
    city text,
    postalcode text
);
"""
cursor.execute(query)
"""---------------------------------"""
cursor = connection.cursor()
query = """
create table if not exists pets (
    id integer primary key autoincrement,
    pname text,
    type text,
    breed text,
    birthdate text,
    ownerID int,
    foreign key (ownerID) references customers(id)
    );
    """
cursor.execute(query)
"""-------------------------------"""
cursor = connection.cursor()
query = """
create table if not exists visits (
    id integer primary key autoincrement,
    ownerid int,
    petid int,
    details text,
    cost int,
    paid int,
    foreign key (ownerid) references customers(id),
    foreign key (petid) references pets(id)
);
"""
cursor.execute(query)

print("Tables created")

"""-----------------------------"""
print("add a customer")
id = input("ID: ")
fname = input("first name: ")
lname = input("last name: ")
phone = input("phone number: ")
email = input("email: ")
address = input("address: ")
city = input("city: ")
postal = input("postal code: ")

data = (id, fname, lname,phone,email,address,city,postal)


query = f"""
insert into customers (fname, lname, phoneNum, email, address, city, postalcode) 
values ('{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}', '{data[5]}', '{data[6]}')
"""

cursor.execute(query)
for i in data:
    print(i)
connection.commit()

def searches():
    g = input("Do you want to search the database? (yes or no): ")
    
    if g.lower() == "yes":
        
        table = input("Do you want to search customers, pets, or visits? Type: 'customers', 'pets', or 'visits': ")
        
        if table == "customers":
            field = input("Search by: fname, lname, email, phoneNum, address, city, or postal code?: ")
            value = input(f"Enter the {field}: ")
            if field == "fname":
                cursor.execute(f"select * from customers where fname = '{value}'")
            elif field == "lname": 
                cursor.execute(f"select * from customers where lname = '{value}'")
            elif field == "email": 
                cursor.execute(f"select * from customers where email = '{value}'")
            elif field == "phoneNum": 
                cursor.execute(f"select * from customers where phoneNum = '{value}'")
            elif field == "address": 
                cursor.execute(f"select * from customers where address = '{value}'")
            elif field == "city": 
                cursor.execute(f"select * from customers where city = '{value}'")
            elif field == "postal code": 
                cursor.execute(f"select * from customers where postal code = '{value}'")
            else:
                print("Invalid field for customers.")
                return

        elif table == "pets":
            field = input("Search by: pname, breed, ownerID, birthdate, or type: ")
            value = input(f"Enter the {field}: ")
            if field == "pname":
                cursor.execute(f"select * from pets where pname = '{value}'")
            elif field == "breed": 
                cursor.execute(f"select * from pets where breed = '{value}'")
            elif field == "ownerID": 
                cursor.execute(f"select * from pets where ownerID = '{value}'")
            elif field == "birthdate": 
                cursor.execute(f"select * from pets where birthdate = '{value}'")
            elif field == "type": 
                cursor.execute(f"select * from pets where type = '{value}'")
            else:
                print("Invalid field for pets.")
                return

        elif table == "visits":
            field = input("Search by: details, cost, amount paid, ownerID, or petID: ")
            value = input(f"Enter the {field}: ")
            if field == "details":
                cursor.execute(f"select * from visits where details like '%{value}%'")
            elif field == "cost": 
                cursor.execute(f"select * from visits where cost = {value}")
            elif field == "paid": 
                cursor.execute(f"select * from visits where paid = {value}")
            elif field == "ownerID": 
                cursor.execute(f"select * from visits where ownerID = {value}")
            elif field == "petID": 
                cursor.execute(f"select * from visits where petID = {value}")
            else:
                print("Invalid field for visits.")
                return

        else:
            print("choose customers, pets, or visits. It's not that hard")
            return
        
        results = cursor.fetchall()
        if results:
            for row in results:
                print(row)
        else:
            print("No results found.")
    
    elif g.lower() == "no":
        connection.close()
        exit()
    
    else:
        print("type only yes or no")
    return

searches()


def update(id, field, new_value):
    g = input("Do you want to edit a value? (yes or no): ")
    if g.lower == "yes":
        
        query = f"update customers set {field} = ? where id = ?"
        cursor.execute(query, (new_value, id))
        connection.commit()
        print(f"{field} for id {id} has been updated to {new_value}.")
    else:
        return


def searchupdate():
    
    field = input("Search by: fname, lname, email, phoneNum, address, city, or postal code: ")
    value = input(f"Enter the {field}: ") 
    query = f"select * from customers where {field} = ?"
    cursor.execute(query, (value,))
    results = cursor.fetchall()
    if results:
        print("Search results:")
        for row in results:
            print(row)
        goon = int(input("Enter the ID of the entry you want to update: "))
        return goon
    else:
        print("No results found.")
        return None


def edit(id):
    cursor.execute(f"select * from customers where id = ?", (id,))
    entry = cursor.fetchone()

    if entry:
        print(f"\nCurrent data for ID {id}:")
        print(f"ID: {entry[0]}, Name: {entry[1]} {entry[2]}, Phone: {entry[3]}, Email: {entry[4]}, Address: {entry[5]}, City: {entry[6]}, Postal: {entry[7]}")

        data = {}
        sandwich = "yes"
        
        while sandwich.lower() == "yes":
            tralalero = input("Enter the field you want to edit (fname, lname, phoneNum, email, address, city, postalcode): ")
            new_value = input(f"Enter the new value for {tralalero}: ")
            data[tralalero] = new_value

            sandwich = input("Do you want to edit another field? (yes/no): ")

        for field, new_value in data.items():
            update(id, field, new_value)

    else:
        print(f"No customer found with ID {id}.")

tungtungtungsahur = searchupdate()
if tungtungtungsahur:
    edit(tungtungtungsahur)

connection.close()