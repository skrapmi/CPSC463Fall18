# -*- coding: utf-8 -*-
#Basic Inventory and Customer program
from __future__ import print_function

import sqlite3
from datetime import datetime
#TEST123
connection = sqlite3.connect ("parts.db")
cursor = connection.cursor()

######### CREATE EMPLOYEES TABLE #############
sql_command = """
CREATE TABLE IF NOT EXISTS EMPLOYEES (
Employ_ID INT(10) NOT NULL,
First VARCHAR(20) NOT NULL,
Last VARCHAR(30) NOT NULL,
Title VARCHAR(30) NOT NULL,
Hire_date VARCHAR(10),
Manager BIT NOT NULL DEFAULT (0), 
PRIMARY KEY (Employ_ID));"""
cursor.execute (sql_command)

######## MANUAL ENTRY OF INVENTORY ITEMS #####
sql_command = """INSERT OR REPLACE INTO EMPLOYEES (Employ_ID, First, Last, Title, Hire_date, Manager)
VALUES (432, 'Dana', 'Shorts', 'CEO', '10/12/2017', 1); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO EMPLOYEES (Employ_ID, First, Last, Title, Hire_date, Manager)
VALUES (123, 'Helen', 'Bye', 'CCO', '10/12/2017', 1); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO EMPLOYEES (Employ_ID, First, Last, Title, Hire_date, Manager)
VALUES (456, 'Johnal', 'Bye', 'CTO', '10/12/2017', 1); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO EMPLOYEES (Employ_ID, First, Last, Title, Hire_date, Manager)
VALUES (789, 'Kavit', 'Bye', 'CFO', '10/12/2017', 1); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO EMPLOYEES (Employ_ID, First, Last, Title, Hire_date, Manager)
VALUES (223, 'Natalie', 'Bye', 'COO', '10/12/2017', 1); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO EMPLOYEES (Employ_ID, First, Last, Title, Hire_date, Manager)
VALUES (223, 'John', 'Bye', 'Programmer', '10/12/2017', 0); """
cursor.execute(sql_command)

######### CREATE CUSTOMER TABLE #############
sql_command = """
CREATE TABLE IF NOT EXISTS CUSTOMERS (
CustID INT(5) NOT NULL,
Fname VARCHAR(20) NOT NULL,
Lname VARCHAR(30) NOT NULL,
Phone VARCHAR(15) NOT NULL,
Email VARCHAR(50),
YTD_Sales VARCHAR(20), 
PRIMARY KEY(CustID));"""
cursor.execute (sql_command)
#NEED TO WORK OUT YTD SALES

######## CREATE INVENTORY TABLE #######
sql_command = """
CREATE TABLE IF NOT EXISTS INVENTORY (
Item_Number INT(10) NOT NULL,
Name VARCHAR(15) NOT NULL,
Units_In_Stock INT(5) NOT NULL,
PRIMARY KEY (Item_Number),
FOREIGN KEY (Item_Number) REFERENCES PRODUCTS (ItemNumber)
FOREIGN KEY (Units_In_Stock) REFERENCES PRODUCTS (Available));"""
cursor.execute (sql_command)


