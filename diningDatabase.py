''' 食堂菜品数据库操作'''
import sqlite3


class dining_user_con:

    def __init__(self, database: str) -> None:
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

        self.cur.execute('''PRAGMA foreign_keys=ON;''')  # SQLite默认外键是关闭的，需要在连接数据库后打开

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS cafeteria(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL);''')  # 食堂表——cafeteria

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS food_counter(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        cafeteria_id INTEGER NOT NULL,
        FOREIGN KEY (cafeteria_id) REFERENCES cafeteria (id) ON DELETE CASCADE) ;
        ''')  # 食堂柜台表——food_counter

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS dishes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        counter_id INTEGER NOT NULL,
        number INTEGER NOT NULL,
        FOREIGN KEY (counter_id) REFERENCES food_counter (id) ON DELETE CASCADE);
        ''')  # 食堂柜台的菜品表——dishes

        '''初始化时就预先添加好各菜品'''
        self.cur.execute("SELECT COUNT(*) FROM dishes")
        count = self.cur.fetchone()[0]
        if count <= 0:
            self.initial_add_dished()

    def initial_add_dished(self):
        '''初始化时通过读入外部文件向表中添加菜品'''
        '''学一食堂 一柜台 饺子'''
        with open('data_initial.txt', 'r', encoding='utf-8') as file:
            for line in file:
                cafename, countername, dishname = line.strip().split(' ')
                self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
                cafe_id = self.cur.fetchall()
                if cafe_id:
                    pass
                else:
                    self.cur.execute('''INSERT INTO cafeteria(name) VALUES (?)''', (cafename,))
                    self.con.commit()
                    self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
                    cafe_id = self.cur.fetchall()

                self.cur.execute('''SELECT id FROM food_counter WHERE name = ? AND cafeteria_id = ?''',
                                 (countername, cafe_id[0][0]))
                counter_id = self.cur.fetchall()
                if counter_id:
                    pass
                else:
                    self.cur.execute('''INSERT INTO food_counter(name, cafeteria_id) VALUES(?,?)''',
                                     (countername, cafe_id[0][0]))
                    self.con.commit()
                    self.cur.execute('''SELECT id FROM food_counter WHERE name = ? AND cafeteria_id = ?''',
                                     (countername, cafe_id[0][0]))
                    counter_id = self.cur.fetchall()

                self.cur.execute('''INSERT INTO dishes(name, counter_id, number) VALUES(?,?,?)''',
                                 (dishname, counter_id[0][0], 0))
                self.con.commit()

    def end(self):
        self.cur.close()
        self.con.close()

    def printAll(self):
        '''打印所有表的信息——测试用'''
        self.cur.execute("SELECT * FROM cafeteria ")
        for item in self.cur:
            print(item)
        self.cur.execute("SELECT * FROM food_counter ")
        for item in self.cur:
            print(item)
        self.cur.execute("SELECT * FROM dishes ")
        for item in self.cur:
            print(item)

    ''' ——————————————读 取 操 作————————————————'''

    def showAllCafeName(self) -> list:
        '''展示所有食堂名字'''
        self.cur.execute('''SELECT name FROM cafeteria ''')
        nameTuple = self.cur.fetchall()
        ret = []
        for item in nameTuple:
            ret.append(item[0])
        return ret

        '''返回结果：['学一食堂', '学二食堂', '学五食堂']'''

    def showCafeAllCounterName(self, cafename: str) -> list:
        '''根据食堂名字展示对应所有柜台名字'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT name FROM food_counter WHERE cafeteria_id = ?''', cafe_id)
        counterName = self.cur.fetchall()
        ret = []
        for item in counterName:
            ret.append(item[0])
        return ret

        '''返回结果：['一柜台', '二柜台', '三柜台', '四柜台']'''

    def showCounterAllDish(self, cafename: str, countername: str) -> list:
        '''根据食堂及柜台名字展示对应所有菜名'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT * FROM dishes WHERE counter_id = ?''', counter_id)
        dish = self.cur.fetchall()
        ret = []
        for item in dish:
            ret.append(item[1])
        return ret

        '''返回结果：['麻辣香锅', '宫保鸡丁', '卤肉饭套餐']'''

    def showOneDish(self, cafename: str, countername: str, dishname: str) -> list:
        '''根据食堂、柜台、菜名返回指定的一道菜的信息'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT * FROM dishes WHERE counter_id = ? AND name = ?''', (counter_id[0], dishname))
        dish = self.cur.fetchall()
        return dish

        '''返回结果：[(41, '麻辣香锅', 5)]'''

    '''————————————————更 新 操 作————————————————————————————————'''

    def updateCafeName(self, cafename: str, newname: str):
        '''更新食堂名字（其他关联信息不变）'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('UPDATE cafeteria SET name = ? WHERE id = ?', (newname, cafe_id[0]))
        self.con.commit()

    def updateCounterName(self, cafename: str, countername: str, newname: str):
        '''更新柜台名字（其他关联信息不变）'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('UPDATE food_counter SET name = ? WHERE id = ?', (newname, counter_id[0]))
        self.con.commit()

    def updateDishName(self, cafename: str, countername: str, dishname: str, newname: str):
        '''更新菜名(其他关联信息不变)'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM dishes WHERE counter_id = ? AND name = ?''', (counter_id[0], dishname))
        dish_id = self.cur.fetchall()[0]
        self.cur.execute('''UPDATE dishes SET name = ? WHERE id = ?''', (newname, dish_id[0]))
        self.con.commit()

    '''————————————————删 除 操 作————————————————————————————————————————'''

    def deleteCafe(self, cafename: str):
        '''删除某个食堂（关联信息如柜台及菜品一并删除）'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('DELETE FROM cafeteria WHERE id = ?', (cafe_id[0],))
        self.con.commit()

    def deleteCounter(self, cafename: str, countername: str):
        '''删除某柜台（级联删除）'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('DELETE FROM food_counter WHERE id = ?', (counter_id[0],))
        self.con.commit()

    def deleteDish(self, cafename: str, countername: str, dishname: str):
        '''删除某菜品（级联删除）'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM dishes WHERE counter_id = ? AND name = ?''', (counter_id[0], dishname))
        dish_id = self.cur.fetchall()[0]
        self.cur.execute('DELETE FROM dishes WHERE id = ?', (dish_id[0],))
        self.con.commit()

    '''————————————————创建 / 新增 操 作——————————————————————————————————————————'''

    def insertCafe(self, cafename: str):
        '''向表中新增食堂'''
        self.cur.execute('''
        INSERT INTO cafeteria(name) VALUES (?)
        ''', (cafename,))
        self.con.commit()

    def insertCounter(self, cafename: str, countername: str):
        '''向表中根据食堂名cafename新增柜台'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''
        INSERT INTO food_counter(name, cafeteria_id) VALUES (?, ?)
        ''', (countername, cafe_id[0]))
        self.con.commit()

    def insertDish(self, cafename: str, countername: str, dishname: str):
        '''根据食堂名、柜台名新增菜品'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('''
        INSERT INTO dishes(name, counter_id) VALUES (?, ?)
        ''', (dishname, counter_id[0]))
        self.con.commit()

    '''—————————————————必吃排行榜相关—————————————————————————————————————————————————'''

    def increaseNumber(self, cafename: str, countername: str, dishname: str):
        '''用户吃过菜品后为次数+1（前端GUI不用调用！在addDish里即自动执行）'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', (cafename,))
        cafe_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?''',
                         (cafe_id[0], countername))
        counter_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT id FROM dishes WHERE counter_id = ? AND name = ?''', (counter_id[0], dishname))
        dish_id = self.cur.fetchall()[0]
        self.cur.execute('''SELECT number FROM dishes WHERE id = ?''', (dish_id[0],))
        num = self.cur.fetchall()[0][0]
        num = num + 1
        self.cur.execute('''UPDATE dishes SET number = ? WHERE id = ?''', (num, dish_id[0]))
        self.con.commit()

    def showAllDishRankingList(self):
        '''菜品排行榜展示所有——菜名 柜台名 食堂名'''
        self.cur.execute('''SELECT * FROM dishes''')
        ret_list = self.cur.fetchall()
        sorted_list = sorted(ret_list, key=lambda x: x[3], reverse=True)
        ret = []
        for item in sorted_list:
            self.cur.execute('''SELECT name, cafeteria_id FROM food_counter WHERE id = ?''', (item[2],))
            countername, cafe_id = self.cur.fetchall()[0]
            self.cur.execute('''SELECT name FROM cafeteria WHERE id = ?''', (cafe_id,))
            cafename = self.cur.fetchall()[0]
            ret.append(item[1] + " " + countername + " " + cafename[0])
        return ret

    def showTop50DishRankingList(self):
        '''菜品排行榜展示前50——菜名 柜台名 食堂名'''
        self.cur.execute('''SELECT * FROM dishes''')
        ret_list = self.cur.fetchall()
        sorted_list = sorted(ret_list, key=lambda x: x[3], reverse=True)
        cnt = 0
        ret = []
        for item in sorted_list:
            cnt += 1
            self.cur.execute('''SELECT name, cafeteria_id FROM food_counter WHERE id = ?''', (item[2],))
            countername, cafe_id = self.cur.fetchall()[0]
            self.cur.execute('''SELECT name FROM cafeteria WHERE id = ?''', (cafe_id,))
            cafename = self.cur.fetchall()[0]
            ret.append(item[1] + " " + countername + " " + cafename[0])
            if cnt == 50:
                break
        return ret


'''# testcase
con = dining_user_con("diningData.db")
con.printAll()
# print(con.showAllDishRankingList())
con.end()

print(con.showAllCafeName())
print(con.showCafeAllCounterName('学一食堂'))
print(con.showCounterAllDish('学二食堂', '一柜台')[0])
print(con.showCounterAllDish('学二食堂', '一柜台'))
print(con.showOneDish('学二食堂', '一柜台', '麻辣香锅'))
con.end()
'''

'''con.insertCafe('学六食堂')
con.insertCounter('学六食堂', '抽象柜台')
con.insertDish('学六食堂', '抽象柜台', '泔水')'''

# con.updateCafeName('学一食堂', '沙河东区食堂')
# con.updateCounterName('沙河东区食堂', '一柜台', '6324柜台')
# con.updateDishName('沙河东区食堂','6324柜台','饺子','草莓米线')
# con.deleteDish('学六食堂', '抽象柜台', '泔水')

'''con.printAll()
con.end()'''
