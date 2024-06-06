from app import app
from model.user_model import user_model
from flask import request
obj = user_model()

@app.route("/users/getall")
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