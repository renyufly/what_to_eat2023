from PyQt5.Qt import *
from diningDatabase import dining_user_con
from userRecordDatabase import user_record_con
from database import user_con
import datetime

userInformDataBase = user_con("data.db")
diningCon = dining_user_con("diningData.db")
recordCon = user_record_con("userCon.db")


class MainWindow(QWidget):
    def __init__(self, user: str):
        super(MainWindow, self).__init__()
        self.userName = user
        self.setWindowTitle("北航吃什么")
        self.resize(1500, 800)

        self.cafeLabel = QLabel("请选择目标食堂")
        self.cafeName = QComboBox(self)
        self.counterLabel = QLabel("请选择目标柜台")
        self.userLabel = QLabel("当前用户：" + self.userName)
        font = QFont("宋体", 16)
        self.userLabel.setFont(font)
        self.checkButton = QPushButton("确定")
        self.likeCafeButton = QPushButton("收藏当前餐厅")
        self.likeCounterButton = QPushButton("收藏当前柜台")
        self.checkTop50Button = QPushButton("必吃排行榜")
        self.recommendButton = QPushButton("菜品推荐")
        self.logoutButton = QPushButton("退出")
        self.counterName = QComboBox(self)
        self.dishes = Dishes(self.userName)
        self.dishesArea = QScrollArea(self)
        self.dishesArea.setWidgetResizable(True)
        self.dishesArea.setMinimumSize(1300, 600)
        self.openRecordWindowButton = QPushButton("查看个人用餐记录")
        self.openLikeWindowButton = QPushButton("查看个人收藏")
        self.recordWindow = RecordWindow(self.userName, self)
        self.bookWindow = BookWindow(self.userName, self)
        self.rankListWindow = RankListWindow(self.userName, self)
        self.recommendWindow = RecommendWindow(self.userName, self)

        self.cafeNameLayOut = QVBoxLayout()
        self.counterNameLayOut = QVBoxLayout()
        self.likeLayout = QVBoxLayout()
        self.selectLayout = QHBoxLayout()
        self.userLayout = QVBoxLayout()
        self.recordAndLikeButtonLayout = QVBoxLayout()
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
        self.dishes.dishes_change(
            self.cafeName.currentText(), self.counterName.currentText()
        )
        self.dishesArea.setWidget(self.dishes)

    def layout_init(self):
        self.cafeNameLayOut.addWidget(self.cafeLabel)
        self.cafeNameLayOut.addWidget(self.cafeName)
        self.counterNameLayOut.addWidget(self.counterLabel)
        self.counterNameLayOut.addWidget(self.counterName)
        self.likeLayout.addWidget(self.likeCafeButton)
        self.likeLayout.addWidget(self.likeCounterButton)
        self.selectLayout.addLayout(self.cafeNameLayOut)
        self.selectLayout.addLayout(self.counterNameLayOut)
        self.selectLayout.addWidget(self.checkButton)
        self.userLayout.addWidget(self.userLabel)
        self.userLayout.addWidget(self.logoutButton)
        self.recordAndLikeButtonLayout.addWidget(self.openRecordWindowButton)
        self.recordAndLikeButtonLayout.addWidget(self.openLikeWindowButton)
        self.selectAndUserLayout.addLayout(self.selectLayout)
        self.selectAndUserLayout.addLayout(self.likeLayout)
        self.selectAndUserLayout.addLayout(self.recordAndLikeButtonLayout)
        self.selectAndUserLayout.addWidget(self.checkTop50Button)
        self.selectAndUserLayout.addWidget(self.recommendButton)
        self.selectAndUserLayout.addLayout(self.userLayout)
        self.dishesAreaLayout.addWidget(self.dishesArea)
        self.allLayout.addLayout(self.selectAndUserLayout)
        self.allLayout.addLayout(self.dishesAreaLayout)
        self.setLayout(self.allLayout)

    def button_init(self):
        self.logoutButton.clicked.connect(self.log_out)
        self.checkButton.clicked.connect(self.change_dishes_func)
        self.likeCafeButton.clicked.connect(self.like_cafe)
        self.likeCounterButton.clicked.connect(self.like_counter)
        self.openRecordWindowButton.clicked.connect(self.open_record_window)
        self.openLikeWindowButton.clicked.connect(self.open_book_window)
        self.checkTop50Button.clicked.connect(self.open_rank_list_window)
        self.recommendButton.clicked.connect(self.open_recommend_window)

    def log_out(self):
        choice = QMessageBox.question(
            self, "确认退出", "您确定要退出吗", QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes:
            self.close()

    def open_record_window(self):
        self.recordWindow = RecordWindow(self.userName, self)
        self.close()
        self.recordWindow.show()

    def open_book_window(self):
        self.bookWindow = BookWindow(self.userName, self)
        self.close()
        self.bookWindow.show()

    def open_rank_list_window(self):
        self.rankListWindow = RankListWindow(self.userName, self)
        self.close()
        self.rankListWindow.show()

    def open_recommend_window(self):
        self.recommendWindow = RecommendWindow(self.userName, self)
        self.close()
        self.recommendWindow.show()

    def like_cafe(self):
        if not recordCon.addStarCafe(self.userName, self.cafeName.currentText()):
            QMessageBox.information(self, "提示", "您已经收藏过该餐厅！")
        else:
            QMessageBox.information(self, "提示", "添加书签成功!")

    def like_counter(self):
        if not recordCon.addStarCounter(
            self.userName, self.cafeName.currentText(), self.counterName.currentText()
        ):
            QMessageBox.information(self, "提示", "您已经收藏过该柜台！")
        else:
            QMessageBox.information(self, "提示", "添加书签成功!")


class Dishes(QWidget):
    def __init__(self, user_name: str):
        super(Dishes, self).__init__()
        self.dishesList = []
        self.userName = user_name
        self.allLayout = QVBoxLayout()
        self.setLayout(self.allLayout)

    def delete_all(self, this_layout):
        if this_layout.count():
            item_list = list(range(this_layout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = this_layout.itemAt(i)
                this_layout.removeItem(item)
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
            dish_item = Cuisine(self.userName, cafe_name, counter_name, dish)
            temp_layout.addWidget(dish_item)
            cnt += 1
            if cnt % 6 == 0:
                temp_all_layout.addLayout(temp_layout)
                temp_layout = QHBoxLayout()
        temp_layout.setAlignment(Qt.AlignLeft)
        temp_all_layout.addLayout(temp_layout)
        temp_all_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.allLayout.addLayout(temp_all_layout)


class Cuisine(QWidget):
    def __init__(self, user_name: str, cafe_name: str, counter_name: str, name: str):
        super(Cuisine, self).__init__()
        pic_and_name = name.split(" ")

        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap(pic_and_name[1]))
        self.pic.setFixedSize(200, 100)
        self.pic.setScaledContents(True)

        self.username = user_name
        self.name = QLabel(pic_and_name[0])
        font = QFont("宋体", 14)
        self.name.setFont(font)
        self.cafeName = cafe_name
        self.counterName = counter_name
        self.setFixedSize(215, 225)

        self.recordButton = QPushButton("添加记录")
        self.bookButton = QPushButton("添加书签")
        self.addCommentButton = QPushButton("发表评论")
        self.lookCommentButton = QPushButton("查看评论")

        self.picLayout = QHBoxLayout()
        self.labelLayout = QHBoxLayout()
        self.buttonLayout1 = QHBoxLayout()
        self.buttonLayout2 = QHBoxLayout()
        self.allVLayout = QVBoxLayout()

        self.button_init()
        self.layout_init()

    def button_init(self):
        self.recordButton.clicked.connect(self.record)
        self.bookButton.clicked.connect(self.like)
        self.addCommentButton.clicked.connect(self.add_comment)
        self.lookCommentButton.clicked.connect(self.check_comment)

    def layout_init(self):
        self.picLayout.addWidget(self.pic)
        self.picLayout.setAlignment(Qt.AlignCenter)

        self.labelLayout.addWidget(self.name)
        self.labelLayout.setAlignment(Qt.AlignCenter)
        self.buttonLayout1.addWidget(self.recordButton)
        self.buttonLayout1.addWidget(self.bookButton)
        self.buttonLayout2.addWidget(self.addCommentButton)
        self.buttonLayout2.addWidget(self.lookCommentButton)
        self.allVLayout.addLayout(self.picLayout)
        self.allVLayout.addLayout(self.labelLayout)
        self.allVLayout.addLayout(self.buttonLayout1)
        self.allVLayout.addLayout(self.buttonLayout2)

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
        else:
            QMessageBox.information(self, "提示", "收藏成功！")

    def add_comment(self):
        self.commentWindow = CommentHelp(self.username, self.name.text())
        self.commentWindow.show()

    def check_comment(self):
        self.dishCommentWindow = CommentWindow(self.name.text())
        self.dishCommentWindow.show()


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


class CommentHelp(QDialog):
    def __init__(self, user_name: str, dish_name: str):
        super(CommentHelp, self).__init__()
        self.setWindowTitle("发表评论")
        self.setFixedSize(800, 300)
        self.userName = user_name
        self.dishName = dish_name

        self.tipLabel = QLabel("请留下您对这道菜的评论:")
        font = QFont("宋体", 14)
        self.tipLabel.setFont(font)
        self.commentPart = QTextEdit()
        self.commentPart.textChanged.connect(self.check_input_func)
        self.confirmButton = QPushButton("确认发表")
        self.cancelButton = QPushButton("取消")
        self.confirmButton.clicked.connect(self.add_comment)
        self.confirmButton.setEnabled(False)
        self.cancelButton.clicked.connect(self.cancel)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.confirmButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.allLayout = QVBoxLayout()
        self.allLayout.addWidget(self.tipLabel)
        self.allLayout.addWidget(self.commentPart)
        self.allLayout.addLayout(self.buttonLayout)
        self.setLayout(self.allLayout)

    def check_input_func(self):
        if (
            self.commentPart.toPlainText() == ""
            or self.commentPart.toPlainText().isspace()
        ):
            self.confirmButton.setEnabled(False)
        else:
            self.confirmButton.setEnabled(True)

    def add_comment(self):
        now_time = datetime.datetime.now().strftime("%Y-%m-%d")
        if not userInformDataBase.comment_dish(
            self.userName, self.dishName, self.commentPart.toPlainText(), now_time
        ):
            QMessageBox.critical(self, "错误", "用户不存在！")
        else:
            QMessageBox.information(self, "提示", "评论成功！")
            self.close()

    def cancel(self):
        self.commentPart.clear()
        self.close()


class CommentWindow(QWidget):
    def __init__(self, dish_name: str):
        super(CommentWindow, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("用户评论")
        self.dishName = dish_name

        self.commentPart = CommentPart(self.dishName)
        self.commentArea = QScrollArea(self)
        self.commentArea.setWidget(self.commentPart)
        self.commentArea.setWidgetResizable(True)
        self.commentArea.setMinimumSize(700, 500)

        self.allLayout = QVBoxLayout()
        self.allLayout.addWidget(self.commentArea)
        self.setLayout(self.allLayout)


class CommentPart(QWidget):
    def __init__(self, dish_name: str):
        super(CommentPart, self).__init__()
        self.dishName = dish_name
        self.commentList = userInformDataBase.get_comment(self.dishName)
        self.allLayout = QVBoxLayout()
        self.show_comments()

    def show_comments(self):
        self.delete_all(self.allLayout)
        self.commentList = userInformDataBase.get_comment(self.dishName)
        for user_comment in self.commentList:
            comment = Comment(user_comment)
            self.allLayout.addWidget(comment)
        self.allLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(self.allLayout)

    def delete_all(self, this_layout):
        if this_layout.count():
            item_list = list(range(this_layout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = this_layout.itemAt(i)
                this_layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    self.delete_all(item)


class Comment(QWidget):
    def __init__(self, comment_content: tuple):
        super(Comment, self).__init__()
        self.user = comment_content[0]
        self.commentWord = comment_content[1]
        self.time = comment_content[2]
        self.setFixedSize(600, 100)

        self.userLabel = QLabel(self.time + " " + self.user)
        self.commentBrowser = QTextBrowser()
        self.commentBrowser.setText(self.commentWord)

        self.allLayout = QVBoxLayout()
        self.allLayout.addWidget(self.userLabel)
        self.allLayout.addWidget(self.commentBrowser)
        self.setLayout(self.allLayout)


class RecordWindow(QWidget):
    def __init__(self, user_name: str, main_window: MainWindow):
        super(RecordWindow, self).__init__()
        self.user_name = user_name
        self.setFixedSize(1500, 800)
        self.setWindowTitle("个人记录界面")
        self.mainWindow = main_window

        self.userLabel = QLabel("当前用户: " + self.user_name, self)
        font = QFont("宋体", 22)
        self.userLabel.setFont(font)
        self.userLabel.setFixedSize(500, 50)
        self.backButton = QPushButton("返回主界面")
        self.backButton.setFixedSize(500, 50)
        self.backButton.clicked.connect(self.back_to_main_window)

        self.recordPart = RecordPart(self.user_name)
        self.recordArea = QScrollArea(self)
        self.recordArea.setWidget(self.recordPart)
        self.recordArea.setWidgetResizable(True)
        self.recordArea.setMinimumSize(1300, 600)

        self.userAndButtonLayout = QHBoxLayout()
        self.userAndButtonLayout.addWidget(self.userLabel)
        self.userAndButtonLayout.addWidget(self.backButton)
        self.allLayout = QVBoxLayout()
        self.allLayout.addLayout(self.userAndButtonLayout)
        self.allLayout.addWidget(self.recordArea)
        self.setLayout(self.allLayout)

    def back_to_main_window(self):
        self.close()
        self.mainWindow.show()


class RecordPart(QWidget):
    def __init__(self, user_name: str):
        super(RecordPart, self).__init__()
        self.user_name = user_name
        self.recordList = recordCon.showAllDishName(self.user_name)
        self.allLayout = QVBoxLayout()
        self.show_list()

    def show_list(self):
        self.delete_all(self.allLayout)
        self.recordList = recordCon.showAllDishName(self.user_name)
        for dish in self.recordList:
            record = Record(self, dish, self.user_name)
            self.allLayout.addWidget(record)
        self.allLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(self.allLayout)

    def delete_all(self, this_layout):
        if this_layout.count():
            item_list = list(range(this_layout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = this_layout.itemAt(i)
                this_layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    self.delete_all(item)


class Record(QWidget):
    def __init__(self, father: RecordPart, dish_name: str, user_name: str):
        super(Record, self).__init__()
        self.father = father
        self.userName = user_name
        self.setFixedSize(1300, 75)

        self.dish_label = QLabel(dish_name)
        self.dish_label.setMinimumSize(300, 75)
        font = QFont("宋体", 20)
        self.dish_label.setFont(font)
        self.delete_button = QPushButton("删除本条记录")
        self.delete_button.clicked.connect(self.delete_dish)
        self.delete_button.setFixedSize(100, 50)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dish_label)
        self.layout.addWidget(self.delete_button)
        self.setLayout(self.layout)

    def delete_dish(self):
        choice = QMessageBox.question(
            self, "确认删除", "您确定要删除这条记录吗", QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes:
            inform_list = self.dish_label.text().split(" ")
            time = inform_list[0]
            dish_type = inform_list[1]
            dish_name = inform_list[2]
            dish_counter = inform_list[3]
            dish_cafe = inform_list[4]
            recordCon.deleteDish(
                self.userName, dish_name, dish_counter, dish_cafe, time, dish_type
            )
            self.father.delete_all(self.father.allLayout)
            self.father.show_list()


class BookWindow(QWidget):
    def __init__(self, user_name: str, main_window: MainWindow):
        super(BookWindow, self).__init__()
        self.user_name = user_name
        self.setFixedSize(1500, 800)
        self.setWindowTitle("个人收藏界面")
        self.mainWindow = main_window

        self.userLabel = QLabel("当前用户: " + self.user_name, self)
        font = QFont("宋体", 22)
        self.userLabel.setFont(font)
        self.userLabel.setFixedSize(500, 50)
        font = QFont("宋体", 18)
        self.backButton = QPushButton("返回主界面")
        self.backButton.setFont(font)
        self.backButton.setFixedSize(500, 45)
        self.backButton.clicked.connect(self.back_to_main_window)
        self.userAndBackLayout = QHBoxLayout()
        self.userAndBackLayout.addWidget(self.userLabel)
        self.userAndBackLayout.addWidget(self.backButton)

        self.cafeSelectButton = QPushButton("查看收藏的餐厅")
        self.cafeSelectButton.setFixedSize(300, 45)
        self.cafeSelectButton.setFont(font)
        self.cafeSelectButton.clicked.connect(self.cafe_button_click)
        self.counterSelectButton = QPushButton("查看收藏的柜台")
        self.counterSelectButton.setFixedSize(300, 45)
        self.counterSelectButton.setFont(font)
        self.counterSelectButton.clicked.connect(self.counter_button_click)
        self.dishSelectButton = QPushButton("查看收藏的菜肴")
        self.dishSelectButton.setFixedSize(300, 45)
        self.dishSelectButton.setFont(font)
        self.dishSelectButton.clicked.connect(self.dish_button_click)
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.cafeSelectButton)
        self.buttonLayout.addWidget(self.counterSelectButton)
        self.buttonLayout.addWidget(self.dishSelectButton)

        self.bookPart = BookPart(self.user_name, self.mainWindow)
        self.bookArea = QScrollArea(self)
        self.bookArea.setWidget(self.bookPart)
        self.bookArea.setWidgetResizable(True)
        self.bookArea.setMinimumSize(1300, 400)

        self.allLayout = QVBoxLayout()
        self.allLayout.addLayout(self.userAndBackLayout)
        self.allLayout.addLayout(self.buttonLayout)
        self.allLayout.addWidget(self.bookArea)
        self.setLayout(self.allLayout)

    def back_to_main_window(self):
        self.close()
        self.mainWindow.show()

    def cafe_button_click(self):
        self.bookPart.show_books(1)

    def counter_button_click(self):
        self.bookPart.show_books(2)

    def dish_button_click(self):
        self.bookPart.show_books(3)


class BookPart(QWidget):
    def __init__(self, user_name: str, main_window: MainWindow):
        super(BookPart, self).__init__()
        self.userName = user_name
        self.allLayout = QVBoxLayout()
        self.mainWindow = main_window

    def show_books(self, search_type: int):
        self.delete_all(self.allLayout)
        if search_type == 1:
            self.bookList = recordCon.showStarAllCafe(self.userName)
            self.tipLabel = QLabel("您目前收藏的餐厅有：")
        elif search_type == 2:
            self.bookList = recordCon.showStarAllCounter(self.userName)
            self.tipLabel = QLabel("您目前收藏的柜台有：")
        else:
            self.bookList = recordCon.showStarAllDish(self.userName)
            self.tipLabel = QLabel("您目前收藏的菜肴有：")
        font = QFont("宋体", 18)
        self.tipLabel.setFont(font)
        self.allLayout.addWidget(self.tipLabel)
        for item in self.bookList:
            like = Like(self.mainWindow, self, item, self.userName, search_type)
            self.allLayout.addWidget(like)
        self.allLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(self.allLayout)

    def delete_all(self, this_layout):
        if this_layout.count():
            item_list = list(range(this_layout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = this_layout.itemAt(i)
                this_layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    self.delete_all(item)


class Like(QWidget):
    def __init__(
        self,
        main_window: MainWindow,
        father: BookPart,
        star_item: str,
        user_name: str,
        search_type: int,
    ):
        super(Like, self).__init__()
        self.mainWindow = main_window
        self.father = father
        self.userName = user_name
        self.name = star_item
        self.searchType = search_type
        self.setFixedSize(1250, 75)

        self.item_label = QLabel(star_item)
        self.item_label.setMinimumSize(300, 75)
        font = QFont("宋体", 20)
        self.item_label.setFont(font)
        self.delete_button = QPushButton("取消收藏")
        self.delete_button.clicked.connect(self.delete_star)
        self.delete_button.setFixedSize(100, 50)
        self.jump_button = QPushButton("跳转")
        self.jump_button.setFixedSize(100, 50)
        self.jump_button.clicked.connect(self.jump)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.item_label)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.jump_button)
        self.setLayout(self.layout)

    def delete_star(self):
        choice = QMessageBox.question(
            self, "确认删除", "您确定要删除该收藏吗", QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes:
            recordCon.deleteStar(self.userName, self.name)
            self.father.delete_all(self.father.allLayout)
            self.father.show_books(self.searchType)

    def jump(self):
        if self.searchType == 2 or self.searchType == 3:
            temp_list = self.name.split(" ")
            cafe_name = temp_list[0]
            counter_name = temp_list[1]
            self.mainWindow.dishes.dishes_change(cafe_name, counter_name)
            self.mainWindow.dishesArea.setWidget(self.mainWindow.dishes)
            self.mainWindow.show()
        else:
            temp_list = self.name.split(" ")
            cafe_name = temp_list[0]
            counter_list = diningCon.showCafeAllCounterName(cafe_name)
            counter_name = counter_list[0]
            self.mainWindow.dishes.dishes_change(cafe_name, counter_name)
            self.mainWindow.dishesArea.setWidget(self.mainWindow.dishes)
            self.mainWindow.show()


class RankListWindow(QWidget):
    def __init__(self, user_name: str, father: MainWindow):
        super(RankListWindow, self).__init__()
        self.setWindowTitle("校园必吃排行榜")
        self.setFixedSize(1500, 800)
        self.userName = user_name
        self.fatherWindow = father

        self.tipLabel = QLabel("校园菜品必吃排行榜Top50")
        font = QFont("华文行楷", 24)
        self.tipLabel.setFont(font)
        self.tipLabel.setFixedSize(500, 50)
        self.backButton = QPushButton("返回主界面")
        self.backButton.setFixedSize(500, 50)
        self.backButton.clicked.connect(self.back_to_main_window)
        self.labelAndButtonLayout = QHBoxLayout()
        self.labelAndButtonLayout.addWidget(self.tipLabel)
        self.labelAndButtonLayout.addWidget(self.backButton)

        self.rankList = RankList(self.userName)
        self.rankArea = QScrollArea(self)
        self.rankArea.setWidget(self.rankList)
        self.rankArea.setWidgetResizable(True)
        self.rankArea.setMinimumSize(1300, 600)

        self.allLayout = QVBoxLayout()
        self.allLayout.addLayout(self.labelAndButtonLayout)
        self.allLayout.addWidget(self.rankArea)
        self.setLayout(self.allLayout)

    def back_to_main_window(self):
        self.close()
        self.fatherWindow.show()


class RankList(QWidget):
    def __init__(self, user_name: str):
        super(RankList, self).__init__()
        self.userName = user_name
        self.allLayout = QVBoxLayout()
        self.show_list()

    def show_list(self):
        self.delete_all(self.allLayout)
        self.rankList = diningCon.showTop50DishRankingList()
        for dish in self.rankList:
            rank = Rank(dish, self.userName)
            self.allLayout.addWidget(rank)
        self.allLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(self.allLayout)

    def delete_all(self, this_layout):
        if this_layout.count():
            item_list = list(range(this_layout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = this_layout.itemAt(i)
                this_layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    self.delete_all(item)


class Rank(QWidget):
    def __init__(self, dish_name: str, user_name: str):
        super(Rank, self).__init__()
        self.userName = user_name
        self.setFixedSize(1200, 75)

        self.dishLabel = QLabel(dish_name)
        self.dishLabel.setMinimumSize(300, 75)
        font = QFont("宋体", 20)
        self.dishLabel.setFont(font)
        self.likeButton = QPushButton("收藏该菜品")
        self.likeButton.clicked.connect(self.like_dish)
        self.likeButton.setFixedSize(100, 60)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dishLabel)
        self.layout.addWidget(self.likeButton)
        self.setLayout(self.layout)

    def like_dish(self):
        temp_list = self.dishLabel.text().split(" ")
        self.dishName = temp_list[0]
        self.counterName = temp_list[1]
        self.cafeName = temp_list[2]
        if not recordCon.addStarDish(
            self.userName, self.cafeName, self.counterName, self.dishName
        ):
            QMessageBox.information(self, "提示", "您已经收藏过该菜品！")
        else:
            QMessageBox.information(self, "提示", "收藏成功！")


class RecommendWindow(QWidget):
    def __init__(self, user_name: str, father: MainWindow):
        super(RecommendWindow, self).__init__()
        self.setWindowTitle("校园菜品推荐")
        self.setFixedSize(1500, 800)
        self.userName = user_name
        self.fatherWindow = father

        self.tipLabel = QLabel("今日校园菜品推荐")
        font = QFont("华文行楷", 24)
        self.tipLabel.setFont(font)
        self.tipLabel.setFixedSize(500, 50)
        self.backButton = QPushButton("返回主界面")
        self.backButton.setFixedSize(500, 50)
        self.backButton.clicked.connect(self.back_to_main_window)
        self.labelAndButtonLayout = QHBoxLayout()
        self.labelAndButtonLayout.addWidget(self.tipLabel)
        self.labelAndButtonLayout.addWidget(self.backButton)

        self.recommendList = RecommendList(self.userName)
        self.recommendArea = QScrollArea(self)
        self.recommendArea.setWidget(self.recommendList)
        self.recommendArea.setWidgetResizable(True)
        self.recommendArea.setMinimumSize(1300, 600)

        self.allLayout = QVBoxLayout()
        self.allLayout.addLayout(self.labelAndButtonLayout)
        self.allLayout.addWidget(self.recommendArea)
        self.setLayout(self.allLayout)

    def back_to_main_window(self):
        self.close()
        self.fatherWindow.show()


class RecommendList(QWidget):
    def __init__(self, user_name: str):
        super(RecommendList, self).__init__()
        self.userName = user_name
        self.allLayout = QVBoxLayout()
        self.show_list()

    def show_list(self):
        self.delete_all(self.allLayout)
        self.recommendList = diningCon.recommendDish(self.userName)
        for dish in self.recommendList:
            recommend = Recommend(dish, self.userName)
            self.allLayout.addWidget(recommend)
        self.allLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.setLayout(self.allLayout)

    def delete_all(self, this_layout):
        if this_layout.count():
            item_list = list(range(this_layout.count()))
            item_list.reverse()  # 倒序删除，避免影响布局顺序
            for i in item_list:
                item = this_layout.itemAt(i)
                this_layout.removeItem(item)
                if item.widget():
                    item.widget().deleteLater()
                else:
                    self.delete_all(item)


class Recommend(QWidget):
    def __init__(self, dish_name: str, user_name: str):
        super(Recommend, self).__init__()
        self.userName = user_name
        self.setFixedSize(1200, 75)

        self.dishLabel = QLabel(dish_name)
        self.dishLabel.setMinimumSize(300, 75)
        font = QFont("宋体", 20)
        self.dishLabel.setFont(font)
        self.likeButton = QPushButton("收藏该菜品")
        self.likeButton.clicked.connect(self.like_dish)
        self.likeButton.setFixedSize(100, 60)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.dishLabel)
        self.layout.addWidget(self.likeButton)
        self.setLayout(self.layout)

    def like_dish(self):
        temp_list = self.dishLabel.text().split(" ")
        self.dishName = temp_list[0]
        self.counterName = temp_list[1]
        self.cafeName = temp_list[2]
        if not recordCon.addStarDish(
            self.userName, self.cafeName, self.counterName, self.dishName
        ):
            QMessageBox.information(self, "提示", "您已经收藏过该菜品！")
        else:
            QMessageBox.information(self, "提示", "收藏成功！")
