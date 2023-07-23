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
        FOREIGN KEY (counter_id) REFERENCES food_counter (id) ON DELETE CASCADE);
        ''')  # 食堂柜台的菜品表——dishes

        '''初始化时就预先添加好各菜品'''
        self.cur.execute("SELECT COUNT(*) FROM dishes")
        count = self.cur.fetchone()[0]
        if count <= 0:
            self.initial_add_dished()

    def initial_add_dished(self):
        '''初始化时向表中添加菜品'''
        cafeterias = [
            ('学一食堂'),
            ('学二食堂'),
            ('学五食堂'),

        ]

        for item in cafeterias:
            self.cur.execute('''
            INSERT INTO cafeteria(name) VALUES (?)
            ''', (item,))

        self.con.commit()

        '''学一食堂'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', ('学一食堂',))
        cafe_id = self.cur.fetchone()[0]
        counters = [
            ('一柜台', cafe_id),
            ('二柜台', cafe_id),
            ('三柜台', cafe_id),
            ('四柜台', cafe_id),
        ]
        for item in counters:
            self.cur.execute('''
                    INSERT INTO food_counter(name, cafeteria_id) VALUES (?, ?)
                    ''', item)
        self.con.commit()
        '''一柜台  (每个柜台10道菜)'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '一柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('牛肉卤粉', counter_id),
            ('饺子', counter_id),
            ('鸡肉米粉', counter_id),
            ('麻辣烫', counter_id),
            ('尖椒炒蛋', counter_id),
            ('蒜蓉生菜', counter_id),
            ('宫保鸡丁', counter_id),
            ('麻辣拌面', counter_id),
            ('肉末蛋包饭', counter_id),
            ('土豆炖牛肉', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
            INSERT INTO dishes(name, counter_id) VALUES (?, ?)
            ''', item)

        self.con.commit()
        '''二柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '二柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('麻辣鱼片', counter_id),
            ('清炒花菜', counter_id),
            ('红烧鸭块', counter_id),
            ('胡辣汤', counter_id),
            ('西红柿牛腩', counter_id),
            ('炒绿豆芽', counter_id),
            ('小白菜炒木耳', counter_id),
            ('西红柿炒鸡蛋', counter_id),
            ('蒸玉米', counter_id),
            ('清炖鸡肉', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                    INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                    ''', item)

        self.con.commit()
        '''三柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '三柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('红烧丸子', counter_id),
            ('酱肉馅饼', counter_id),
            ('炸鸡排', counter_id),
            ('木耳炒青菜', counter_id),
            ('青菜木耳烩肉', counter_id),
            ('清炒白菜', counter_id),
            ('干煸豆角土豆条', counter_id),
            ('糖醋肉', counter_id),
            ('韭菜鸡蛋馅饼', counter_id),
            ('圆白菜炒面', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                            INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                            ''', item)

        self.con.commit()
        '''四柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '四柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('豆角红烧肉', counter_id),
            ('豆角炒面', counter_id),
            ('烧排骨', counter_id),
            ('麻辣一锅鲜', counter_id),
            ('东北肉卷', counter_id),
            ('酱爆鸡丁', counter_id),
            ('飘香鸡蛋', counter_id),
            ('川椒肉排', counter_id),
            ('重庆卤粉', counter_id),
            ('脆皮五花', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                                    INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                                    ''', item)

        self.con.commit()

        '''学二食堂'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', ('学二食堂',))
        cafe_id = self.cur.fetchone()[0]
        counters = [
            ('一柜台', cafe_id),
            ('二柜台', cafe_id),
            ('三柜台', cafe_id),
            ('四柜台', cafe_id),
            ('五柜台', cafe_id),
        ]
        for item in counters:
            self.cur.execute('''
                            INSERT INTO food_counter(name, cafeteria_id) VALUES (?, ?)
                            ''', item)
        self.con.commit()
        '''一柜台  (每个柜台10道菜)'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '一柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('麻辣香锅', counter_id),
            ('宫保鸡丁', counter_id),
            ('卤肉饭套餐', counter_id),
            ('五谷豆浆', counter_id),
            ('土豆牛肉', counter_id),
            ('风味烤鸡腿', counter_id),
            ('饺子', counter_id),
            ('口水鸡', counter_id),
            ('鱼香肉丝', counter_id),
            ('豆角烧茄子', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                    INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                    ''', item)

        self.con.commit()
        '''二柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '二柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('葱香鸡蛋饼', counter_id),
            ('茴香肉馅饼', counter_id),
            ('西红柿炒鸡蛋', counter_id),
            ('红烧腐竹', counter_id),
            ('千叶豆腐', counter_id),
            ('红烧排骨', counter_id),
            ('牛肉面', counter_id),
            ('炒花菜', counter_id),
            ('青椒炒鸡蛋', counter_id),
            ('红烧丸子', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                            INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                            ''', item)

        self.con.commit()
        '''三柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '三柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('红烧茄子', counter_id),
            ('香煎玉米饼', counter_id),
            ('香辣渔粉', counter_id),
            ('梅菜扣肉', counter_id),
            ('炒豆芽', counter_id),
            ('韭菜炒鸡蛋', counter_id),
            ('红烧香菇', counter_id),
            ('红烧带鱼', counter_id),
            ('胡萝卜炖牛肉', counter_id),
            ('青瓜炒鸡蛋', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                                    INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                                    ''', item)

        self.con.commit()
        '''四柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '四柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('红烧鱼块', counter_id),
            ('韭菜干丝', counter_id),
            ('锅包肉', counter_id),
            ('白菜油豆腐', counter_id),
            ('蒸蛋', counter_id),
            ('炒生菜', counter_id),
            ('炒青菜', counter_id),
            ('西红柿炒茄子', counter_id),
            ('菠萝炒粉丝', counter_id),
            ('炒白萝卜丝', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                                            INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                                            ''', item)

        self.con.commit()
        '''五柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '五柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('豆角炒肉', counter_id),
            ('麻辣烫', counter_id),
            ('石锅拌饭', counter_id),
            ('糯米排骨', counter_id),
            ('刀削面', counter_id),
            ('小酥肉', counter_id),
            ('杭椒牛柳', counter_id),
            ('丸子白菜汤', counter_id),
            ('土豆鸡块', counter_id),
            ('炒莴苣', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                                                    INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                                                    ''', item)

        self.con.commit()

        '''学五食堂'''
        self.cur.execute('''SELECT id FROM cafeteria WHERE name = ?''', ('学五食堂',))
        cafe_id = self.cur.fetchone()[0]
        counters = [
            ('一柜台', cafe_id),
            ('二柜台', cafe_id),
            ('三柜台', cafe_id),
        ]
        for item in counters:
            self.cur.execute('''
                                   INSERT INTO food_counter(name, cafeteria_id) VALUES (?, ?)
                                   ''', item)
        self.con.commit()
        '''一柜台  (每个柜台10道菜)'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '一柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('红烧肉', counter_id),
            ('鱼粉', counter_id),
            ('麻辣香锅', counter_id),
            ('烧茄子', counter_id),
            ('口水鸡', counter_id),
            ('清炒圆白菜', counter_id),
            ('萝卜炖牛肉', counter_id),
            ('排骨玉米汤', counter_id),
            ('猪脚汤', counter_id),
            ('番茄牛腩汤', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                           INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                           ''', item)

        self.con.commit()
        '''二柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '二柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('肉炒圆白菜', counter_id),
            ('溜丸子', counter_id),
            ('西红柿炒鸡蛋', counter_id),
            ('韭黄炒鸡蛋', counter_id),
            ('鱼头豆腐汤', counter_id),
            ('炒面', counter_id),
            ('豇杂面', counter_id),
            ('红烧鱼套餐', counter_id),
            ('酱大骨套餐', counter_id),
            ('酱爆鸡丁', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                                   INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                                   ''', item)

        self.con.commit()
        '''三柜台'''
        self.cur.execute("SELECT id FROM food_counter WHERE cafeteria_id = ? AND name = ?", (cafe_id, '三柜台'))
        counter_id = self.cur.fetchone()[0]
        one_dishes = [
            ('外婆肘子', counter_id),
            ('紫米发糕', counter_id),
            ('酸菜鱼', counter_id),
            ('咖喱鸡块饭', counter_id),
            ('干锅烤肉饭', counter_id),
            ('糖醋排骨', counter_id),
            ('韩式牛肉铁板饭', counter_id),
            ('蚕豆烧牛肉', counter_id),
            ('五花肉烤肉饭', counter_id),
            ('木须肉', counter_id),
        ]
        for item in one_dishes:
            self.cur.execute('''
                                           INSERT INTO dishes(name, counter_id) VALUES (?, ?)
                                           ''', item)

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


# testcase
con = dining_user_con("diningData.db")
# con.printAll()
'''
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

# con.printAll()
# con.end()

# clearAllData
'''
con=dining_user_con("diningData.db")
con.execute("DELETE FROM cafeteria")
con.execute("DELETE FROM food_counter")
con.execute("DELETE FROM dishes")
con.commit()
con.end
'''
