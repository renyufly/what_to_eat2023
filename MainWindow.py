from PyQt5.Qt import *
import sys
from diningDatabase import dining_user_con

diningCon = dining_user_con('diningData.db')


class MainWindow(QWidget):

    def __init__(self, usr: str):
        super(MainWindow, self).__init__()
        self.curUser = usr
        self.setWindowTitle('北航吃什么')
        self.resize(1500, 800)

        self.userLabel = QLabel('当前用户：' + usr)
        self.logoutButton = QPushButton('退出')
        self.cafeLabel = QLabel('请选择目标食堂')
        self.cafeName = QComboBox(self)
        self.counterLabel = QLabel('请选择目标柜台')
        self.counterName = QComboBox(self)
        self.dishes = Dishes()
        self.dishesArea = QScrollArea(self)

        self.cafeNameLayOut = QVBoxLayout()
        self.counterNameLayOut = QVBoxLayout()
        self.selectLayout = QHBoxLayout()
        self.userLayout = QHBoxLayout()
        self.selectAndUserLayout = QHBoxLayout()
        self.allLayout = QVBoxLayout()

        self.cafe_and_counter_init()
        self.logout_button_init()
        self.layout_init()

    def cafe_and_counter_init(self):
        self.cafeName.addItems(diningCon.showAllCafeName())
        self.counterName.addItems(diningCon.showCafeAllCounterName(self.cafeName.currentText()))
        self.cafeName.currentTextChanged.connect(lambda: self.change_cafe_func())
        self.counterName.currentTextChanged.connect(lambda: self.change_counter_func())
        self.dishes.dishes_change(self.cafeName.currentText(), self.counterName.currentText())
        self.dishesArea.setWidget(self.dishes)

    def change_cafe_func(self):
        self.counterName.clear()
        self.counterName.addItems(
            diningCon.showCafeAllCounterName(self.cafeName.currentText()))
        # self.dishes.dishes_change(self.cafeName.currentText(), self.counterName.currentText())
        # self.dishesArea.setWidget(self.dishes)

    # def change_counter_func(self):
        # self.dishes.dishes_change(self.cafeName.currentText(), self.counterName.currentText())
        # self.dishesArea.setWidget(self.dishes)

    def layout_init(self):
        self.selectLayout.addWidget(self.cafeName)
        self.selectLayout.addWidget(self.counterName)
        self.userLayout.addWidget(self.userLabel)
        self.userLayout.addWidget(self.logoutButton)
        self.selectAndUserLayout.addLayout(self.selectLayout)
        self.selectAndUserLayout.addLayout(self.userLayout)
        self.selectAndUserLayout.setSpacing(200)
        self.allLayout.addLayout(self.selectAndUserLayout)
        self.allLayout.addWidget(self.dishesArea)
        self.setLayout(self.allLayout)

    def logout_button_init(self):
        self.logoutButton.clicked.connect(self.log_out)

    def log_out(self):
        choice = QMessageBox.question(self, '确认注销', '您确定要注销吗', QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            self.close()


class Dishes(QWidget):
    def __init__(self):
        super(Dishes, self).__init__()
        self.dishesList = []
        self.allLayout = QVBoxLayout()

    def dishes_change(self, cafe_name: str, counter_name: str):
        self.dishesList = diningCon.showCounterAllDish(cafe_name, counter_name)
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
        self.allLayout = temp_all_layout
        self.setLayout(self.allLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow('ycz')
    mainWindow.show()
    sys.exit(app.exec_())
