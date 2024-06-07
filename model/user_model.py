import mysql.connector
from flask import make_response
from datetime import datetime,timedelta
import jwt
from config.config import dbconfig


class user_model():

    def __init__(self):

        try:
            self.conn = mysql.connector.connect(host=dbconfig['host'],user = dbconfig['username'], password = dbconfig['password'], database = dbconfig['database'])
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
        
    def user_patchuser_model(self,data):
        qry = "UPDATE users SET "
        for key in data:
            if key!='id':
                qry += f"{key}='{data[key]}',"
        qry = qry[:-1] + f" WHERE id = {data['id']}"
        self.curr.execute(qry)
        if self.curr.rowcount>0:
            return make_response({"message":"Successfully Updated the user"},200)
        else:
            return make_response({"message":"Error Occured"},204)
           
    def pagination_model(self, pno, limit):
        pno = int(pno)
        limit = int(limit)
        start = (pno*limit)-limit
        qry = f"SELECT * FROM users LIMIT {start}, {limit}"
        self.curr.execute(qry)
        result = self.curr.fetchall()
        if len(result)>0:
            return make_response({"page":pno, "per_page":limit,"this_page":len(result), "payload":result})
        else:
            return make_response({"message":"No Data Found"}, 204)
        
    def upload_avatar_model(self,uid,finalFilePath):
        self.curr.execute(f"UPDATE users SET avatar='{finalFilePath}' WHERE id={uid}")
        if self.curr.rowcount>0:
            return make_response({"message":"Successfully Uploaded the file"},200)
        else:
            return make_response({"message":"Error Occured"},204)
        
    def user_login_model(self, data):
        self.curr.execute(f"SELECT id, role_id, avatar, email, name, phone from users WHERE email='{data['email']}' and password='{data['password']}'")
        result = self.curr.fetchall()
        if len(result)==1:
            exptime = datetime.now() + timedelta(minutes=60)
            exp_epoc_time = exptime.timestamp()
            data = {
                "payload":result[0],
                "exp_time":int(exp_epoc_time)
            }

            jwt_token = jwt.encode(data, "Sumit", algorithm="HS256")
            return make_response({"token":jwt_token}, 200)
        else:
            return make_response({"message":"NO SUCH USER"}, 204)