import cx_Oracle

conn = cx_Oracle.connect("scott/tiger@//localhost:1523/orl")
def display(conn):
    try:
        cur = conn.cursor()
        query = "SELECT * FROM LMS_DATA"
        cur.execute(query)
        row = cur.fetchall()
        return row
    except Exception as err:
        print("Error While Executing DISPLAY Query: ",err)
data = display(conn)

class LMS:
    """This Class Is Used To Keep Records of Books Library.
    It Has Total Four Modules : "Display Book", "Issue Book", "Return Book", "Add Book" """
    def __init__ (self,data) :
        self.List_Of_Books= data
        self.books_dict=dict((x,y,) for x, y ,a,b,c in self.List_Of_Books)
        #self.conn = conn
    
    def Display(self) :
        print("------------------LIST OF BOOKS-------------------")
        print("Books ID","\t","Title")
        print("--"*25)
        for key, values in self.books_dict.items():
            print(key,"\t     \t",values)
        print("--"*25)
    
    def Issue_Book(self):
        print("----------------ISSUING BOOKS---------------------")
        book_id=input("Enter Book ID: ")
        try:    
            query_status = "SELECT STATUS FROM LMS_DATA WHERE BOOK_ID = :book_id "
            cur = conn.cursor()
            cur.execute(query_status,{"book_id":book_id})
            row = cur.fetchall()
            tuple= row[0]
            lower = tuple[0]
            status=str(lower.lower())
            print(status)
        except Exception as err:
            print("Error While Executing Query_Status: ",err)
        else:
            if status == 'available':
                lender_name = input("Enter Your Name: ")
                date = input("Enter today's date [dd-mm-yy]: ")
                try :
                    query_issue = """UPDATE LMS_DATA SET STATUS = 'NOT AVAILABLE', 
                    LENDER_NAME = '{}' , ISSUE_DATE = '{}' WHERE BOOK_ID = {} """.format(lender_name, date, book_id)
                    cur = conn.cursor()
                    cur.execute(query_issue)
                except Exception as err:
                        print("Error while executing Query_Issue ",err)
                else:
                    print("BOOK HAS BEEN ISSUED !!!")
                    conn.commit()
                    cur.close()
            else:
                print("Book Is Not Available, Please Try Another Book !!!")
                print("--"*25)


    def Return_Book(self):
        print("----------------RETURNING BOOK---------------------")
        book_id=input("Enter Book ID: ")
        try:    
            query_status = "UPDATE LMS_DATA SET STATUS = 'AVAILABLE' WHERE BOOK_ID = :book_id "
            cur = conn.cursor()
            cur.execute(query_status,{"book_id":book_id})
        except Exception as err:
            print("Error While Executing Query_Status: ",err)
        else:
            conn.commit()
            cur.close()
            print("BOOK RETURNED SUCESSFULLY !!!")
        
    def Add_Book(self):
        print("----------------ADDING BOOK---------------------")
        book_id=input("Enter Book ID: ")
        book_title = input("Enter Book Title: ")
        try:    
            query_insert = " INSERT INTO LMS_DATA VALUES(:1, :2, :3, :4, :5) "
            cur = conn.cursor()
            cur.execute (query_insert,[book_id,book_title,'AVAILABLE',None,None])
        except Exception as err:
            print("Error While Executing Query_Status: ",err)
        else:
            conn.commit()
            cur.close()
            print("BOOK ADDED SUCESSFULLY !!!")
            
        


My_LMS=LMS(data)
press_key_list= {"D":"Display Book","I":"Issued Book","A":"Add Book","R":"Return Book","Q":"Quit"}
key_press = False
while (key_press != "q"):
    print(f"\n---------WELCOME TO Python Library MANAGEMENT SYSTEM---------\n")
    for key,value in press_key_list.items():
        print("Press",key,"To",value)
    print("--"*25)
    key_press = input("Press Key: ").lower()
    #print("--"*25)
    if key_press == "i":
            My_LMS.Issue_Book()
    elif key_press == "a":
            My_LMS.Add_Book()
    elif key_press == "d":
            My_LMS.Display()
    elif key_press == "r":
        My_LMS.Return_Book()
    elif key_press == "q":
            print("Thank You !!!")
            break
    else:
            continue