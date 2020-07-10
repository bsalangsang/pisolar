import mysql.connector
from mysql.connector import Error

class mysqlExecCmds:
    def __init__(self, dbCon):
       self.db = dbCon
       
    def dbConnect(self):
        try:
            self.db=mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="test"
            )
            
            if self.db.is_connected():
                db_Info = self.db.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.db.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
        except Error as e:
            print("Error while connecting to MySQL", e)
    
    def fetchSql(self,sqlCmd,isAllRecord):
        try:
            
            myCursor=self.db.cursor()
            command =sqlCmd
            myCursor.execute(command)
        
            result = ""
            if bool(isAllRecord) == "False":
                result = myCursor.fetchone() # when fetching specific Record
            else:
                result = myCursor.fetchall()
            return result 
                          
        except mysql.connector.Error as error:
            print("parameterized query failed {}".format(error))

    def execSql(self, execType , targetTable, targetField, targetString, targetValues, updateField):
        try:
            myCursor=self.db.cursor()
            if execType == "insert":
                command = "INSERT INTO " + targetTable + " (" + targetField + ") VALUES "+ targetString + "" 
                myCursor.execute(command,targetValues)
                self.db.commit()
                return "success"
            else:
                command = "UPDATE " + targetTable + " SET "
                for x in range(0, len(targetField)):
                    if x == (len(targetField)-1):
                        command  += targetField[x] + "=" +'%s' + ""
                    else:
                        command += targetField[x] + "=" +'%s' + ","
                command += " " + updateField
                print(command)
                print(targetValues)
                myCursor.execute(command,targetValues)
                self.db.commit()
                return "success"
               
        except mysql.connector.Error as error:
            print("parameterized query failed {}".format(error))