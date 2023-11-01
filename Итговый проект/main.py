import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.db = db
        self.init_main()

    # Метод инициализации виджетов
    def init_main(self):
        # Тулбар
        toolbar = tk.Frame(bg='#9999ff', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        # Кнопка добавления
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar,
                            image=self.add_img,
                            bg='#9999ff', bd=0,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Кнопка редактирования
        self.upd_img = tk.PhotoImage(file='./img/upd.png')
        btn_upd = tk.Button(toolbar,
                            image=self.upd_img,
                            bg='#9999ff', bd=0,
                            command=self.open_update)
        btn_upd.pack(side=tk.LEFT)

        # Кнопка удаления
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del = tk.Button(toolbar,
                            image=self.del_img,
                            bg='#9999ff', bd=0,
                            command=self.del_records)
        btn_del.pack(side=tk.LEFT)

        # Кнопка поиска
        self.srh_img = tk.PhotoImage(file='./img/search.png')
        btn_srh = tk.Button(toolbar,
                            image=self.srh_img,
                            bg='#9999ff', bd=0,
                            command=self.open_search)
        btn_srh.pack(side=tk.LEFT)

        # Кнопка обновления
        self.ref_img = tk.PhotoImage(file='./img/refresh.png')
        btn_ref = tk.Button(toolbar,
                            image=self.ref_img,
                            bg='#9999ff', bd=0,
                            command=self.view_records)
        btn_ref.pack(side=tk.LEFT)

        # Таблица для вывода информации для контактов
        self.tree = ttk.Treeview(self,
                                 columns=('ID', 'name', 'phone', 'email', 'salary'),
                                 show='headings', height=18)
        # Настройки для столбцов
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=150, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        # Задаем подписи столбцам
        self.tree.heading('ID', text='id')
        self.tree.heading('name', text='Имя')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='Электроная Почта')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack()
        self.view_records()

        # Создание скроллбара (полоса прокрутки)
        scroll = tk.Scrollbar(root, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления в БД (посредник)
    def record(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Метод редактирования в БД
    def upd_record(self, name, phone, email, salary):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''
            UPDATE employees SET name = ?, phone = ?, email = ?, salary = ?
            WHERE id = ?
            ''', (name, phone, email, salary, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления в БД
    def del_records(self):
        for i in self.tree.selection():
            self.db.cur.execute('DELETE FROM employees WHERE id = ?',
                                (self.tree.set(i, '#1'),))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска в БД
    def srh_records(self, name):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # Перезаполнение виджета таблицы
    def view_records(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.db.cur.execute('SELECT * FROM employees')
        r = self.db.cur.fetchall()
        for i in r:
            self.tree.insert('', 'end', values=i)

    # Метод открытия окна добавления
    def open_child(self):
        Child()

    # Метод открытия окна редактирования
    def open_update(self):
        Update()

    # Метод открытия окна поиска
    def open_search(self):
        Search()


# Класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    # Метод для создания виджетов дочернего окна
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        # Перехватываем события происходящие в приложении
        self.grab_set()
        # Перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_phone = tk.Label(self, text='Телефон')
        label_email = tk.Label(self, text='Электронная почта')
        label_salary = tk.Label(self, text='Зарплата')
        label_name.place(x=60, y=30)
        label_phone.place(x=60, y=60)
        label_email.place(x=60, y=90)
        label_salary.place(x=60, y=120)

        self.entry_name = tk.Entry(self)
        self.entry_phone = tk.Entry(self)
        self.entry_email = tk.Entry(self)
        self.entry_salary = tk.Entry(self)
        self.entry_name.place(x=220, y=30)
        self.entry_phone.place(x=220, y=60)
        self.entry_email.place(x=220, y=90)
        self.entry_salary.place(x=220, y=120)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=250, y=160)

        self.btn_add = tk.Button(self, text='Добавить')
        self.btn_add.bind('<Button-1>', lambda ev: self.view.record(self.entry_name.get(),
                                                                    self.entry_phone.get(),
                                                                    self.entry_email.get(),
                                                                    self.entry_salary.get()))
        self.btn_add.place(x=320, y=160)


# Класс редактирования
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Изменение информации')
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text='Изменить')
        self.btn_upd.bind('<Button-1>', lambda ev: self.view.upd_record(self.entry_name.get(),
                                                                        self.entry_phone.get(),
                                                                        self.entry_email.get(),
                                                                        self.entry_salary.get()))
        self.btn_upd.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_upd.place(x=320, y=160)

    # Метод автозаполнения формы
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT *  FROM employees WHERE id = ?', (id,))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Класс поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    # Метод для создания виджетов дочернего окна
    def init_search(self):
        self.title('Поиск сотрудника')
        self.geometry('400x100')
        self.resizable(False, False)
        # Перехватываем события происходящие в приложении
        self.grab_set()
        # Перехватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=60, y=30)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=220, y=30)

        btn_close = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_close.place(x=270, y=70)

        self.btn_srh = tk.Button(self, text='Найти')
        self.btn_srh.bind('<Button-1>', lambda ev: self.view.srh_records(self.entry_name.get()))
        self.btn_srh.bind('<Button-1>', lambda ev: self.destroy(),
                          add='+')
        self.btn_srh.place(x=340, y=70)


# Класс БД
class Db:
    # Создание соединения, курсора и таблицы (если её нет)
    def __init__(self):
        self.conn = sqlite3.connect('employees.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        phone TEXT,
                        email TEXT,
                        salary INTEGER
        )''')

    # Метод добавления в БД
    def insert_data(self, name, phone, email, salary):
        self.cur.execute('''
            INSERT INTO employees (name, phone, email, salary)
            VALUES (?, ?, ?, ?)
        ''', (name, phone, email, salary))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Список сотрудников компании')
    root.geometry('665x450')
    root.resizable(False, False)
    db = Db()
    app = Main(root)
    app.pack()
    root.mainloop()
