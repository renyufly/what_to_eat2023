import sqlite3


class user_con:
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

    def register(self, name: str, key: str) -> bool:
        self.cur.execute("SELECT * FROM data WHERE name==?", (name,))
        res = self.cur.fetchall()
        if not res:
            self.cur.execute("INSERT INTO data VALUES(?,?)", (name, key))
            self.con.commit()
            return True
        else:
            return False

    def login(self, name: str, key: str) -> bool:
        self.cur.execute("SELECT * FROM data WHERE name==? AND key==?", (name, key))
        res = self.cur.fetchall()
        if not res:
            return False
        else:
            return True


'''        
#testcase        
con=user_con("data.db")
while True:
    tmp=input().split()
    if len(tmp)==1:
        if tmp.pop()!="-1":
            print("WRONG OPERATION!")
        break
    
    op,name,key=tmp
    op=int(op)
    if op==1:
        print(con.register(name,key))
    elif op==2:
        print(con.login(name,key))
    else:
        print("WRONG OPERATION!")
        break    
con.printall()
con.end()'''
