'''用户记录菜品数据库操作'''
import sqlite3


class user_record_con():

    def __init__(self, databasename: str) -> None:
        """连接用户信息数据库"""
        self.con = sqlite3.connect(databasename)
        self.cur = self.con.cursor()

        self.cur.execute('''PRAGMA foreign_keys=ON;''')  # SQLite默认外键是关闭的，需要在连接数据库后打开

    def print(self, username):
        '''仅做测试用函数'''
        username = 'user_' + username
        print_sql = f"SELECT * FROM {username} "
        self.cur.execute(print_sql)
        contents = self.cur.fetchall()
        for item in contents:
            print(item)

    def end(self):
        '''关闭数据库连接'''
        self.cur.close()
        self.con.close()

    '''———————————————用户注册时必须执行的操作 ↓ ———————————————————————————————————————'''

    def createUserTable(self, username: str, ):
        '''创建用户记录菜品表
        在进行用户注册的同时就执行'''
        username = 'user_' + username
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {username} (id INTEGER PRIMARY KEY AUTOINCREMENT,dishname TEXT NOT NULL,countername TEXT NOT NULL,cafename TEXT NOT NULL,timestamp TEXT NOT NULL)"
        self.cur.execute(create_table_sql)  # 菜名, 柜台名,食堂名,时间戳

    def createUserStar(self, username: str):
        '''创建用户添加书签表
        在进行用户注册的同时就执行'''
        username = 'userStar_' + username
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {username} (id INTEGER PRIMARY KEY AUTOINCREMENT,dishname TEXT,countername TEXT,cafename TEXT)"
        self.cur.execute(create_table_sql)  # 菜名, 柜台名,食堂名

    '''——————————————————添加、删除、展示用户吃过的菜记录 ↓——————————————————————————————————————————————————————————————————'''

    def addDish(self, username: str, dishname: str, countername: str, cafename: str, timestamp: str):
        '''添加吃过的菜
        参数介绍：dishname-菜名，countername-柜台名，cafename-食堂名，timestamp-时间戳-形如'2023-07-21'    '''
        username = 'user_' + username
        '''如果重复，则只更新时间戳'''
        sel_cafe_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername = ? AND dishname = ?"
        self.cur.execute(sel_cafe_sql, (cafename, countername, dishname))
        dish_id = self.cur.fetchall()
        if dish_id:
            update_sql = f"UPDATE {username} SET timestamp = ? WHERE id = ?"
            self.cur.execute(update_sql, (timestamp, dish_id[0][0]))
            self.con.commit()
        else:
            add_table_dish_sql = f"INSERT INTO {username}(dishname,countername,cafename,timestamp) VALUES(?,?,?,?)"
            self.cur.execute(add_table_dish_sql, (dishname, countername, cafename, timestamp))
            self.con.commit()

    def deleteDish(self, username: str, dishname: str, countername: str, cafename: str):
        '''删除吃过的菜的记录'''
        username = 'user_' + username
        sel_cafe_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername = ? AND dishname = ?"
        self.cur.execute(sel_cafe_sql, (cafename, countername, dishname))
        dish_id = self.cur.fetchall()[0]
        del_sql = f"DELETE FROM {username} WHERE id = ?"
        self.cur.execute(del_sql, (dish_id[0],))
        self.con.commit()

    def showAllDishName(self, username: str) -> list:
        '''展示用户吃过的所有菜名记录（仅展示菜的名字）'''
        username = 'user_' + username
        show_sql = f"SELECT dishname FROM {username}"
        self.cur.execute(show_sql)
        nameTuple = self.cur.fetchall()
        ret = []
        for item in nameTuple:
            ret.append(item[0])
        return ret
        # 返回结果：['饺子', '面条', '豆腐']

    # ————————————添加、删除、展示书签(收藏夹)操作 ↓——————————————————————————

    def addStarCafe(self, username: str, cafename: str) -> bool:
        '''为食堂添加书签'''
        username = 'userStar_' + username
        '''如果重复，就不添加'''
        sel_cafe_sql = f"SELECT id FROM {username} WHERE cafename = ?"
        self.cur.execute(sel_cafe_sql, (cafename,))
        dish_id = self.cur.fetchall()
        if dish_id:
            return False
        else:
            add_table_dish_sql = f"INSERT INTO {username}(cafename) VALUES(?)"
            self.cur.execute(add_table_dish_sql, (cafename,))
            self.con.commit()
            return True

    def addStarCounter(self, username: str, cafename: str, countername: str) -> bool:
        '''为柜台添加书签（需要提供食堂名）'''
        username = 'userStar_' + username
        '''如果重复，就不添加'''
        sel_cafe_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername = ?"
        self.cur.execute(sel_cafe_sql, (cafename, countername))
        dish_id = self.cur.fetchall()
        if dish_id:
            return False  # 重复会返回False
        else:
            add_table_dish_sql = f"INSERT INTO {username}(cafename, countername) VALUES(?, ?)"
            self.cur.execute(add_table_dish_sql, (cafename, countername))
            self.con.commit()
            return True

    def addStarDish(self, username: str, cafename: str, countername: str, dishname: str) -> bool:
        '''为菜品添加书签（需提供食堂名、柜台名）'''
        username = 'userStar_' + username
        '''如果重复，就不添加'''
        sel_cafe_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername = ? AND dishname = ?"
        self.cur.execute(sel_cafe_sql, (cafename, countername, dishname))
        dish_id = self.cur.fetchall()
        if dish_id:
            return False
        else:
            add_table_dish_sql = f"INSERT INTO {username}(cafename, countername, dishname) VALUES(?, ?, ?)"
            self.cur.execute(add_table_dish_sql, (cafename, countername, dishname))
            self.con.commit()
            return True

    def deleteStar(self, username: str, record: str):
        '''删除某项书签
        传入参数：username-用户名， record-界面显示的书签内容：如显示"学六食堂 一柜台" 就把该字符串全传进来'''
        username = 'userStar_' + username
        recordSlice = record.split(' ')
        if len(recordSlice) == 1:  # 仅有食堂名
            sel_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername is NULL AND dishname is NULL"
            self.cur.execute(sel_sql, (recordSlice[0],))
            del_id = self.cur.fetchall()[0]
            del_sql = f"DELETE FROM {username} WHERE id = ?"
            self.cur.execute(del_sql, (del_id[0],))
            self.con.commit()
        elif len(recordSlice) == 2:  # 仅有食堂名&柜台名
            sel_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername = ? AND dishname is NULL"
            self.cur.execute(sel_sql, (recordSlice[0], recordSlice[1]))
            del_id = self.cur.fetchall()[0]
            del_sql = f"DELETE FROM {username} WHERE id = ?"
            self.cur.execute(del_sql, (del_id[0],))
            self.con.commit()
        else:
            sel_sql = f"SELECT id FROM {username} WHERE cafename = ? AND countername = ? AND dishname = ?"
            self.cur.execute(sel_sql, (recordSlice[0], recordSlice[1], recordSlice[2]))
            del_id = self.cur.fetchall()[0]
            del_sql = f"DELETE FROM {username} WHERE id = ?"
            self.cur.execute(del_sql, (del_id[0],))
            self.con.commit()

    def showStarAllCafe(self, username: str):
        '''展示当前用户书签的所有食堂名'''
        username = 'userStar_' + username
        show_sql = f"SELECT * FROM {username}"
        self.cur.execute(show_sql)
        nameList = self.cur.fetchall()
        ret = []
        for itemTuple in nameList:
            if itemTuple[1] == None and itemTuple[2] == None:
                ret.append(itemTuple[3])  # [3]是食堂名, [2]是柜台名, [1]是菜名
        return ret
        # 返回结果：['学七食堂']

    def showStarAllCounter(self, username: str):
        '''展示当前用户书签的所有柜台名'''
        username = 'userStar_' + username
        show_sql = f"SELECT * FROM {username}"
        self.cur.execute(show_sql)
        nameList = self.cur.fetchall()
        ret = []
        for itemTuple in nameList:
            if itemTuple[1] == None and itemTuple[2] != None:
                ret.append(itemTuple[3] + " " + itemTuple[2])
        return ret
        # 返回结果：['学八食堂 六柜台']

    def showStarAllDish(self, username: str):
        '''展示当前用户书签的所有菜名'''
        username = 'userStar_' + username
        show_sql = f"SELECT * FROM {username}"
        self.cur.execute(show_sql)
        nameList = self.cur.fetchall()
        ret = []
        for itemTuple in nameList:
            if itemTuple[1] != None and itemTuple[2] != None:
                ret.append(itemTuple[3] + " " + itemTuple[2] + " " + itemTuple[1])
        return ret
        # 返回结果：['学九食堂 九柜台 红烧茄子']



'''
con = user_record_con('userdata.db')
con.createUserTable('admin')
con.createUserStar('admin')'''
'''con.addDish('admin','饺子','6324柜台','学二食堂','2023-07-05')
con.addDish('admin','饺子3','4柜台','学一食堂','2023-07-02')
con.addDish('admin','饺子2','4柜台','学三食堂','2023-07-02')
con.deleteDish('admin','饺子','4柜台','学一食堂')
con.print('admin')
print(con.showAllDishName('admin'))'''
'''con.addStarCafe('admin','学七食堂')
con.addStarCounter('admin', '学七食堂', '六柜台')
con.addStarDish('admin', '学七食堂','酒柜台', '888')

#con.deleteStar('admin', '学七食堂')
print(con.showStarAllCafe('admin'))
print(con.showStarAllCounter('admin'))
print(con.showStarAllDish('admin'))
con.end()
'''