######## MANUAL ENTRY OF INVENTORY ITEMS #####
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (88222, 'Intake', 572); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (15675, 'Exhaust', 213); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (25531, 'Bucket Seat', 52); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (74515, 'Steering Wheel', 75); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (83246, 'Shift Knob', 93); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (55677, 'Coilovers', 36); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (98743, 'Supercharger', 13); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (63215, 'Turbocharger', 6); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (67052, 'Oil Cap', 47); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO INVENTORY (Item_Number, Name, Units_In_Stock)
VALUES (73372, 'Filter', 104); """
cursor.execute(sql_command)

######## CREATE PRODUCTS TABLE #######
sql_command = """
CREATE TABLE IF NOT EXISTS PRODUCTS (
ItemNumber INT(5) NOT NULL,
Description VARCHAR(20) NOT NULL,
Price DECIMAL(10, 2) NOT NULL,
Available INT(5) NOT NULL,
Class VARCHAR(10) NOT NULL,
Origin VARCHAR(15) NOT NULL,
Lead_Time VARCHAR(20) NOT NULL,
PRIMARY KEY (ItemNumber));"""
cursor.execute (sql_command)

###### MANUAL ENTRY OF PRODUCTS ######
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('88222', 'Intake', 249.99, 572, 'Engine', 'Japan', '3-4 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('15675', 'Exhaust', 799.99, 213, 'Exhaust', 'Japan', '5-6 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('25531', 'Bucket Seat', 1299.99, 52, 'Interior', 'China', '10-12 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('74515', 'Steering Wheel', 199.99, 75, 'Interior', 'Italy', '2-3 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('83246', 'Shift Knob', 79.99, 93, 'Interior', 'Italy', '2-3 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('55677', 'Coilovers', 1399.99, 36, 'Suspension', 'Japan', '4-6 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('98742', 'Supercharger', 4599.99, 13, 'Engine', 'USA', '5-6 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('63215', 'Turbocharger', 6299.99, 6, 'Engine', 'USA', '7-8 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('67052', 'Oil Cap', 59.99, 47, 'Engine', 'Japan', '2-3 weeks'); """
cursor.execute(sql_command)
sql_command = """INSERT OR REPLACE INTO PRODUCTS (ItemNumber, Description, Price, Available, Class, Origin, Lead_Time)
VALUES ('73372', 'Filter', 59.99, 104, 'Engine', 'Japan', '1-2 weeks'); """
cursor.execute(sql_command)

######## CREATE RECEIPT TABLE #######
#TransactionID = YYMMDD+0001 (incrementing value that resets on new day)
#sql_command = """
#CREATE TABLE IF NOT EXISTS RECEIPTS (
#TransactionID INT(20) NOT NULL, 
#Date DATE NOT NULL,
#RegisterNumber INT(2) NOT NULL,
#Total DECIMAL(10, 2) NOT NULL,
#Available INT(5) NOT NULL,
#PaymentType VARCHAR(10) NOT NULL,
#PRIMARY KEY (TransactionID));"""
#cursor.execute (sql_command)

####### CREATE TRANSACTIONS TABLE #######
sql_command = """
CREATE TABLE IF NOT EXISTS TRANSACTIONS (
transactionID VARCHAR(30) NOT NULL,
Itemnum INT(10) NOT NULL,
CustID INT(5) NOT NULL,
OrderDate VARCHAR(10) NOT NULL,
Quantity INT(5) NOT NULL,
Paid DECIMAL(10, 2) NOT NULL,
PRIMARY KEY (transactionID),
FOREIGN KEY (CustID) REFERENCES CUSTOMERS(CustID),
FOREIGN KEY (Itemnum) REFERENCES PRODUCTS(ItemNumber));"""
cursor.execute (sql_command)
connection.commit()


def main(): 
    running = True

    while running:
        print("1 = Reports")
        print("2 = Add Customer, Orders, Inventory, or Products")
        print("3 = Discontinued, threshold for reordering")
        print("4 = Daily Ledger")
        print("5 = New Sale")
        print("6 = End of Day Report")
        print("7 = Exit program")
        cmd = int(input(">> "))
        prev = True
        if cmd == 1:
            print("1 = Inventory Report")
            print("2 = Customers Listing")
            print("3 = Products Report")
            print("4 = Transactions Record")
            print("5 = Customer Transaction History")
            print("6 = Previous Page")
            cmd = input(">> ")
            if cmd == 1:
                inventory()
            elif cmd == 2:
                customers()
            elif cmd == 3:
                products()
            elif cmd == 4:
                orders()
            elif cmd == 5:
                transactions()                
            else:
                previous()

        elif cmd == 2:
            print("1 = Add Customer")
            print("2 = Add Order")
            print("3 = Add/Edit Products")
            print("4 = Add Inventory")
            print("5 = Previous Page")
            cmd = input(">> ")
            if cmd == 1:
                addCustomer()
            elif cmd == 2:
                addOrder()
            elif cmd == 3:
                addProducts()
            elif cmd == 4:
                pass
            #addInventory()
            else:
                previous()

        elif cmd == 3:
            bl = True
            print("1 = Delete Discontinued item from Inventory and Products")
            print("2 = List the item which are reached the threshold for reordering")
            print("3 = Previous Page")
            cmd = input(">> ")
            if cmd == 1:
                Discontinued()
            elif cmd == 2:
                    SoldOut()
            elif cmd == 3:
                previous()

        elif cmd == 4:
            ledger()
            previous()
            
        elif cmd == 5:
            # call new sale function
            newSale()

        elif cmd == 6:
            # End of day report
            endofday()

        elif cmd == 7:
            # call the end function
            end()
            break
        
        else:
            end()
            break

