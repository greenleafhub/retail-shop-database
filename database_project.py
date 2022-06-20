import pymysql

#try get local password file
localDbPassword=''
try:
    f = open("localpw.txt", "r")
    localDbPassword=f.read()
    f.close()
except:
    localDbPassword='password'
    
#Connect to database
db = pymysql.connect(host='localhost',
                     user='root',
                     password=localDbPassword,
                     database='Comp7640_Proj')
cursor = db.cursor()

#global vars
#table format string
tblFormat1 = "{:<6} {:<40} {:<20} {:<8} {:<40}"
tblFormat2 = "{:<6} {:<20} {:<20} {:<40}"

#User ID
userid = "NULL"

#Fet number input from user
def getInput(option, mode):
    #mode values:
    #0 from main menu
    #1 from shop menu
    #2 from 

    if mode == 0: #main menu
        for i in range(1,len(option)):
            print("{:<6} {:<50}".format((str(i)+":"), option[i])) #main menu items
        print("{:<6} {:<50}".format((str(0)+":"), option[0])) #quit prog

    elif mode == 1: #all shops, select shop
        for i in range(0,len(option)):
            print("{:<6} {:<50}".format((str(i+1)+":"), option[i]))    
        print("{:<6} {:<50}".format(("0:"), "[Go Back]"))
        
    # elif mode == 2: # 
    #     for i in range(0,len(option)):
    #         print("{:<6} {:<40} {:<20} {:<8}".format((str(i+1)+":"), option[i][0], option[i][1], option[i][2]))

    elif mode == 4: #showallcoustomer 
        for i in range(0,len(option)):
            print(tblFormat2.format((str(i+1)+":"),option[i][0], option[i][1], option[i][2]))

    elif mode == 5: #getorder
        for i in range(0,len(option)):
            print("{:<6} {:<50}".format((str(i+1)+":"),option[i][0]))

    #Simple data validation
    while True:
        try: 
            val = Input = int(input("Enter number : "))
        except ValueError:
            print("Input must be an integer!")
            continue
        else:
            val = int(val)
            if ((val < 0) or (val > len(option))):
                print("Input must be within 1-"+str(len(option))+"!")
                continue
            break
    print("") 
    return val

#Show all item of a shop
def showItems(shop_id):

    #get shop_name
    sql = "SELECT shop_name FROM Shops WHERE shop_id = %s"
    cursor.execute(sql, (shop_id, ))
    shopName = cursor.fetchone()[0]

    print("All items sold by "+ shopName +" [ID: "+shop_id+"]:")
    print("")
    print("{:<6} {:<15} {:<40} {:<20} {:<8}".format("", "Item ID", "Item Name", "Price(HKD)", "Quantity"))
    try:
        sql = "SELECT item_id, item_name, price, stock_qty FROM items_sell WHERE shop_id = %s"
        cursor.execute(sql, (shop_id, ))
        rows = cursor.fetchall()
        result = []
        if len(rows)>0:
            for row in rows:
                temp = []
                temp.append(row[0])
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[3])
                result.append(temp)
            for i in range(0,len(result)):
                print("{:<6} {:<15} {:<40} {:<20} {:<8}".format((str(i+1)+":"), result[i][0], result[i][1], result[i][2], result[i][3]))
        else:
            print("[This shop is empty]")

    except:
        print("Error fetching data!")
    menu()

#Get all shop
def allShops():
    print("Shops list:")
    sql = "SELECT shop_name, shop_id FROM Shops"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        result = [row[0]+" ("+row[1]+")" for row in rows]
        id = [row[1] for row in rows]

        input = getInput(result, 1)
        if input > 0:            
            shop_id = id[input-1]
            showItems(shop_id)
        elif input == 0:
            menu()           

    except:
        print("Error fetching data!")

    #Switch for different shop

