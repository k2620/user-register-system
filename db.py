import pymysql
from config import DB_CONFIG

#1.定义连接数据库的函数
    # 功能：连接到MySQL数据库
    # 输入：无
    # 输出：数据库连接对象，如果失败返回None
def get_connection():
    try:
        conn=pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            charset="utf8mb4"
        )
        print("数据库链接成功！")
        return conn
    except Exception as e:
        print(f"链接数据库失败：{e}")
        return None
    
#单独测试这个函数
# if __name__=="__main__":
#     conn=get_connection()
#     if conn:
#         print("可以正常链接")
#         conn.close()
#     else:
#         print("连接失败，检查配置")

#2.写查询函数
    # 功能：执行查询语句（SELECT）
    # 输入：sql语句，参数（可选）
    # 输出：查询结果列表，失败返回None
#sql参数（我要执行的sql语句），params=None参数，防止sql注入
def execute_query(sql,params=None):
    #初始化，声明变量，先设置为None,后面才能判断是否链接成功/游标是否存在
    conn=None
    cursor=None  #游标
    try:
        #1.连接数据库
        conn=get_connection()
        if not conn:
            return None    #如果连接失败的话就返回None
        #2.创建游标(游标用于执行sql和获取结果)
        cursor=conn.cursor()
        #3.执行sql
        cursor.execute(sql,params or ())
        #4.获取结果
        result=cursor.fetchall()   #获取所有查询结果，fetchone()取一条结果
        print(f"查询到{len(result)}条记录")

        return result  #把查到的数据返回给调用者
    except Exception as e:
        print(f"查询失败：{e}")
        return None
    finally:
        #5.关闭链接(无论如何都要执行)
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("连接已关闭")
#测试查询函数
# if __name__=="__main__":
#     #测试查询
#     sql='select * from users'
#     result=execute_query(sql)
#     print("查询结果",result)

#写插入函数
    # 功能：执行插入语句（INSERT）
    # 输入：sql语句，参数
    # 输出：新记录的ID，失败返回None
def execute_insert(sql,params=True):
    #初始化
    conn=None
    cursor=None

    try:
        #1.连接数据库
        conn =get_connection()
        if not conn:
            return None
        #2.创建游标
        cursor=conn.cursor()
        #3.执行插入
        cursor.execute(sql,params or ())
        #4.提交事务(重要)，这个是insert必须有的，不提交不会真正写入数据库
        conn.commit()
        #5.获取新插入的ID
        new_id=cursor.lastrowid   #获取刚插入记录的自增ID
        print(f"插入成功，新ID：{new_id}")
        return new_id   #把新id返回给调用者
    #回滚部分（错误处理）
    except Exception as e:
        #6.如果出错，回滚事务
        if conn:
            conn.rollback()   #撤销之前的操作
        print(f"插入失败：{e}")
        return None
    #关闭链接
    finally:
        #7.关闭链接
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("连接已关闭")
#测试插入函数
# if __name__=="__main__":
#     sql="INSERT INTO users (name,password) VALUES(%s,%s)"
#     user_id=execute_insert(sql,("测试用户",'123456'))
#     if user_id:
#         print(f"用户创建成功，ID：{user_id}")

    
    

    