def inventory():
    print("------Inventory Report------")
    
    cursor.execute("SELECT * FROM INVENTORY") 
    result = cursor.fetchall() 
    for r in result:
        print (r)


def customers():
    customer_table = 'CUSTOMERS'
    cust_ID = 'CustID'
    fname = 'Fname'    
    lname = 'Lname'    
    phone = 'Phone'    
    email = 'Email'    
    ytd = 'YTD_Sales'    
    
    
    running = True
    while running:
        print("1 = Full Customer Report") #Item Number, Products, Stock Levels, 
        print("2 = Individual Customer Report") #CustID, First Name, Last Name, Phone, Email, YTD Sales
        
        
        cmd = int(input(">> "))
        if cmd == 1:      
            print("------Full Customer Listing------")
    
            cursor.execute("SELECT * FROM CUSTOMERS") 
            result = cursor.fetchall() 
            for r in result:
                print (r)    
                
        if cmd == 2:      
            print("------Individual Customer Listing------")
            
            custId = raw_input('Please enter the existing client ID: ')
            cursor.execute('SELECT * FROM CUSTOMERS WHERE {idf}={my_id}'.\
                               format(coi = fname, tn=customer_table, idf = cust_ID, my_id = custId))
            id_exists = cursor.fetchall()
            if id_exists:
                print('Customer Report: {}'.format(id_exists))
            else:
                print('{} does not exist'.format(custId))  
                
        else:
            break
            
                                
def products():
    print("------Product Report------")
    
    cursor.execute("SELECT * FROM PRODUCTS") 
    result = cursor.fetchall() 
    for r in result:
        print (r)

        
def orders():
    print("———List of Transactions———")
    cursor.execute("SELECT * FROM TRANSACTIONS")
    result = cursor.fetchall()
    for r in result:
        print (r)
    
    
def transactions():
    print("------Transaction History------")

    id = int(input('Please enter customer ID: '))   
    
    cursor.execute('''SELECT TRANSACTIONS.OrderDate, PRODUCTS.Description, CUSTOMERS.Fname, CUSTOMERS.Lname, CUSTOMERS.Phone, TRANSACTIONS.Paid
                    FROM CUSTOMERS, TRANSACTIONS, PRODUCTS WHERE CUSTOMERS.CustID = TRANSACTIONS.CustID AND TRANSACTIONS.Itemnum = PRODUCTS.ItemNumber AND CUSTOMERS.CustID = ?''', (id,))        
    result = cursor.fetchall()
    for r in result:
        print (r)        
        
    
    
def ledger():
    print("------Daily Ledger------")
    

def addCustomer():
    print("------Add a customer to the list------")
    
    custId = raw_input('Enter client ID: ')
    first = raw_input('Enter client first name: ')
    last = raw_input('Enter client last name: ')  
    phone = raw_input('Enter client phone number: ')
    email = raw_input('Enter client email: ')
    ytd = raw_input('Enter client money spent: ')    
          
    print ("The customer has been added to the database")
    
    sql_command = "INSERT INTO CUSTOMERS VALUES (?, ?, ?, ?, ?, ?);"
    cursor.execute(sql_command, (custId, first, last, phone, email, ytd))
    connection.commit()    
    
    
    
