from PyQt5.Qt import *
import sys
from diningDatabase import dining_user_con
from userRecordDatabase import user_record_con

diningCon = dining_user_con('diningData.db')
recordCon = user_record_con('userCon.db')


class MainWindow(QWidget):

    def __init__(self, usr: str):
        super(MainWindow, self).__init__()
        self.curUser = usr
        self.setWindowTitle('北航吃什么')
        self.resize(1500, 800)

        self.cafeLabel = QLabel('请选择目标食堂')
        self.cafeName = QComboBox(self)
        self.counterLabel = QLabel('请选择目标柜台')
        self.userLabel = QLabel('当前用户：' + usr)
        self.checkButton = QPushButton('确定')
        self.logoutButton = QPushButton('退出')
        self.counterName = QComboBox(self)
        self.dishes = Dishes()
        self.dishesArea = QScrollArea(self)

        self.cafeNameLayOut = QVBoxLayout()
        self.counterNameLayOut = QVBoxLayout()
        self.selectLayout = QHBoxLayout()
        self.userLayout = QHBoxLayout()
        self.selectAndUserLayout = QHBoxLayout()
        self.dishesAreaLayout = QHBoxLayout()
        self.allLayout = QVBoxLayout()

        self.cafe_and_counter_init()
        self.button_init()
        self.layout_init()

    def cafe_and_counter_init(self):
        self.cafeName.addItems(diningCon.showAllCafeName())
        self.counterName.addItems(diningCon.showCafeAllCounterName(self.cafeName.currentText()))
        self.cafeName.currentTextChanged.connect(lambda: self.change_cafe_func())
        self.dishes.dishes_change(self.cafeName.currentText(), self.counterName.currentText())
        self.dishesArea.setWidget(self.dishes)

    def change_cafe_func(self):
        self.counterName.clear()
        self.counterName.addItems(
            diningCon.showCafeAllCounterName(self.cafeName.currentText()))

    def change_dishes_func(self):
        # print(self.cafeName.currentText(), self.counterName.currentText())
        self.dishes.dishes_change(self.cafeName.currentText(), self.counterName.currentText())
        # print('here')
        self.dishesArea.setWidget(self.dishes)
        '''
        while self.dishesAreaLayout.count():
            child = self.dishesAreaLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        '''
        # print(self.dishes.dishesList)
        # self.dishesAreaLayout.addWidget(self.dishesArea)

    def layout_init(self):
        self.cafeNameLayOut.addWidget(self.cafeLabel)
        self.cafeNameLayOut.addWidget(self.cafeName)
        self.counterNameLayOut.addWidget(self.counterLabel)
        self.counterNameLayOut.addWidget(self.counterName)
        self.selectLayout.addLayout(self.cafeNameLayOut)
        self.selectLayout.addLayout(self.counterNameLayOut)
        self.selectLayout.addWidget(self.checkButton)
        self.userLayout.addWidget(self.userLabel)
        self.userLayout.addWidget(self.logoutButton)
        self.selectAndUserLayout.addLayout(self.selectLayout)
        self.selectAndUserLayout.addLayout(self.userLayout)
        self.dishesAreaLayout.addWidget(self.dishesArea)
        self.allLayout.addLayout(self.selectAndUserLayout)
        self.allLayout.addLayout(self.dishesAreaLayout)
        self.setLayout(self.allLayout)

    def button_init(self):
        self.logoutButton.clicked.connect(self.log_out)
        self.checkButton.clicked.connect(lambda: self.change_dishes_func())

    def log_out(self):
        choice = QMessageBox.question(self, '确认注销', '您确定要注销吗', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.close()


class Dishes(QWidget):
    def __init__(self):
        super(Dishes, self).__init__()
        self.dishesList = []
        self.allLayout = QVBoxLayout()
        self.setLayout(self.allLayout)

    def dishes_change(self, cafe_name: str, counter_name: str):
        self.dishesList = diningCon.showCounterAllDish(cafe_name, counter_name)
        if self.allLayout.count():
            item_list = list(range(self.allLayout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = self.allLayout.itemAt(i)
                self.allLayout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
        '''
        while self.allLayout.count() > 0:
            child = self.allLayout.takeAt(0)
            child.deleteLater()
            print('here')
        print('suc1')
        '''
        temp_all_layout = QVBoxLayout()
        cnt = 0
        temp_layout = QHBoxLayout()
        for dish in self.dishesList:
            dish_label = QLabel(dish)
            temp_layout.addWidget(dish_label)
            cnt += 1
            if cnt % 5 == 0:
                temp_all_layout.addLayout(temp_layout)
                temp_layout = QHBoxLayout()
        self.allLayout.addLayout(temp_all_layout)


'''
class Cuisine(QWidget):
    def __init__(self, cafe_name: str, counter_name: str, name: str):
        super(Cuisine, self).__init__()
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap('image.jpg'))
        self.name = QLabel(name)
        self.cafeName = cafe_name
        self.counterName = counter_name

        self.recordButton = QPushButton('添加记录')
        self.bookButton = QPushButton('添加书签')

        self.buttonLayout = QHBoxLayout()
        self.allVLayout = QVBoxLayout()

        self.button_init()
        self.layout_init()

    def button_init(self):
        self.recordButton.clicked.connect(self.record())
        self.bookButton.clicked.connect(self.like())

    def layout_init(self):
        self.buttonLayout.addWidget(self.recordButton)
        self.buttonLayout.addWidget(self.bookButton)
        self.allVLayout.addWidget(self.pic)
        self.allVLayout.addWidget(self.name)
        self.allVLayout.addLayout(self.buttonLayout)
        self.setLayout(self.allVLayout)

    def record(self):

    def like(self):

class Re


class LikeWindow(QWidget):
    def __init__(self, user_name: str):
        super(LikeWindow, self).__init__()
        self.user_name = user_name
        self.setWindowTitle('北航吃什么：用户书签界面')
        self.resize(1500,800)

        self.userLabel = QLabel('当前用户: ' + self.user_name, self)
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow('ycz')
    mainWindow.show()
    sys.exit(app.exec_())
