from PyQt5.Qt import *
import sys
from diningDatabase import dining_user_con
from userRecordDatabase import user_record_con

diningCon = dining_user_con("diningData.db")
recordCon = user_record_con("userCon.db")


class MainWindow(QWidget):
    def __init__(self, usr: str):
        super(MainWindow, self).__init__()
        self.curUser = usr
        self.setWindowTitle("北航吃什么")
        self.resize(1500, 800)

        self.cafeLabel = QLabel("请选择目标食堂")
        self.cafeName = QComboBox(self)
        self.counterLabel = QLabel("请选择目标柜台")
        self.userLabel = QLabel("当前用户：" + usr)
        self.checkButton = QPushButton("确定")
        self.logoutButton = QPushButton("退出")
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
        self.counterName.addItems(
            diningCon.showCafeAllCounterName(self.cafeName.currentText())
        )
        self.cafeName.currentTextChanged.connect(lambda: self.change_cafe_func())
        self.dishes.dishes_change(
            self.cafeName.currentText(), self.counterName.currentText()
        )
        self.dishesArea.setWidget(self.dishes)

    def change_cafe_func(self):
        self.counterName.clear()
        self.counterName.addItems(
            diningCon.showCafeAllCounterName(self.cafeName.currentText())
        )

    def change_dishes_func(self):
        # print(self.cafeName.currentText(), self.counterName.currentText())
        self.dishes.dishes_change(
            self.cafeName.currentText(), self.counterName.currentText()
        )
        # print('here')
        self.dishesArea.setWidget(self.dishes)
        """
        while self.dishesAreaLayout.count():
            child = self.dishesAreaLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        """
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
        choice = QMessageBox.question(
            self, "确认注销", "您确定要注销吗", QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes:
            self.close()


class Dishes(QWidget):
    def __init__(self):
        super(Dishes, self).__init__()
        self.dishesList = []
        self.allLayout = QVBoxLayout()
        self.setLayout(self.allLayout)

    def delete_all(self, thisLayout):
        if thisLayout.count():
            item_list = list(range(thisLayout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = thisLayout.itemAt(i)
                thisLayout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    self.delete_all(item)

    def dishes_change(self, cafe_name: str, counter_name: str):
        self.dishesList = diningCon.showCounterAllDish(cafe_name, counter_name)
        self.delete_all(self.allLayout)
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


class Cuisine(QWidget):
    def __init__(self, user_name: str, cafe_name: str, counter_name: str, name: str):
        super(Cuisine, self).__init__()
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap("image.jpg"))
        self.pic.setFixedSize(200, 100)
        self.pic.setScaledContents(True)
        self.username = user_name
        self.name = QLabel(name)
        self.cafeName = cafe_name
        self.counterName = counter_name
        self.setFixedSize(215, 200)

        self.recordButton = QPushButton("添加记录")
        self.bookButton = QPushButton("添加书签")

        self.picLayout = QHBoxLayout()
        self.labelLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.allVLayout = QVBoxLayout()

        self.button_init()
        self.layout_init()

    def button_init(self):
        self.recordButton.clicked.connect(lambda: self.record())
        self.bookButton.clicked.connect(lambda: self.like())

    def layout_init(self):
        self.picLayout.addWidget(self.pic)
        self.picLayout.setAlignment(Qt.AlignCenter)
        self.labelLayout.addWidget(self.name)
        self.labelLayout.setAlignment(Qt.AlignCenter)
        self.buttonLayout.addWidget(self.recordButton)
        self.buttonLayout.addWidget(self.bookButton)
        self.allVLayout.addLayout(self.picLayout)
        self.allVLayout.addLayout(self.labelLayout)
        self.allVLayout.addLayout(self.buttonLayout)

        self.setLayout(self.allVLayout)

    def record(self):
        self.recordWindow = RecordHelp(
            self.username, self.name.text(), self.counterName, self.cafeName
        )
        self.recordWindow.show()

    def like(self):
        if not recordCon.addStarDish(
            self.username, self.cafeName, self.counterName, self.name.text()
        ):
            QMessageBox.information(self, "提示", "您已经收藏过该菜品！")


class RecordHelp(QDialog):
    def __init__(
        self, user_name: str, dish_name: str, counter_name: str, cafe_name: str
    ):
        super(RecordHelp, self).__init__()
        self.setWindowTitle("添加记录")
        self.userName = user_name
        self.dishName = dish_name
        self.counterName = counter_name
        self.cafeName = cafe_name

        self.helpLabel = QLabel("请以形如2023-07-06的形式输入记录时间")
        self.timeLine = QLineEdit()
        self.helpLabel1 = QLabel("请选择记录用餐的形式")
        self.dishType = QComboBox()
        type_list = ["早餐", "午餐", "晚餐"]
        self.dishType.addItems(type_list)
        self.confirmButton = QPushButton("确定")
        self.cancelButton = QPushButton("取消")

        self.writeLayout = QHBoxLayout()
        self.lunchLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.allLayout = QVBoxLayout()

        self.button_init()
        self.text_line_init()
        self.layout_init()

    def button_init(self):
        self.confirmButton.setEnabled(False)
        self.confirmButton.clicked.connect(lambda: self.add_record())
        self.cancelButton.clicked.connect(lambda: self.cancel())

    def text_line_init(self):
        self.timeLine.textChanged.connect(lambda: self.check_input_func())

    def check_input_func(self):
        if self.timeLine.text():
            self.confirmButton.setEnabled(True)
        else:
            self.confirmButton.setEnabled(False)

    def layout_init(self):
        self.writeLayout.addWidget(self.helpLabel)
        self.writeLayout.addWidget(self.timeLine)
        self.lunchLayout.addWidget(self.helpLabel1)
        self.lunchLayout.addWidget(self.dishType)
        self.buttonLayout.addWidget(self.confirmButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.allLayout.addLayout(self.writeLayout)
        self.allLayout.addLayout(self.lunchLayout)
        self.allLayout.addLayout(self.buttonLayout)
        self.setLayout(self.allLayout)

    def add_record(self):
        if not recordCon.addDish(
            self.userName,
            self.dishName,
            self.counterName,
            self.cafeName,
            self.timeLine.text(),
            self.dishType.currentText(),
            diningCon,
        ):
            QMessageBox.critical(self, "错误", "错误的日期格式")
            self.timeLine.clear()
        else:
            self.close()

    def cancel(self):
        self.timeLine.clear()
        self.close()


class RecordWindow(QWidget):
    def __init__(self, user_name: str):
        super(RecordWindow, self).__init__()
        self.user_name = user_name
        self.setFixedSize(1500, 800)
        self.setWindowTitle("个人记录界面")
        self.userLabel = QLabel("当前用户: " + self.user_name, self)
        font = QFont("宋体", 22)
        self.userLabel.setFont(font)
        self.userLabel.setFixedSize(500, 50)
        self.recordPart = RecordPart(self.user_name)
        self.recordPart.setFixedSize(1500, 750)
        self.allLayout = QVBoxLayout()
        self.allLayout.addWidget(self.userLabel)
        self.allLayout.addWidget(self.recordPart)
        self.setLayout(self.allLayout)


class RecordPart(QWidget):
    def __init__(self, user_name: str):
        super(RecordPart, self).__init__()
        self.user_name = user_name
        self.recordList = recordCon.showAllDishName(self.user_name)
        print(self.recordList)
        self.allLayout = QVBoxLayout()
        self.show_list()

    def show_list(self):
        self.recordList = recordCon.showAllDishName(self.user_name)
        self.allLayout = QVBoxLayout()
        for dish in self.recordList:
            temp_layout = QHBoxLayout()
            dish_label = QLabel(dish)
            delete_button = QPushButton("删除本条记录")
            modify_button = QPushButton("更改本条记录")
            delete_button.clicked.connect(
                lambda: self.delete_dish(self.user_name, dish)
            )
            # modify_button.clicked.connect()
            temp_layout.addWidget(dish_label)
            temp_layout.addWidget(modify_button)
            temp_layout.addWidget(delete_button)
            self.allLayout.addLayout(temp_layout)
        self.setLayout(self.allLayout)

    def delete_dish(self, user_name: str, dish_inform: str):
        inform_list = dish_inform.split(" ")
        time = inform_list[0]
        dish_type = inform_list[1]
        dish_name = inform_list[2]
        dish_counter = inform_list[3]
        dish_cafe = inform_list[4]
        recordCon.deleteDish(
            user_name, dish_name, dish_counter, dish_cafe, time, dish_type
        )
        self.show_list()


class BookWindow(QWidget):
    def __init__(self, user_name: str):
        super(BookWindow, self).__init__()
        self.user_name = user_name
        self.setFixedSize(1500, 800)
        self.setWindowTitle("个人收藏界面")

        self.userLabel = QLabel("当前用户: " + self.user_name, self)
        font = QFont("宋体", 22)
        self.userLabel.setFont(font)
        self.userLabel.setFixedSize(500, 50)

        self.cafeSelectButton = QPushButton("查看收藏的餐厅")
        self.cafeSelectButton.clicked.connect(lambda: self.cafe_button_click())
        self.counterSelectButton = QPushButton("查看收藏的柜台")
        self.cafeSelectButton.clicked.connect(lambda: self.counter_button_click())
        self.dishSelectButton = QPushButton("查看收藏的菜肴")
        self.dishSelectButton.clicked.connect(lambda: self.dish_button_click())
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.cafeSelectButton)
        self.buttonLayout.addWidget(self.counterSelectButton)
        self.buttonLayout.addWidget(self.dishSelectButton)

        self.bookPart = BookPart(self.user_name)
        self.bookPart.setFixedSize(1500, 750)
        self.allLayout = QVBoxLayout()
        self.allLayout.addWidget(self.userLabel)
        self.allLayout.addLayout(self.buttonLayout)
        self.allLayout.addWidget(self.bookPart)
        self.setLayout(self.allLayout)

    def cafe_button_click(self):
        self.bookPart.show_books(1)
        self.setLayout(self.allLayout)

    def counter_button_click(self):
        self.bookPart.show_books(2)
        self.setLayout(self.allLayout)

    def dish_button_click(self):
        self.bookPart.show_books(3)
        self.setLayout(self.allLayout)


class BookPart(QWidget):
    def __init__(self, user_name: str):
        super(BookPart, self).__init__()
        self.userName = user_name
        self.allLayout = QVBoxLayout()

    def show_books(self, search_type: int):
        if search_type == 1:
            self.bookList = recordCon.showStarAllCafe(self.userName)
            self.tipLabel = QLabel("您目前收藏的餐厅有：")
        elif search_type == 2:
            self.bookList = recordCon.showStarAllCounter(self.userName)
            self.tipLabel = QLabel("您目前收藏的餐厅有：")
        else:
            self.bookList = recordCon.showStarAllDish(self.userName)
            self.tipLabel = QLabel("您目前收藏的菜肴有：")
        self.allLayout = QVBoxLayout()
        self.allLayout.addWidget(self.tipLabel)
        print(self.bookList)
        for item in self.bookList:
            temp_layout = QHBoxLayout()
            item_label = QLabel(item)
            delete_button = QPushButton("取消收藏")
            temp_layout.addWidget(item_label)
            temp_layout.addWidget(delete_button)
            self.allLayout.addLayout(temp_layout)
            print("here")
        self.setLayout(self.allLayout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    """
    mainWindow = MainWindow('ycz')
    mainWindow.show()
    """
    """
    test = Cuisine('mu', '学一食堂', '一柜台', '宫保鸡丁')
    test.show()
    recordCon.print('mu')
    
    test = RecordWindow('mu')
    test.show()
    """
    test = BookWindow("mu")
    test.show()

    sys.exit(app.exec_())