def addProducts():
    
    running = True
    while running:
        print("1 = Add a new product") #...
        print("2 = Edit an exisitng product") #...
        print("*****Press any other key to exit") #...
        
        
        cmd = int(input(">> "))
        if cmd == 1:      
            print("------Please enter new product information------")
            
            itemnum = int(input('Enter Item Number: '))
            descrip = raw_input('Enter Item Description: ')
            cost = raw_input('Enter product price: ')  
            stock = raw_input('Enter available quantities: ')
            custclass = raw_input('Enter product class: ')
            origin = raw_input('Enter product origin: ')    
            ldtime = raw_input('Enter product lead time: ')   
        
            print ("The product has been added to the database")
        
            sql_command = "INSERT INTO PRODUCTS VALUES (?, ?, ?, ?, ?, ?, ?);"
            cursor.execute(sql_command, (itemnum, descrip, cost, stock, custclass, origin, ldtime))
            connection.commit()            
            
        if cmd == 2:      
            print("------Please enter the item number to edit------")
            itemnum = int(input(': '))
            
            print("What information would you like to udpate ? Desc, Price, Avail, Class, Orgn, or lead")
            choice = raw_input(': ')
            
            if choice == 'Desc':
                newDesc = raw_input('Enter a new product description: ')
                cursor.execute ("UPDATE PRODUCTS SET Description = ? WHERE ItemNumber = ?", [newDesc, itemnum])                
                connection.commit()     
                
            elif choice == 'Price':                   
                newPrice = raw_input('Enter a new product price: ')
                cursor.execute ("UPDATE PRODUCTS SET Price = ? WHERE ItemNumber = ?", [newPrice, itemnum])                
                connection.commit()
                
                
            elif choice == 'Avail':
                newAvail = raw_input('Enter a new product availability: ')
                cursor.execute ("UPDATE PRODUCTS SET Available = ? WHERE ItemNumber = ?", [newAvail, itemnum])                
                connection.commit() 
                
            elif choice == 'Class':
                newClass = raw_input('Enter a new product class: ')
                cursor.execute ("UPDATE PRODUCTS SET Class = ? WHERE ItemNumber = ?", [newClass, itemnum])                
                connection.commit()       
                
            elif choice == 'Orgn':
                newOrigin = raw_input('Enter a new product origin: ')
                cursor.execute ("UPDATE PRODUCTS SET Origin = ? WHERE ItemNumber = ?", [newOrigin, itemnum])                
                connection.commit()                  
                
            elif choice == 'Lead':
                newlead = raw_input('Enter a new product lead time: ')
                cursor.execute ("UPDATE PRODUCTS SET Lead_Time = ? WHERE ItemNumber = ?", [newlead, itemnum])                
                connection.commit()  
                
            else:
                running = False
            
        
            print ("*The product has been updated*")
            selection = raw_input('Update or add another product? (Y)es, (N)o: ')
            
            
            if selection == 'Y':
                previous()
            else:
                running = False
            
        else:
            running = False
            
                

#def addOrder():
 #   print("------ADD Orders------")
    
  #  custId = input('Enter client ID: ')
   # item = int(input('Enter item number: '))
    #date = input('Enter order date (MMDDYYYY): ')
    #quant = input('Enter quantities of the item: ')
    #cost = input('Enter in cost of item: ')
    
    #add transaction to orders table    
    #sql_command = "INSERT INTO TRANSACTIONS VALUES (?, ?, ?, ?, ?);"
    #cursor.execute(sql_command, (item, custId, date, quant, cost))
    #connection.commit()        
    #print ("The order has been added to the database")
    
    
    #decrease the Units_in_Stock
    #units = cursor.execute("SELECT Units_In_Stock FROM INVENTORY WHERE Item_Number = ?", (item,)).fetchone()[0]
    #units = units - quant
    #cursor.execute("UPDATE INVENTORY SET Units_In_Stock = ? WHERE Item_Number = ?", [units, item])
    
    

def SoldOut():
    print("———Items reached the threshold for reordering———")
    cursor.execute("SELECT * FROM INVENTORY WHERE Units_In_Stock == 0")
    result = cursor.fetchall()
    for r in result:
        print (r)

def Discontinued():
        print("Input the item number discontinued item")
        item = input('Enter item number: ')
        cursor.execute("DELETE FROM INVENTORY WHERE Item_Number = ?", (item,))
        cursor.execute("DELETE FROM PRODUCTS WHERE Item_Number = ?", (item,))