def newShop():
    #Get shop name and check if any duplicate
    name = input("Enter name of the shop: ")
    # sql = "SELECT shop_name FROM Shops WHERE shop_name=%s"
    # check = cursor.execute(sql, name)
    # while check == 0:
    #     print("Shop name already occupied!")
    #     name = input("Enter name of the shop: ")
    #     sql = "SELECT shop_name FROM Shops WHERE shop_name=%s"
    #     check = cursor.execute(sql, name)
    #Get location
    location = input("Enter location of the shop: ")

    #Insert data
    try:
        num = cursor.execute("SELECT shop_name FROM Shops") + 1
        id = str(num).zfill(4)
        id = "S" + id
        sql = "INSERT INTO Shops (shop_id, shop_name, rating, location) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql,(id, name, 0, location))
        db.commit()
        print(name + " successfully added!")
        print("")
        menu()
    except:
        print("Error fetching data!")

def newItem():
    shop_id = input("Enter ID of the shop: ")
    try:
        sql = "SELECT shop_name FROM Shops WHERE shop_id=%s"
        check = cursor.execute(sql, shop_id)
    except Exception as e:
        print(str(e))
    while check == 0:
        print("Shop did not exist!")
        shop_id = input("Enter ID of the shop: ")
        sql = "SELECT shop_name FROM Shops WHERE shop_id=%s"
        check = cursor.execute(sql, shop_id)
    name = input("Enter name of new item: ")
    while True:
        try:
            price = int(input("Price of new item: "))
            qty = int(input("Quantity of new item: "))
        except ValueError:
            print("Price and Quantity of new item must be an integer!")
            continue
        else:
            price = int(price)
            qty = int(qty)
            break
    kw1 = input("Keyword 1 of new item: ")
    kw2 = input("Keyword 2 of new item: ")
    kw3 = input("Keyword 3 of new item: ")
    num = cursor.execute("SELECT item_id FROM items_sell WHERE shop_id=%s",shop_id) + 1
    item_id = str(num).zfill(4)
    item_id = shop_id+"I"+item_id
    #item_id parsed in SxxxIxxx format for human-readability

    try:
        if kw1 != "" and kw2 != "" and kw3 != "":
            sql = "INSERT INTO items_sell (item_id, item_name, price, stock_qty, keyword1, keyword2, keyword3, shop_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(item_id, name, price, qty, kw1, kw2, kw3, shop_id))
        elif kw1 != "" and kw2 != "" and kw3 == "":
            sql = "INSERT INTO items_sell (item_id, item_name, price, stock_qty, keyword1, keyword2, shop_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(item_id, name, price, qty, kw1, kw2, shop_id))
        elif kw1 != "" and kw2 == "" and kw3 == "":
            sql = "INSERT INTO items_sell (item_id, item_name, price, stock_qty, keyword1, shop_id) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(item_id, name, price, qty, kw1, shop_id))
        elif kw1 == "" and kw2 == "" and kw3 == "":
            sql = "INSERT INTO items_sell (item_id, item_name, price, stock_qty, shop_id) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql,(item_id, name, price, qty, shop_id))
        else:
            print("There is an error!")
        db.commit()
        print(name + " successfully added!")
        print("")
        menu()
    except:
        print("Error fetching data!")

#Search all items
def searchItems():
    keyword = input("Input keyword: ")
    if keyword != "":
        print("All items that matches the keyword: ", keyword)
        print("")
        print(tblFormat1.format("", "Item Name", "Price(HKD)", "Shop ID", "Shop Name"))
        try:
            #partial matches
            # sqlWhereClause = "("
            # sqlWhereClause = sqlWhereClause+ "item_name LIKE '%" + keyword + "%' OR "
            # sqlWhereClause = sqlWhereClause+  "keyword1 LIKE '%" + keyword + "%' OR "
            # sqlWhereClause = sqlWhereClause+  "keyword2 LIKE '%"+ keyword + "%' OR "
            # sqlWhereClause = sqlWhereClause+  "keyword3 LIKE '%" + keyword + "%'"
            # sqlWhereClause = sqlWhereClause+  ")"
            #
            # sql = "SELECT item_name, price, i.shop_id, shop_name FROM items_sell i, shops s WHERE i.shop_id=s.shop_id AND " + sqlWhereClause
            # cursor.execute(sql)

            #full matches only
            sql = "SELECT item_name, price, i.shop_id, shop_name FROM items_sell i, shops s WHERE i.shop_id=s.shop_id AND(item_name = %s OR keyword1 = %s OR keyword2 = %s OR keyword3 = %s)"
            cursor.execute(sql, (keyword, keyword, keyword, keyword,))

            rows = cursor.fetchall()
            result = []
            for row in rows:
                temp = []
                temp.append(row[0])
                temp.append(row[1])
                temp.append(row[2])
                temp.append(row[3])
                result.append(temp)
            for i in range(0,len(result)):
                print(tblFormat1.format((str(i+1)+":"), result[i][0], result[i][1], result[i][2],result[i][3]))
        except:
            print("Error fetching data!")            
    else:
        print("No keyword detected")        
    menu()

