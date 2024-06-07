from app import app
from model.user_model import user_model
from model.auth_model import auth_model
from flask import request,send_file
from datetime import datetime
obj = user_model()
auth = auth_model()

@app.route("/users/getall")
@auth.token_auth("/users/getall")
def user_getall_controller():
    return obj.user_getall_model()

@app.route("/users/adduser",methods=["POST"])
def user_adduser_controller():
    return obj.user_adduser_model(request.form)

@app.route("/users/updateuser",methods=["PUT"])
def user_updateuser_controller():
    return obj.user_updatauser_model(request.form)

@app.route("/users/deleteuser/<id>",methods=["DELETE"])
def user_deleteuser_controller(id):
    return obj.user_deleteuser_model(id)

@app.route("/users/patchusers",methods=["PATCH"])
def user_patchuser_controller():
    return obj.user_patchuser_model(request.form)

@app.route("/users/page/<pno>/limit/<limit>",methods=["GET"])
def pagination_controller(pno,limit):
    return obj.pagination_model(pno,limit)

@app.route("/users/<uid>/avatar/upload",methods=["PUT"])
def upload_avatar_controller(uid):
    file = request.files['avatar']
    uniqueFileName = str(datetime.now().timestamp()).replace(".","")
    fileNameSplit = file.filename.split(".")
    exe = fileNameSplit[len(fileNameSplit)-1]
    finalFilePath = f"uploads/{uniqueFileName}.{exe}"
    file.save(finalFilePath)
    return obj.upload_avatar_model(uid,finalFilePath)

@app.route("/uploads/<filename>")
def user_get_avatar_controller(filename):
    return send_file(f"uploads/{filename}")


@app.route("/users/login",methods=["POST"])
def user_login():
    return obj.user_login_model(request.form)