def newSale():
    products_table = 'PRODUCTS'
    item_ID = 'ItemNumber'
    product_descrip = 'Description'

    purchaseList = []
    print("--------New Sale-------")
    timestamp = datetime.now()
    date = datetime.today().strftime("%m/%d/%Y")
    transactionID = (timestamp.strftime('%y%m%d%H%M%S%f'))
    print ("Transaction ID: " +(transactionID))
    custID = input("Enter customer phone number (0 to decline): ")
    #Needs to check if customer is in database or not. If not, adds new customer.
    #If so, add this transaction to their records.
    while True:
        qty = input("Enter quantity of product to be purchased (0 to exit): ")
        if (qty == 0):
            break
        itemToBuy = input("Enter product ID: ")
        cursor.execute('SELECT ({coi}) FROM {tn} WHERE {idf}={my_id}'.\
                       format(coi = product_descrip, tn=products_table, idf = item_ID, my_id = itemToBuy))
        id_exists = [row[0] for row in cursor.fetchall()]
        if id_exists:
            print('Product Description: {}'.format(id_exists))
            purchaseList.append(qty)
            purchaseList.append(itemToBuy)
        else:
            print('{} does not exist'.format(itemToBuy))
            
        price = cursor.execute("SELECT Price FROM PRODUCTS WHERE PRODUCTS.ItemNumber = ?", (itemToBuy,)).fetchone()[0]   
        #add transaction to transactions table    
        sql_command = "INSERT INTO TRANSACTIONS VALUES (?, ?, ?, ?, ?, ?);"
        cursor.execute(sql_command, (transactionID, itemToBuy, custID, date, qty, price))
        connection.commit()        
              
        #decrease the Units_in_Stock\
        units = cursor.execute("SELECT Units_In_Stock FROM INVENTORY WHERE Item_Number = ?", (itemToBuy,)).fetchone()[0]
        units = units - qty
        cursor.execute("UPDATE INVENTORY SET Units_In_Stock = ? WHERE Item_Number = ?", [qty, itemToBuy])   
        
        print ("The transaction has been added to the database and items removed from stock")
        
     
            

    #once all qty and items have been entered, use list to pull pricing from database,
    #and multiply by quantity from list as well to come up with total and breakdown for receipt.
    print(*purchaseList, sep='\n')
    print('\n')
         
    #lookup product from database -- make sure exists -- collect price and description
    # If using raw_inputTo convert purchaseList to list of ints use
    #(Python 2) purchaseList = map(int, purchaseList) or
    #(Python 3) purchaseList = list(map(int, purchaseList))

# end function  
def end():
    print("ending Inventory System.....")
    running = False

def endofday():
    numcash = 0
    numcard = 0
    print("----------------Total Cash Sale----------------")
    cursor.execute("SELECT * FROM RECEIPTS WHERE PaymentType == 'CASH'")
    result = cursor.fetchall()
    for c in result:
        numcash = numcash + 1
        print(c)
    cursor.execute("SELECT SUM(Total) FROM RECEIPTS WHERE PaymentType == 'CASH'")
    cashresult = cursor.fetchall()
    print ("\nTotal Cash Amount Sales : $", cashresult[0][0])
    print("Total Number of Cash Sale ", numcash)
    print("----------------Total Credit/debit Sale----------------")
    cursor.execute("SELECT * FROM RECEIPTS WHERE PaymentType == 'CARD'")
    result = cursor.fetchall()
    for c in result:
        numcard = numcard + 1
        print(c)
    cursor.execute("SELECT SUM(Total) FROM RECEIPTS WHERE PaymentType == 'CARD'")
    cardresult = cursor.fetchall()
    print("\nTotal Card Amount Sales : $", cardresult[0][0])
    print("Total Number of Card Sale ", numcard)
    #print(card)
    #print("\n")
    print("----------------Total Items “damaged out”----------------")
    print ("\n\n")


def previous():
    prev = False


# -----------------------------------------------
# call the main function
main()
cursor.close()
connection.close()
