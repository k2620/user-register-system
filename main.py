from flask import Flask,request,jsonify,render_template
from db import execute_query,execute_insert    #导入数据库函数
#导入密码加密相关包
from werkzeug.security import generate_password_hash,check_password_hash
import re    #正则校验包
   
app=Flask(__name__)


@app.route("/")
def index():
    return render_template("register1.html")


#登入验证业务api
@app.route("/api/register",methods=["POST"])
def register():
    #1、获取前端提交的数据
    data=request.get_json()
    name=data.get("name","").strip()   #去掉用户名前后的空格
    password=data.get("password","").strip()
    confirm_password=data.get("confirm_password","").strip()

    #2.验证非空
    if not name or not password or not confirm_password:
        return jsonify({
            'code':400,'msg':"用户名和密码不能为空"
        }),400    #添加状态码
    
    #3.校验密码长度
    if len(password) < 6:
        return jsonify({'code':400,'msg':"密码的长度只是6位数字"}),400
    
    #验证两次密码是否一致
    if password !=confirm_password:
        return jsonify({'code':400,'msg':"两次密码输入不一致"}),400
    
    #调用验证密码强度的函数
    strength_result=check_password_strength(password)
    if not strength_result['isValid']:
        return jsonify({'code':400,'msg':strength_result['message']}),400
    
    #4.用户名格式验证
    if not re.match("^[a-zA-Z0-9_\u4e00-\u9fa5]{2,10}$",name):
        return jsonify({'code':400,'msg':"用户名只能包含大、小写字母，数字、下划线、中文，2-10位数"}),400
    
    
    #5.检查用户名是否已经存在
    check_sql="SELECT id FROM users WHERE name=%s"
    existing_users=execute_query(check_sql,(name,))

    if existing_users:         #如果为True，表示用户名已经存在
        return jsonify({
            'code':409,         #409表示冲突
            'msg':"用户名已经存在，请换一个用户名",
        }),409
    
    #6.密码加密
    hashed_password=generate_password_hash(password)  #把明文密码变成乱码
    print(f"原始密码：{password}")  
    print(f"加密后：{hashed_password}")

    #7.业务逻辑，插入新用户到数据库,并存入加密后的密码
    insert_sql="INSERT INTO users (name,password) VALUES(%s,%s)"
    new_id=execute_insert(insert_sql,(name,hashed_password))

    if new_id:    #为True创建成功
        return jsonify({
            'code':200,
            'msg':"用户注册成功",
            'data':{
                'id':new_id,
                "name":name
                #不能返回密码
            }
        }),200
    else:
        return jsonify({
            'code':500,
            'msg':"注册失败，数据库错误"
        }),500
    
    #密码强度验证函数
    # 验证密码强度
    # 要求：至少包含 大写字母、小写字母、数字、特殊字符 中的3种
def check_password_strength(password):
    has_upper=bool(re.search(r'[A-Z]',password))  #有大写字母
    has_lower=bool(re.search(r'[a-z]',password))  #有小写字母
    has_digit=bool(re.search(r'\d',password))    #有数字
    has_special=bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]',password)) #有特殊字符

    #计算满足条件数量
    strength_count=sum([has_upper,has_lower,has_digit,has_special])

    print(f"密码强度检测：大写={has_upper}, 小写={has_lower}, 数字={has_digit}, 特殊={has_special}, 得分={strength_count}")

    if strength_count < 3:
        return {
                'isValid':False,
                'message': '密码强度太弱！必须包含大写字母、小写字母、数字、特殊字符中的至少3种'
        }
    return {
            'isValid':True,
            'message':'密码强度合格'
    }
              


    
    #业务逻辑，添加新用户
    # new_id=len(user) + 1
    # new_user={
    #     "id":new_id,
    #     "name":name,
    #     "password":password
    # }
    # user.append(new_user)

    # #返回数据
    # return jsonify({
    #     'code':200,
    #     'msg':"用户注册成功",
    #     "data":new_user,
    # })
    

if __name__=="__main__":
    app.run(debug=True,port=5050)