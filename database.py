import sqlite3


class user_con:
    key_maxlen = 32
    key_minlen = 6  # 新增了对密码长度的检测

    def __init__(self, database: str) -> None:
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS data(name TEXT, key TEXT)")

    def end(self):
        self.cur.close()
        self.con.close()

    def printall(self):
        self.cur.execute("SELECT * FROM data ")
        for item in self.cur:
            print(item)

    def print_messages(self, name: str):
        self.cur.execute("SELECT * FROM " + name)
        for item in self.cur:
            print(item)

    def register(self, name: str, key: str) -> int:
        if len(key) < self.key_minlen or len(key) > self.key_maxlen:
            return 1  # key_length out of range
        self.cur.execute("SELECT * FROM data WHERE name==?", (name,))
        res = self.cur.fetchall()
        if not res:
            self.cur.execute("INSERT INTO data VALUES(?,?)", (name, key))
            self.cur.execute("CREATE TABLE " + name + "(sender TEXT,messages TEXT,time TEXT)")
            self.con.commit()
            return 0  # sucess
        else:
            return 2  # repeated name

    def login(self, name: str, key: str) -> bool:
        if len(key) < self.key_minlen or len(key) > self.key_maxlen:
            return False
        self.cur.execute("SELECT * FROM data WHERE name==? AND key==?", (name, key))
        res = self.cur.fetchall()
        if not res:
            return False
        else:
            return True

    '''
    修改密码功能
    对密码长度进行检测，当不在长度范围内的时候会返回False
    '''

    def revise_key(self, name: str, key: str) -> bool:
        if len(key) < self.key_minlen or len(key) > self.key_maxlen:
            return False  # key length out of range
        self.cur.execute("UPDATE data SET key=? WHERE name==?", (key, name))
        self.con.commit()
        return True

    '''
    提供参数分别为发送者，接收者，信息，时间
    当发送者或接收者不存在时会返回False
    '''

    def send_messages(self, sender: str, receiver: str, message: str, time: str) -> bool:
        self.cur.execute("SELECT * FROM data WHERE name==?", (sender,))
        res = self.cur.fetchall()
        if not res:
            return False
        self.cur.execute("SELECT * FROM data WHERE name==?", (receiver,))
        res = self.cur.fetchall()
        if not res:
            return False
        self.cur.execute("INSERT INTO " + receiver + "(sender,messages,time) VALUES(?,?,?)", (sender, message, time))
        self.con.commit()
        return True

    '''
    提供用户名，返回（发送者，信息，时间）元组组成的列表
    返回最近的100条消息
    '''

    def get_messages(self, name: str) -> list:
        self.cur.execute("SELECT * FROM " + name)
        res = self.cur.fetchall()
        return res[-1:-101:-1]

    '''
    提供评论者，菜，评价，时间四个参数
    当返回值为False时代表用户不存在
    '''

    def comment_dish(self, user: str, dish: str, comment: str, time: str) -> bool:
        self.cur.execute("SELECT * FROM data WHERE name==?", (user,))
        res = self.cur.fetchall()
        if not res:
            return False
        self.cur.execute("CREATE TABLE IF NOT EXISTS " + dish + "(commenter TEXT ,comment TEXT,time TEXT)")
        self.cur.execute("INSERT INTO " + dish + "(commenter,comment,time) VALUES(?,?,?)", (user, comment, time))
        self.con.commit()
        return True

    '''
    提供菜品名称,保证该菜品名称正确，返回评论信息组成的列表
    品论信息组成为一个元组 (user,comment,time)
    '''

    def get_comment(self, dish: str) -> list:
        self.cur.execute("SELECT * FROM " + dish)
        res = self.cur.fetchall()
        return res


'''
# testcase
con = user_con("data.db")
while True:
    tmp = input().split()
    if len(tmp) == 1:
        op = tmp.pop()
        if op == "0":
            con.printall()
        elif op == "-1":
            break
        else:
            print("WRONG OPERATION!")
    elif len(tmp) == 2:
        op = tmp.pop(0)
        if op == "-2":
            con.print_messages(tmp.pop())
        elif op == "6":
            print(con.get_comment(tmp.pop()))
        else:
            print("WRONG OPERATION!")
    elif len(tmp) == 3:
        op, name, key = tmp
        op = int(op)
        if op == 1:
            print(con.register(name, key))
        elif op == 2:
            print(con.login(name, key))
        elif op == 3:
            print(con.revise_key(name, key))
        else:
            print("WRONG OPERATION!")

    elif len(tmp) == 5:
        op, sender, receiver, message, time = tmp
        op = int(op)
        if op == 4:
            con.send_messages(sender, receiver, message, time)
            print(con.get_messages(receiver))
        elif op == 5:
            con.comment_dish(sender, receiver, message, time)
        else:
            print("WRONG OPERATION!")
con.end()
'''