def showAllCustomers():
    print("Customers list:")
    sql = "SELECT customer_id, tel_no, addr FROM customers"
    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        if len(rows)>0:            
            print(tblFormat2.format(" ","Customer Id", "Phone Number", "Address"))
            # for customer in rows:
            #     print(tblFormat2.format((customer[0]+":"), customer[1], customer[2]))
            val = getInput(rows,4)
            global userid
            userid = rows[val-1][0]
            print("SELECTED ",userid)
        else:
            print("No customers found.")
            
    except:
        print("Error fetching data from customers table")
    finally:
        menu()

def createCustomer():

    phNum = input("Enter Phone Number: ")
    address = input("Enter Address: ")

    #Insert data
    try:
        num = cursor.execute("SELECT customer_id FROM customers") +1
        id = str(num).zfill(4)
        id = "C" + id
        print(id)

        sql = "INSERT INTO customers (customer_id, tel_no, addr) VALUES (%s, %s, %s)"
        cursor.execute(sql,(id, phNum,address))
        print("sql ran")
        db.commit()
        print("Customer with Phone Number: " + phNum + " successfully added!")
        print("")
        menu()
    except:
        print("Error fetching data!")

def showOrders():
    if userid == "NULL":
        print("Please select a customer first in the Show all customers function first!")
        menu()
    else:
        try:
            sql = "SELECT order_id FROM Orders_Purchase WHERE customer_id = %s"
            cursor.execute(sql, userid)
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("No orders from selected user")
                menu()
            else:
                val = getInput(rows,5)
                orderid = rows[val-1][0]
                showOrderItem(orderid)
        except:
            print("Error fetching orders of selected users")

def showOrderItem(orderid):
    try:
        sql = "SELECT Items_Sell.item_name, Items_Sell.price, Transactions.item_id, Transactions.order_qty FROM Items_Sell INNER JOIN Transactions ON Items_Sell.item_id = Transactions.Item_id WHERE Transactions.order_id = %s"
        cursor.execute(sql, orderid)
        rows = cursor.fetchall()
        for row in rows:
            print("{:<50} {:<15} {:<7} {:<5}".format(row[0],row[2],row[1],row[3]))
        print("\n")

        options = ["Back to main menu","Delete entrie order","Update some items"]
        val = getInput(options, 0)

        if val == 0:
            menu()
        elif val == 1:
            deleteAllTransactions(orderid)
        elif val == 2:
            updateOrderItemQuantity(orderid, rows)

    except Exception as e:
        print("Error fetching items from selected order")
        print(str(e))

#Operations for editing orders deleted entire order or delete some items
def deleteOrder(orderid):
    try:
        sql = "DELETE FROM Orders_Purchase WHERE order_id = %s AND customer_id = %s"
        cursor.execute(sql, (orderid, userid))
        db.commit()
        print("Successfully deleted the order")
        menu()
    except Exception as e:
        print(str(e))

def deleteAllTransactions(orderid):   
    try:  
        sql = "DELETE FROM Transactions WHERE order_id = %s "
        cursor.execute(sql, (orderid))
        db.commit()
        deleteOrder(orderid)
        print("Successfully deleted the order")
        menu()
    except Exception as e:
        print(str(e))

