# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/src/res/layout/activity_info.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoDialog(object):
    def setupUi(self, InfoDialog):
        InfoDialog.setObjectName("InfoDialog")
        InfoDialog.resize(566, 421)
        InfoDialog.setStyleSheet("background-color: rgb(41, 41, 49);")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(InfoDialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(20, 50, 521, 291))
        self.plainTextEdit.setStyleSheet("QPlainTextEdit {\n"
"    background-color: gray;\n"
"    background-attachment: scroll;\n"
"    border-style: outset;\n"
"    border-width: 1px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    color: white;\n"
"    font: 13pt \"Monaco\";\n"
"}\n"
"")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(InfoDialog)
        self.label.setGeometry(QtCore.QRect(170, 20, 211, 20))
        self.label.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 19pt \"Gill Sans\"")
        self.label.setObjectName("label")
        self.push_ok = QtWidgets.QPushButton(InfoDialog)
        self.push_ok.setGeometry(QtCore.QRect(200, 360, 166, 31))
        self.push_ok.setStyleSheet("QPushButton {\n"
"    background-color: rgb(105, 105, 105);\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: rgb(127, 127, 127);\n"
"    color: rgb(255, 255, 255);\n"
"    font: 13pt \"Gill Sans\";\n"
"    min-width: 10em;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(127, 127, 127);\n"
"    border-style: inset;\n"
"    color: rgb(36, 255, 6);\n"
"}")
        self.push_ok.setObjectName("push_ok")

        self.retranslateUi(InfoDialog)
        QtCore.QMetaObject.connectSlotsByName(InfoDialog)

    def retranslateUi(self, InfoDialog):
        _translate = QtCore.QCoreApplication.translate
        InfoDialog.setWindowTitle(_translate("InfoDialog", "Info dialog"))
        self.plainTextEdit.setPlainText(_translate("InfoDialog", "Meson-ui (C), permission granted to Michael Brockus, by the creators of Meson and this application is a free software licensed under Apache 2.0, compatible with version 3 of the GNU GPL.\n"
"\n"
"Please note that this license is not compatible with GPL version 2, because it has some requirements that are not in that GPL version. These include certain patent termination and indemnification provisions. The patent termination provision is a good thing, which is why we recommend the Apache 2.0 license for substantial programs over other lax permissive licenses.\n"
"\n"
"Meson-ui is intended to conform to PyQt5 terms of agreements for development of open source projects.  Meson is copyrighted by all members of the Meson development team.  Meson is licensed under the Apache 2.0 license.\n"
"\n"
"Meson is a registered trademark of Jussi Pakkanen.\n"
"\n"
"Meson\'s logo is (C) Jussi Pakkanen and used by the Meson project with specific permission. The Meson logo is used with permission in this app given by Jussi Pakkanen himself."))
        self.label.setText(_translate("InfoDialog", "Meson-ui legel information"))
        self.push_ok.setText(_translate("InfoDialog", "Ok"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InfoDialog = QtWidgets.QDialog()
    ui = Ui_InfoDialog()
    ui.setupUi(InfoDialog)
    InfoDialog.show()
    sys.exit(app.exec_())
