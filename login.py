from PyQt5.Qt import *
import sys
from database import user_con

userCon = user_con('data.db')


class LoginWindow(QWidget):  # 登录界面
    def __init__(self):
        super(LoginWindow, self).__init__()
        self.resize(300, 100)
        self.setWindowTitle('Login Window')

        self.userLabel = QLabel('用户名:', self)  # 初始化标签，输入框，按钮等内容
        self.pwdLabel = QLabel('密码:', self)
        self.userLine = QLineEdit(self)
        self.pwdLine = QLineEdit(self)
        self.loginButton = QPushButton('登录', self)
        self.signinButton = QPushButton('注册', self)

        self.userAndPwdLayout = QGridLayout()  # 用户名与密码区的摆放
        self.buttonLayout = QHBoxLayout()  # 登录与注册按钮的摆放
        self.allLayout = QVBoxLayout()  # 总体的纵向摆放

        self.lineedit_init()  # 登录界面输入框的初始化
        self.pushbutton_init()  # 按钮的初始化
        self.layout_init()  # 登录框的摆放初始化
        self.signin_page = SigninPage()  # 实例化注册页面

    def lineedit_init(self):
        self.userLine.setPlaceholderText('请输入您的用户名')
        self.pwdLine.setPlaceholderText('请输入您的密码')
        self.pwdLine.setEchoMode(QLineEdit.Password)
        self.userLine.textChanged.connect(self.check_input_func)
        self.pwdLine.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.loginButton.setEnabled(False)
        self.loginButton.clicked.connect(self.check_login_func)
        self.signinButton.clicked.connect(self.show_signin_page_func)

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

    def check_input_func(self):
        if self.userLine.text() and self.pwdLine.text():
            self.loginButton.setEnabled(True)
        else:
            self.loginButton.setEnabled(False)

    def check_login_func(self):
        if userCon.login(self.userLine.text(), self.pwdLine.text()):
            QMessageBox.information(self, 'Information', '登陆成功！')
        else:
            QMessageBox.critical(self, 'Wrong', '用户名或密码错误')
            self.pwdLine.clear()

    def show_signin_page_func(self):
        self.signin_page.exec_()


class SigninPage(QDialog):                                          # 注册窗口
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

    def lineedit_init(self):
        self.signinPwdLine.setEchoMode(QLineEdit.Password)
        self.signinPwd2Line.setEchoMode(QLineEdit.Password)

        self.signinUserLine.textChanged.connect(self.check_input_func)
        self.signinPwdLine.textChanged.connect(self.check_input_func)
        self.signinPwd2Line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.signinButton.setEnabled(False)
        self.signinButton.clicked.connect(self.signin_func)

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

    def check_input_func(self):
        if self.signinUserLine.text() and self.signinPwdLine.text() and self.signinPwd2Line.text():
            self.signinButton.setEnabled(True)
        else:
            self.signinButton.setEnabled(False)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loginWindow = LoginWindow()
    loginWindow.show()
    sys.exit(app.exec_())