def updateOrderItemQuantity(orderid, rows):
    for i in range(0,len(rows)):
        print("{:<50} {:<15} {:<7} {:<5}".format(rows[i][0],rows[i][2],rows[i][1],rows[i][3]))
    print("\n0: Back to main menu")
    try:
        itemid, new_qty = input("Enter ItemID and New Quantity: ").split()
        new_qty = int(new_qty)

        print(new_qty, type(new_qty))

        if new_qty == 0:
            sql = "DELETE FROM Transactions WHERE order_id = %s AND item_id = %s"
            cursor.execute(sql, (orderid, itemid))
            db.commit()
            print("Successfully deleted",itemid,"from the order")
            sql = "SELECT * FROM Transactions WHERE order_id = %s"
            num = cursor.execute(sql, (orderid, ))
            if num == 0:
                deleteOrder(orderid)
        else:
            sql = "UPDATE Transactions SET order_qty = %s WHERE item_id = %s AND order_id = %s"
            cursor.execute(sql, (new_qty, itemid, orderid))
            db.commit()
            print("\nSuccessfully updated quantity of",itemid,"to",new_qty)
            print("\n")
        showOrderItem(orderid)
    except ValueError:
        menu()
    except Exception as e:
        print("Error deleting items from selected order")
        print(str(e))

def IteminOrders(id, userid):
    itemid, qty = input("Enter ItemID and Quantity: ").split()
    qty = int(qty)
    try:
        try:            
            sql = "INSERT INTO transactions (order_id, item_id, order_qty) VALUES (%s, %s, %s)"
            cursor.execute(sql,(id, itemid, qty))
            db.commit()
            print("itemID " + itemid + " successfully added!")
            print("")
            continueorder(id, userid)                
        
        except (pymysql.Error, pymysql.Warning) as e:
            print(e)
            CheckifOrderEmpty(id, userid)      
            
    except:
        print("Error occured! Item does not exist/Same item already added to your order")
        CheckifOrderEmpty(id, userid)                 


def CheckifOrderEmpty(id, userid):
    sql = "SELECT order_id FROM transactions WHERE order_id = %s"
    cursor.execute(sql, (id))
    iteminorder = cursor.fetchall()
    if len(iteminorder) == False:
        print("Order "+id+" has no items, will be deleted.")
        deleteOrder(id)
    else:
        continueorder(id, userid)    

def continueorder(id, userid):
    option = input("Do you want to add more items into the order? [Y/N]: ")
     
    if option == "Y" or option =="y":
        IteminOrders(id, userid)
    else:
        print("Order "+id+" completed!")
        menu()   

def createOrders():
    if userid == "NULL":
        print("Please select a customer first in the Show all customers function first!")
        menu()
    else:
            try:
                cursor.execute("SELECT MAX(order_id) FROM orders_purchase")
                result = cursor.fetchone()
                result = result[0]             
                result = int(result[1:5])       
                id = result + 1
                id = str(id).zfill(4)
                id = str("O" + id)          
                sql = "INSERT INTO orders_purchase (order_id, customer_id) VALUES (%s, %s)"
                cursor.execute(sql,(id, userid))
                db.commit()
                print("Order ID " + id + " successfully created for user "+ userid+"!")
                print("")
                IteminOrders(id, userid)
            except:
                print("Error fetching data!")
                CheckifOrderEmpty(id, userid)

#Main menu function
def menu():
    print("")
    print("Main Menu - Please select an option:")
    option = ["Quit", "Show all shops", "Add new shop","Add new item","Search by item keyword","Show all customers","Add new customer","Show Orders","Create Orders"]
    val = getInput(option, 0)

    #Switch for different option
    if (val == 0):
        return
    elif (val == 1):
        allShops()
    elif (val == 2):
        newShop()
    elif (val ==3):
        newItem()
    elif (val ==4):
        searchItems()
    elif (val ==5):
        showAllCustomers()
    elif (val ==6):
        createCustomer()
    elif (val ==7):
        showOrders()
    elif (val ==8):
        createOrders()
        
    else:
        print("Error occured")

#main
print("Welcome to our e-shopping platform")
menu()
