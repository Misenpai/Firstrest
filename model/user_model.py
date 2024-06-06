import mysql.connector
import json
from flask import make_response


class user_model():

    def __init__(self):

        try:
            self.conn = mysql.connector.connect(host="localhost",user = "root", password = "1234", database = "flask_tutorial")
            self.conn.autocommit = True
            self.curr = self.conn.cursor(dictionary=True)
            print("Succussfully Connected")
        except:
            print("Connection Error")

    def user_getall_model(self):
        self.curr.execute("SELECT * FROM users")
        result = self.curr.fetchall()

        if len(result)>0:  
            return make_response({"result":result},200)
        else:
            return make_response({"message":"no data in the database"}, 204)
        
    def user_adduser_model(self,data):
        self.curr.execute(f"INSERT INTO users(name,email,phone,role,password) VALUES('{data['name']}','{data['email']}','{data['phone']}','{data['role']}','{data['password']}')")
        print(data)
        return make_response({"message":"Successfully added the user"},200)
    
    def user_updatauser_model(self,data):
        self.curr.execute(f"UPDATE users SET name='{data['name']}', email='{data['email']}', phone='{data['phone']}' WHERE id={data['id']}")

        if self.curr.rowcount>0:
            return make_response({"message":"Successfully updated the user"},200)
        else:
            return make_response({"message":"Error occurred while updating the user"},204)
        
    def user_deleteuser_model(self,id):
        self.curr.execute(f"DELETE FROM users WHERE id={id}")
        if self.curr.rowcount>0:
            return make_response({"message":"Successfully deleted the user"},200)
        else:
            return make_response({"message":"Error while deleting the user"},204)