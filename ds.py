from datetime import datetime
import email
from turtle import title
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import sqlite3
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel, QSqlQueryModel
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QCursor
import re
import csv
from numpy import number
from sqlalchemy import Date
import xlsxwriter
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport

count = 0

# Подключение к БД
con = sqlite3.connect('lms')

cursor = con.cursor()
# Определение колонок БД
library_labels = ['Идентификатор книги', 'Название', 'Автор', 'Дата публикации']

user_labels = ['Идентификатор пользователя', 'Электронная почта', 'Номер телефона', 'Имя пользователя', 'Пароль', 'Изображение']

class_labels = ['Идентификатор класса', 'Название класса']

student_labels = ['Идентификатор студента', 'Идентификатор пользователя', 'Идентификатор класса', 'Имя']

teacher_labels = ['Идентификатор учителя', 'Опыт работы', 'Идентификатор пользователя', 'Идентификатор класса', 'Имя']

lesson_labels = ['Идентификатор семинара', 'Тема', 'Дата', 'Идентификатор учителя', 'Идентификатор класса']

test_labels = ['Идентификатор теста', 'Тема', 'Идентификатор учителя']

testres_labels = ['Идентификатор оценки', 'Идентификатор студента', 'Идентификатор теста', 'Идентификатор учителя', 'Оценка']

changeres_labels = ['Идентификатор журнала', 'Вид изменения', 'Идентификатор теста', 'Идентификатор студента',
                     'Идентификатор учителя', 'Оценка', 'Дата изменения']

table_name = 'lesson'

library_labels_dict = {'Идентификатор книги' : 'book_id',
                        'Название' : 'name',
                        'Автор' : 'author',
                        'Дата публикации' : 'public_date'}

user_labels_dict = {'Идентификатор пользователя' : 'user_id',
                    'Электронная почта' : 'email',
                    'Номер телефона' : 'number',
                    'Имя пользователя' : 'username',
                    'Пароль' : 'password',
                    'Изображение' : 'image'}

class_labels_dict = {'Идентификатор класса' : 'class_id',
                    'Название класса' : 'title'}

student_labels_dict = {'Идентификатор студента' : 'student_id',
                        'Идентификатор пользователя' : 'user_id',
                        'Идентификатор класса' : 'class_id',
                        'Имя' : 'name',}

teacher_labels_dict = {'Идентификатор учителя' : 'teacher_id',
                        'Имя' : 'name',
                        'Опыт работы' : 'work_exp',
                        'Идентификатор пользователя' : 'user_id',
                        'Идентификатор класса' : 'class_id'}

lesson_labels_dict = {'Идентификатор семинара' : 'lesson_id',
                        'Тема' : 'title_lesson',
                        'Дата' : 'lesson_date',
                        'Идентификатор учителя' : 'teacher_id',
                        'Идентификатор класса' : 'class_id'}

test_labels_dict = {'Идентификатор теста' : 'test_id',
                        'Тема' : 'title_test',
                        'Идентификатор учителя' : 'teacher_id',}

testres_labels_dict = {'Идентификатор оценки' : 'res_id',
                        'Идентификатор студента' : 'student_id',
                        'Идентификатор теста' : 'test_id',
                        'Идентификатор учителя' : 'teacher_id',
                        'Оценка' : 'grade'}

changeres_labels_dict = {'Идентификатор журнала' : 'change_id',
                        'Вид изменения' : 'type',
                        'Идентификатор теста' : 'test_id',
                        'Идентификатор студента' : 'student_id',
                        'Идентификатор учителя' : 'teacher_id',
                        'Оценка' : 'change_grade',
                        'Дата изменения' : 'change_date'}


class HelloWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("EzEng DataBase")  # заголовок окна
        self.move(0, 0)  # положение окна
        self.resize(1920, 1024)  # размер окна
        self.setWindowIcon(QtGui.QIcon("icon2.jpg"))
        self.label = QLabel('Welcome to EzEng DataBase!', self)
        self.label.resize(900, 200)
        self.label.move(700, 0)
        self.label.setFont(QtGui.QFont("<b>Arial", 40))
        self.label.setStyleSheet('color:White')
        self.continueButton = QPushButton('Начать работу с БД EzEng', self)
        self.continueButton.setStyleSheet('color:blue')
        self.continueButton.resize(200 ,100)
        self.continueButton.move(960, 150)
        self.continueButton.show()
        self.continueButton.clicked.connect(self.hello)

    def hello(self):
        self.close()

class Dialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Input Dialog')
        if table_name == 'library':
            self.line_edit_name = QLineEdit()
            self.line_edit_author = QLineEdit()
            self.line_edit_public = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Название:', self.line_edit_name)
            form_layout.addRow('Автор:', self.line_edit_author)
            form_layout.addRow('Дата публикации:', self.line_edit_public)
        elif table_name == 'user':
            self.line_edit_email = QLineEdit()
            self.line_edit_number = QLineEdit()
            self.line_edit_username = QLineEdit()
            self.line_edit_password = QLineEdit()
            self.line_edit_image = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Электронная почта:', self.line_edit_email)
            form_layout.addRow('Номер телефона:', self.line_edit_number)
            form_layout.addRow('Имя пользователя:', self.line_edit_username)
            form_layout.addRow('Пароль:', self.line_edit_password)
            form_layout.addRow('Изображение:', self.line_edit_image)
        elif table_name == 'class':
            self.line_edit_title_class = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Название класса:', self.line_edit_title_class)
        elif table_name == 'student':
            self.line_edit_name_student = QLineEdit()
            self.line_edit_user_id = QLineEdit()
            self.line_edit_class_id = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Имя:', self.line_edit_name_student)
            form_layout.addRow('Идентификатор пользователя:', self.line_edit_user_id)
            form_layout.addRow('Идентификатор класса:', self.line_edit_class_id)
        elif table_name == 'teacher':
            self.line_edit_name_teacher = QLineEdit()
            self.line_edit_work_exp = QLineEdit()
            self.line_edit_user_id = QLineEdit()
            self.line_edit_class_id = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Имя:', self.line_edit_name_teacher)
            form_layout.addRow('Опыт работы:', self.line_edit_work_exp)
            form_layout.addRow('Идентификатор пользователя:', self.line_edit_user_id)
            form_layout.addRow('Идентификатор класса:', self.line_edit_class_id)
        elif table_name == 'lesson':
            self.line_edit_title_lesson = QLineEdit()
            self.line_edit_lesson_date = QLineEdit()
            self.line_edit_teacher_id = QLineEdit()
            self.line_edit_class_id = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Тема:', self.line_edit_title_lesson)
            form_layout.addRow('Дата:', self.line_edit_lesson_date)
            form_layout.addRow('Идентификатор учителя:', self.line_edit_teacher_id)
            form_layout.addRow('Идентификатор класса:', self.line_edit_class_id)
        elif table_name == 'test':
            self.line_edit_title_test = QLineEdit()
            self.line_edit_teacher_id = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Тема:', self.line_edit_title_test)
            form_layout.addRow('Идентификатор учителя:', self.line_edit_teacher_id)
        elif table_name == 'testres':
            self.line_edit_student_id = QLineEdit()
            self.line_edit_test_id = QLineEdit()
            self.line_edit_teacher_id = QLineEdit()
            self.line_edit_grade = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор студента:', self.line_edit_student_id)
            form_layout.addRow('Идентификатор теста:', self.line_edit_test_id)
            form_layout.addRow('Идентификатор учителя:', self.line_edit_teacher_id)
            form_layout.addRow('Оценка:', self.line_edit_grade)
        elif table_name == 'changeres':
            self.line_edit_type = QLineEdit()
            self.line_edit_test_id = QLineEdit()
            self.line_edit_student_id = QLineEdit()
            self.line_edit_teacher_id = QLineEdit()
            self.line_edit_change_grade = QLineEdit()
            self.line_edit_change_date = QLineEdit()

            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор студента:', self.line_edit_type)
            form_layout.addRow('Идентификатор теста:', self.line_edit_test_id)
            form_layout.addRow('Идентификатор студента:', self.line_edit_student_id)
            form_layout.addRow('Идентификатор учителя:', self.line_edit_teacher_id)
            form_layout.addRow('Оценка:', self.line_edit_change_grade)
            form_layout.addRow('Дата изменения:', self.line_edit_change_date)






        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

class RemoveDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Remove Dialog')
        if table_name == 'library':
            self.line_edit_book_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор книги:', self.line_edit_book_id)
        elif table_name == 'user':
            self.line_edit_user_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор пользователя:', self.line_edit_user_id)
        elif table_name == 'class':
            form_layout = QFormLayout()
            self.line_edit_class_id = QLineEdit()
            form_layout.addRow('Идентификатор класса:', self.line_edit_class_id)
        elif table_name == 'student':
            form_layout = QFormLayout()
            self.line_edit_student_id = QLineEdit()
            form_layout.addRow('Идентификатор студента:', self.line_edit_student_id)
        elif table_name == 'teacher':
            self.line_edit_teacher_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор учителя:', self.line_edit_teacher_id)
        elif table_name == 'lesson':
            self.line_edit_lesson_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор семинара:', self.line_edit_lesson_id)
        elif table_name == 'test':
            self.line_edit_test_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор теста:', self.line_edit_test_id)
        elif table_name == 'testres':
            self.line_edit_res_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор оценки:', self.line_edit_res_id)
        elif table_name == 'changeres':
            self.line_edit_change_id = QLineEdit()
            form_layout = QFormLayout()
            form_layout.addRow('Идентификатор изменения:', self.line_edit_change_id)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)

class FilterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Filter Dialog')
        if table_name == 'library':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(library_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'user':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(user_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'class':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(class_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'student':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(student_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'teacher':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(teacher_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'lesson':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(lesson_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'test':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(test_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'testres':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(testres_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)
        elif table_name == 'changeres':
            self.line_edit_box = QComboBox()
            self.line_edit_box.addItems(changeres_labels)
            self.line_edit_comp_box = QComboBox()
            self.line_edit_value = QLineEdit()
            self.line_edit_comp_box.addItems(['>', '>=', '=', '<=', '<'])
            form_layout = QFormLayout()
            form_layout.addRow('Выберите поле фильтрации:', self.line_edit_box)
            form_layout.addRow('Выберите знак сравнения', self.line_edit_comp_box)
            form_layout.addRow('Введите значение для сравнения', self.line_edit_value)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)







class MainWindow(QMainWindow):  # главное окно
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self._createActions()
        self._createMenuBar()
        self.setWindowIcon(QtGui.QIcon("icon2.jpg"))

    def addRow(self):
        if table_name == 'library':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            name = str(inputDialog.line_edit_name.text())
            author = str(inputDialog.line_edit_author.text())
            public_date = datetime(inputDialog.line_edit_public.text())
            if not name or not author or not public_date:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values = [name, author, public_date]
            print(values[1])
            print(type(values))
            cursor.execute(f'INSERT INTO library VALUES (NULL, "{values[0]}", "{values[1]}", "{values[2]}");')
            print('запрос успешен')
            self._showTable_library()
        elif table_name == 'user':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            email = str(inputDialog.line_edit_email.text())
            number = str(inputDialog.line_edit_number.text())
            username = str(inputDialog.line_edit_username.text())
            password = str(inputDialog.line_edit_password.text())
            image = str(inputDialog.line_edit_image.text())

            if not email or not number or not username or not password:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values = [email, number, username, password, image]
            print(values[1])
            # print(type(values))
            cursor.execute(
                f'INSERT INTO user VALUES (NULL, "{values[0]}", "{values[1]}", "{values[2]}", "{values[3]}", "{values[4]}");')
            print('запрос успешен')
            self._showTable_user()
        elif table_name == 'class':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            title = str(inputDialog.line_edit_title_class.text())

            if not title:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values = [title]
            print(values[0])
            # print(type(values))
            cursor.execute(
                f'INSERT INTO class VALUES (NULL, "{values[0]}");')
            print('запрос успешен')
            self._showTable_class()
        elif table_name == 'student':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

           
            user_id = int(inputDialog.line_edit_user_id.text())
            class_id = int(inputDialog.line_edit_class_id.text())
            name = str(inputDialog.line_edit_name_student.text())

            if not user_id or not class_id or not name:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values =  [user_id, class_id, name]
            print(values[1])
            # print([type(value) for value in values])
            cursor.execute(f'INSERT INTO student VALUES (NULL, {values[0]}, {values[1]}, "{values[2]}");')
            print('запрос успешен')
            self._showTable_student()
        elif table_name == 'teacher':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            name = str(inputDialog.line_edit_name_teacher.text())
            work_exp = str(inputDialog.line_edit_work_exp.text())
            user_id = int(inputDialog.line_edit_user_id.text())
            class_id = int(inputDialog.line_edit_class_id.text())

            if not name or not work_exp or not user_id or not class_id:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values =  [work_exp, user_id, class_id, name]
            print(values[1])
            # print([type(value) for value in values])
            cursor.execute(f'INSERT INTO teacher VALUES (NULL, "{values[0]}", {values[1]}, {values[2]}, "{values[3]}");')
            print('запрос успешен')
            self._showTable_teacher()
        elif table_name == 'lesson':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            title = str(inputDialog.line_edit_title_lesson.text())
            date = datetime(inputDialog.line_edit_lesson_date.text())
            teacher_id = int(inputDialog.line_edit_teacher_id.text())
            class_id = int(inputDialog.line_edit_class_id.text())

            if not title or not class_id or not date or not teacher_id:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values =  [teacher_id, title, date, class_id]
            print(values[1])
            # print([type(value) for value in values])
            cursor.execute(f'INSERT INTO lesson VALUES (NULL, {values[0]}, "{values[1]}", "{values[2]}", {values[3]});')
            print('запрос успешен')
            self._showTable_lesson()
        elif table_name == 'test':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            title = str(inputDialog.line_edit_title_test.text())
            teacher_id = int(inputDialog.line_edit_teacher_id.text())

            if not title or not teacher_id:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values =  [teacher_id, title]
            print(values[1])
            # print([type(value) for value in values])
            cursor.execute(f'INSERT INTO test VALUES (NULL, {values[0]}, "{values[1]}");')
            print('запрос успешен')
            self._showTable_test()
        elif table_name == 'testres':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            student_id = int(inputDialog.line_edit_student_id.text())
            test_id = int(inputDialog.line_edit_test_id.text())
            teacher_id = int(inputDialog.line_edit_teacher_id.text())
            grade = int(inputDialog.line_edit_grade.text())

            if not student_id or not test_id or not teacher_id or not grade:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values =  [student_id, test_id, teacher_id, grade]
            print(values[1])
            # print([type(value) for value in values])
            cursor.execute(f'INSERT INTO testres VALUES (NULL, {values[0]}, {values[1]}, {values[2]}, {values[3]});')
            print('запрос успешен')
            self._showTable_testres()
        elif table_name == 'changeres':
            inputDialog = Dialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return

            type = str(inputDialog.line_edit_type.text())
            test_id = int(inputDialog.line_edit_test_id.text())
            student_id = int(inputDialog.line_edit_student_id.text())
            teacher_id = str(inputDialog.line_edit_teacher_id.text())
            grade = int(inputDialog.line_edit_change_grade.text())
            change_data = datetime(inputDialog.line_edit_change_grade.text())

            if not type or not test_id or not student_id or not teacher_id or not grade or not change_data:
                msg = QMessageBox.information(self, 'Внимание', 'Заполните пожалуйста все поля.')
                return
            values =  [type, test_id, student_id, teacher_id, grade, change_data]
            print(values[1])
            # print([type(value) for value in values])
            cursor.execute(f'INSERT INTO changeres VALUES (NULL, "{values[0]}", {values[1]}, {values[2]}, {values[2]}, {values[2]}, "{values[2]}");')
            print('запрос успешен')
            self._showTable_changeres()


    def deleteRow(self):
        if table_name == 'library':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_book_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM library WHERE book_id = {delete_id}')
            self._showTable_library()
        elif table_name == 'user':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_user_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM user WHERE user_id = {delete_id}')
            self._showTable_user()
        elif table_name == 'class':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_class_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM class WHERE class_id = {delete_id}')
            self._showTable_class()
        elif table_name == 'student':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_student_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM student WHERE student_id = {delete_id}')
            self._showTable_student()
        elif table_name == 'teacher':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_teacher_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM teacher WHERE teacher_id = {delete_id}')
            self._showTable_teacher()
        elif table_name == 'lesson':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_lesson_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM lesson WHERE lesson_id = {delete_id}')
            self._showTable_lesson()
        elif table_name == 'test':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_test_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM test WHERE test_id = {delete_id}')
            self._showTable_test()
        elif table_name == 'testres':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_testres_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM testres WHERE testres_id = {delete_id}')
            self._showTable_testres()
        elif table_name == 'changeres':
            inputDialog = RemoveDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            delete_id = int(inputDialog.line_edit_change_id.text())
            print(delete_id)
            cursor.execute(f'DELETE FROM changeres WHERE change_id = {delete_id}')
            self._showTable_changeres()


    def filterRows(self):
        if table_name == 'library':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from library;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from library where {library_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 4):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row,rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'user':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from user;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from user where {user_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 6):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'class':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from class;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from class where {class_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 2):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'student':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from student;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from student where {student_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 4):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'teacher':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from teacher;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from teacher where {teacher_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 5):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'lesson':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from lesson;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from lesson where {lesson_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 5):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'test':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from test;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from test where {test_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 3):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'testres':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from testres;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from testres where {testres_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 5):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)
        elif table_name == 'changeres':
            inputDialog = FilterDialog()
            rez = inputDialog.exec()
            if not rez:
                msg = QMessageBox.information(self, 'Внимание', 'Диалог сброшен.')
                return
            field = inputDialog.line_edit_box.currentText()
            comp = inputDialog.line_edit_comp_box.currentText()
            value = inputDialog.line_edit_value.text()
            row = 0
            cursor.execute(f'Select * from changeres;')
            rows = len(cursor.fetchall())
            cursor.execute(f'Select * from changeres where {changeres_labels_dict[field]} {comp} {value};')
            while True:
                sqlRow = cursor.fetchone()
                print(sqlRow)
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 7):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
            print(range(row, rows))
            for i in range(row, rows):
                self.table.setRowHidden(i, True)










    def findName(self, s):
        name = self.search.text().lower()
        for row in range(self.table.rowCount()):
            items = []
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                items.append(item.text())
                self.table.setRowHidden(row, name not in item.text().lower())
            print(items)
            flags = []
            for i in items:
                flags.append(name in i.lower())
            self.table.setRowHidden(row, sum(flags) == 0)

    def _showTable_user(self):
        global table_name
        table_name = 'user'
        cursor.execute('Select * from user')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))  ##set number of rows
        self.table.setColumnCount(6)  # Устанавливаем три колонки
        self.table.setHorizontalHeaderLabels(user_labels)
        row = 0
        cursor.execute('Select * from user')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 6):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_class(self):
        global table_name
        table_name = 'class'
        cursor.execute('Select * from class')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))  ##set number of rows
        self.table.setColumnCount(2)  # Устанавливаем три колонки
        self.table.setHorizontalHeaderLabels(class_labels)
        row = 0
        cursor.execute('Select * from class')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 2):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_student(self):
        global table_name
        table_name = 'student'
        cursor.execute('Select * from student')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))  ##set number of rows
        self.table.setColumnCount(4)  # Устанавливаем три колонки
        self.table.setHorizontalHeaderLabels(student_labels)
        row = 0
        cursor.execute('Select * from student')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 4):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)
    def _showTable_teacher(self):
        global table_name
        table_name = 'teacher'
        cursor.execute('Select * from teacher')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(teacher_labels)
        row = 0
        cursor.execute('Select * from teacher')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 5):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_lesson(self):
        global table_name
        table_name = 'lesson'
        cursor.execute('Select * from lesson')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(lesson_labels)
        row = 0
        cursor.execute('Select * from lesson')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 5):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_test(self):
        global table_name
        table_name = 'test'
        cursor.execute('Select * from test')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(test_labels)
        row = 0
        cursor.execute('Select * from test')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 3):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_testres(self):
        global table_name
        table_name = 'testres'
        cursor.execute('Select * from testres')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(testres_labels)
        row = 0
        cursor.execute('Select * from testres')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 5):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_changeres(self):
        global table_name
        table_name = 'changeres'
        cursor.execute('Select * from changeres')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(changeres_labels)
        row = 0
        cursor.execute('Select * from changeres')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 7):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)

    def _showTable_library(self):
        global table_name
        table_name = 'library'
        cursor.execute('Select * from library')
        allSQLRows = cursor.fetchall()
        self.table.setRowCount(len(allSQLRows))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(library_labels)
        row = 0
        cursor.execute('Select * from library')
        while True:
            sqlRow = cursor.fetchone()
            if sqlRow is None:
                break  ##stops while loop if there is no more lines in sql table
            for col in range(0, 4):  ##otherwise add row into tableWidget
                self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
            row += 1
        self.addButton = QPushButton('Добавить', self)
        self.addButton.move(1650, 450)
        self.addButton.resize(200, 50)
        self.addButton.show()
        self.selectButton = QPushButton('Фильтр', self)
        self.selectButton.move(1650, 550)
        self.selectButton.resize(200, 50)
        self.selectButton.show()
        self.deleteButton = QPushButton('Удалить', self)
        self.deleteButton.move(1650, 650)
        self.deleteButton.resize(200, 50)
        self.deleteButton.show()
        self.addButton.clicked.connect(self.addRow)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.selectButton.clicked.connect(self.filterRows)


    # Сортировка таблицы по нажатию на столбец
    def click_handler_sort(self, e):
        global count
        if count % 2 == 0:
            desc = 'desc'
        else:
            desc = 'asc'
        if table_name == 'user':
            cursor.execute(f'select * from user order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels(user_labels)
            row = 0
            cursor.execute(f'select * from user order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 6):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'class':
            cursor.execute(f'Select * from class order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(class_labels)
            row = 0
            cursor.execute(f'Select * from class order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 2):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'student':
            cursor.execute(f'Select * from student order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels(student_labels)
            row = 0
            cursor.execute(f'Select * from student order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 4):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'teacher':
            cursor.execute(f'Select * from teacher order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(teacher_labels)
            row = 0
            cursor.execute(f'Select * from teacher order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 5):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'lesson':
            cursor.execute(f'Select * from lesson order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(lesson_labels)
            row = 0
            cursor.execute(f'Select * from lesson order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 5):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'test':
            cursor.execute(f'Select * from test order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(test_labels)
            row = 0
            cursor.execute(f'Select * from test order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 3):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'testres':
            cursor.execute(f'Select * from testres order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(testres_labels)
            row = 0
            cursor.execute(f'Select * from testres order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 5):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'changeres':
            cursor.execute(f'Select * from changeres order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))
            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(changeres_labels)
            row = 0
            cursor.execute(f'Select * from changeres order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 7):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        elif table_name == 'library':
            cursor.execute(f'Select * from library order by {e+1} {desc}')
            allSQLRows = cursor.fetchall()
            self.table.setRowCount(len(allSQLRows))  ##set number of rows
            self.table.setColumnCount(4)  # Устанавливаем три колонки
            self.table.setHorizontalHeaderLabels(library_labels)
            row = 0
            cursor.execute(f'Select * from library order by {e+1} {desc}')
            while True:
                sqlRow = cursor.fetchone()
                if sqlRow is None:
                    break  ##stops while loop if there is no more lines in sql table
                for col in range(0, 4):  ##otherwise add row into tableWidget
                    self.table.setItem(row, col, QTableWidgetItem(str((sqlRow[col]))))
                row += 1
        count += 1




    def fileSave(self):
        fileName, ok = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            ".",
            "All Files(*.xlsx)"
        )
        if not fileName:
            return

        _list = []
        model = self.table.model()
        for row in range(model.rowCount()):
            _r = []
            for column in range(model.columnCount()):
                _r.append("{}".format(model.index(row, column).data() or ""))
            _list.append(_r)
        print(fileName)

        workbook = xlsxwriter.Workbook(fileName)
        worksheet = workbook.add_worksheet()

        for r, row in enumerate(_list):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        workbook.close()
        msg = QMessageBox.information(
            self,
            "Успешно!",
            f"Данные сохранены в файле: \n{fileName}"
        )

    def saveToPDF(self):
        fileName, ok = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            ".",
            "All Files(*.pdf)"
        )
        if not fileName:
            return

        model = self.table.model()
        printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.PrinterResolution)
        printer.setOutputFormat(QtPrintSupport.QPrinter.PdfFormat)
        printer.setPaperSize(QtPrintSupport.QPrinter.A4)
        printer.setOrientation(QtPrintSupport.QPrinter.Landscape)
        printer.setOutputFileName(fileName)

        doc = QtGui.QTextDocument()

        html = """<html>
        <head>
        <style>
        table, th, td {
          border: 1px solid black;
          border-collapse: collapse;
        }
        </style>
        </head>"""
        html += "<table><thead>"
        html += "<tr>"
        for c in range(model.columnCount()):
            html += "<th>{}</th>".format(model.headerData(c, QtCore.Qt.Horizontal))

        html += "</tr></thead>"
        html += "<tbody>"
        for r in range(model.rowCount()):
            html += "<tr>"
            for c in range(model.columnCount()):
                html += "<td>{}</td>".format(model.index(r, c).data() or "")
            html += "</tr>"
        html += "</tbody></table>"
        doc.setHtml(html)
        doc.setPageSize(QtCore.QSizeF(printer.pageRect().size()))
        doc.print_(printer)
        msg = QMessageBox.information(
            self,
            "Успешно!",
            f"Данные сохранены в файле: \n{fileName}"
        )




    def _createActions(self):
        # Creating action using the first constructor
        self.userAction = QAction(self)
        self.userAction.setText("Пользователи")
        self.userAction.clickAction = QAction(self.userAction)
        # Creating actions using the second constructor
        self.classAction = QAction("Классы", self)
        self.studentAction = QAction("Студенты", self)
        self.teacherAction = QAction("Учителя", self)
        self.lessonAction = QAction("Семинары", self)
        self.testAction = QAction("Тесты", self)
        self.testresAction = QAction("Оценки", self)
        self.changeresAction = QAction("Оценки Log ", self)
        self.libAction = QAction("Библиотека", self)
        self.pdfAction = QAction('PDF-файл', self)
        self.xlsAction = QAction('Excel-файл', self)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("Таблицы", self)
        self.table = QTableWidget(self)
        self.table.horizontalHeader().setDefaultSectionSize(200)
        self.table.move(0, 60)
        self.table.resize(1600, 1000)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.userAction)
        fileMenu.addAction(self.classAction)
        fileMenu.addAction(self.studentAction)
        fileMenu.addAction(self.teacherAction)
        fileMenu.addAction(self.lessonAction)
        fileMenu.addAction(self.testAction)
        fileMenu.addAction(self.testresAction)
        fileMenu.addAction(self.changeresAction)
        fileMenu.addAction(self.libAction)
        self.userAction.triggered.connect(self._showTable_user)
        self.classAction.triggered.connect(self._showTable_class)
        self.studentAction.triggered.connect(self._showTable_student)
        self.teacherAction.triggered.connect(self._showTable_teacher)
        self.lessonAction.triggered.connect(self._showTable_lesson)
        self.testAction.triggered.connect(self._showTable_test)
        self.testresAction.triggered.connect(self._showTable_testres)
        self.changeresAction.triggered.connect(self._showTable_changeres)
        self.libAction.triggered.connect(self._showTable_library)
        self.xlsAction.triggered.connect(self.fileSave)
        self.pdfAction.triggered.connect(self.saveToPDF)
        self.table.horizontalHeader().sectionDoubleClicked.connect(self.click_handler_sort)

        # Creating menus using a title
        printMenu = menuBar.addMenu('Экспорт таблицы')
        printMenu.addAction(self.pdfAction)
        printMenu.addAction(self.xlsAction)

    def setupUi(self):
        self.setWindowTitle("EzEng DataBase")  # заголовок окна
        self.move(0, 0)  # положение окна
        self.resize(1920, 1024)  # размер окна
        self.search = QLineEdit('', self)
        self.search.setToolTip('Поиск по таблице')
        self.search.setPlaceholderText('Поиск')
        self.search.move(20, 30)
        self.search.resize(500, 20)
        self.search.textChanged.connect(self.findName)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow()
    win.show()
    helloWindow = HelloWindow()
    helloWindow.setObjectName("HelloWindow")
    helloWindow.setStyleSheet("#HelloWindow{border-image:url(icon.jpg)}")
    helloWindow.show()
    sys.exit(app.exec_())
