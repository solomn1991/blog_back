from flask import Flask,session,request
import json

from config import FLASK_CONFIG

from db.services import UserService
from db.services import PassageService

app = Flask(__name__)
app.config.update(**FLASK_CONFIG)


@app.route("/register",methods=["POST"])
def register():
    username = request.json.get("username");
    password = request.json.get("password");
    email = request.json.get("email")
    user_service = UserService()
    res = user_service.add_user(username,password,email)
    return json.dumps(res)

@app.route("/login",methods=["POST"])
def login():
    if "is_login" in session and session["is_login"]==True:
        result = {"login_success":True,"message":"have logined","user":session["user"]}
        return json.dumps(result)

    username = request.json.get("username");
    password = request.json.get("password");

    # 在数据库中找到对应的账号与密
    user_service = UserService()
    user_info = user_service.find_user(username=username)


    if user_info and user_info.password==password:
        match=True
    else:
        match=False

    if match:
        session["is_login"] = True
        session["user"] = {"username":user_info.username,"id":user_info.id}
        result = {"login_success":True,"message":"login success","user":session["user"]}

    else:
        result = {"login_success":False,"reason":"login fail"}

    return json.dumps(result)


@app.route("/logout",methods=["POST",])
def logout():
    if "is_login" in session:
        session.pop("is_login")
        result = {"logout_success":True,"message":"welcome visit again"}
        return json.dumps(result)
    else:
        result = {"error":"unknown","message":"unknown error"}
        return json.dumps(result)


@app.route("/passage",methods=["POST"])
def add_passage():
    if not "is_login" in session:
        result = {"add_passage_success":False,"message":"请先登录"}
        return json.dumps(result)


    user_id = session["user"].get("id");
    content = request.json.get("content")
    title = request.json.get("title")
    passage_service = PassageService()
    passage = passage_service.add_passage(user_id,title,content)
    result = {"add_passage_success":True,"message":"添加成功","passage":passage}
    return json.dumps(result)

@app.route('/passagelist',methods=["GET"])
def get_user_passage():
    user_id = request.values.get("user_id")
    if session.get("is_login"):
        this_user_id = session.get("user").get("id")
    else:
        this_user_id = None

    user_id = user_id or this_user_id
    passage_service = PassageService()
    passage_list = passage_service.get_passage_list(user_id)

    return json.dumps(passage_list)




@app.route('/passage',methods=['GET'])
def fetch_passage():

    passage_id = request.values.get("id")
    passage_service = PassageService()
    passage = passage_service.get_passage(passage_id)
    if not passage:
        result = {}
        return json.dumps(result)
    else:
        result = {"fetch_success":True,"passage":{
            "id":passage.id,
            "title":passage.title,
            "content":passage.content,
            "user_id":passage.user_id
        }}
        return json.dumps(result)

@app.route('/passage',methods=['PUT'])
def update_passage():
    passage_id = request.json.get("id")
    title = request.json.get("title");
    content = request.json.get("content");
    is_publish = request.json.get("is_publish")
    passage_service = PassageService()
    r = passage_service.update_passage(passage_id,title,content,is_publish)
    result = {"update_success":True,"message":"更新成功"}
    return json.dumps(result)


@app.route('/passage/<id>',methods=["DELETE"])
def delete_passage(id):
    passage_service = PassageService()
    passage_service.delete_passage(id)
    result= {"delete_success":True,"message":""}
    return json.dumps(result)


@app.route('/home/passagelist/',methods=["GET"])
def get_home_passages():
    passage_service = PassageService()
    passages = passage_service.get_published_passages()
    return json.dumps(passages)




if __name__=="__main__":
    app.run(port=3000)