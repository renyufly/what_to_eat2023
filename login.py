from PyQt5.Qt import *
import sys
from database import user_con
from MainWindow import MainWindow

userCon = user_con('data.db')


# 登录界面
class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.resize(300, 100)
        self.setWindowTitle('Login Window')

        # 实例化标签，输入框，按钮等内容
        self.userLabel = QLabel('用户名:', self)
        self.pwdLabel = QLabel('密码:', self)
        self.userLine = QLineEdit(self)
        self.pwdLine = QLineEdit(self)
        self.loginButton = QPushButton('登录', self)
        self.signinButton = QPushButton('注册', self)

        # 摆放框架的实例化
        self.userAndPwdLayout = QGridLayout()  # 用户名与密码区的摆放
        self.buttonLayout = QHBoxLayout()  # 登录与注册按钮的摆放
        self.allLayout = QVBoxLayout()  # 总体的纵向摆放

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()  # 登录框的摆放初始化
        self.signin_page = SigninPage()  # 实例化注册页面

    # 登录界面用户名与输入框部分的初始化
    def lineedit_init(self):
        self.userLine.setPlaceholderText('请输入您的用户名')
        self.pwdLine.setPlaceholderText('请输入您的密码')
        self.pwdLine.setEchoMode(QLineEdit.Password)
        self.userLine.textChanged.connect(self.check_input_func)
        self.pwdLine.textChanged.connect(self.check_input_func)

    # 登录按钮的信号与槽函数的链接
    def pushbutton_init(self):
        self.loginButton.setEnabled(False)
        self.loginButton.clicked.connect(self.check_login_func)
        self.signinButton.clicked.connect(self.show_signin_page_func)

    # 摆放内容的填充
    def layout_init(self):
        self.userAndPwdLayout.addWidget(self.userLabel, 0, 0, 1, 1)
        self.userAndPwdLayout.addWidget(self.userLine, 0, 1, 1, 1)
        self.userAndPwdLayout.addWidget(self.pwdLabel, 1, 0, 1, 1)
        self.userAndPwdLayout.addWidget(self.pwdLine, 1, 1, 1, 1)
        self.buttonLayout.addWidget(self.loginButton)
        self.buttonLayout.addWidget(self.signinButton)
        self.allLayout.addLayout(self.userAndPwdLayout)
        self.allLayout.addLayout(self.buttonLayout)

        self.setLayout(self.allLayout)

    # 检查用户名与密码输入框是否为空，保证两者任何一个为空时登录按钮不能被点击
    def check_input_func(self):
        if self.userLine.text() and self.pwdLine.text():
            self.loginButton.setEnabled(True)
        else:
            self.loginButton.setEnabled(False)

    # 登录，验证用户名与密码的匹配
    def check_login_func(self):
        if userCon.login(self.userLine.text(), self.pwdLine.text()):
            QMessageBox.information(self, 'Information', '登陆成功！')
            self.close()
            self.mainWindow = MainWindow(self.userLine.text())
            self.mainWindow.show()
        else:
            QMessageBox.critical(self, 'Wrong', '用户名或密码错误')
            self.pwdLine.clear()

    # 注册界面的唤出
    def show_signin_page_func(self):
        self.signin_page.exec_()


# 注册窗口
class SigninPage(QDialog):
    def __init__(self):
        super(SigninPage, self).__init__()
        self.setWindowTitle('注册')

        self.signinUserLabel = QLabel('新的用户名:', self)
        self.signinPwdLabel = QLabel('密码:', self)
        self.signinPwd2Label = QLabel('重复密码:', self)
        self.signinUserLine = QLineEdit(self)
        self.signinPwdLine = QLineEdit(self)
        self.signinPwd2Line = QLineEdit(self)
        self.signinButton = QPushButton('注册', self)

        self.userHLayout = QHBoxLayout()
        self.pwdHLayout = QHBoxLayout()
        self.pwd2HLayout = QHBoxLayout()
        self.allVLayout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    # 注册界面用户名与输入框部分的初始化，完成与检测输入内容函数的链接
    def lineedit_init(self):
        self.signinPwdLine.setEchoMode(QLineEdit.Password)
        self.signinPwd2Line.setEchoMode(QLineEdit.Password)

        self.signinUserLine.textChanged.connect(self.check_input_func)
        self.signinPwdLine.textChanged.connect(self.check_input_func)
        self.signinPwd2Line.textChanged.connect(self.check_input_func)

    # 注册界面注册按钮的初始化，完成与注册功能的链接
    def pushbutton_init(self):
        self.signinButton.setEnabled(False)
        self.signinButton.clicked.connect(self.signin_func)

    # 页面摆放内容的添加
    def layout_init(self):
        self.userHLayout.addWidget(self.signinUserLabel)
        self.userHLayout.addWidget(self.signinUserLine)
        self.pwdHLayout.addWidget(self.signinPwdLabel)
        self.pwdHLayout.addWidget(self.signinPwdLine)
        self.pwd2HLayout.addWidget(self.signinPwd2Label)
        self.pwd2HLayout.addWidget(self.signinPwd2Line)

        self.allVLayout.addLayout(self.userHLayout)
        self.allVLayout.addLayout(self.pwdHLayout)
        self.allVLayout.addLayout(self.pwd2HLayout)
        self.allVLayout.addWidget(self.signinButton)

        self.setLayout(self.allVLayout)

    # 检测三个输入框内是否含有内容
    def check_input_func(self):
        if self.signinUserLine.text() and self.signinPwdLine.text() and self.signinPwd2Line.text():
            self.signinButton.setEnabled(True)
        else:
            self.signinButton.setEnabled(False)

    # 完成注册功能，检查注册时两次输入的密码是否保持一致，并启动主界面
    def signin_func(self):
        if self.signinPwdLine.text() != self.signinPwd2Line.text():
            QMessageBox.critical(self, '错误', '两次输入的密码不一致！')
        else:
            if userCon.register(self.signinUserLine.text(), self.signinPwdLine.text()):
                QMessageBox.information(self, '提示', '注册成功，请重新登陆')
                self.close()
            else:
                QMessageBox.critical(self, '错误', '注册失败')
                self.signinUserLine.clear()
                self.signinPwdLine.clear()
                self.signinPwd2Line.clear()


'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    loginWindow.show()
    sys.exit(app.exec_())
'''