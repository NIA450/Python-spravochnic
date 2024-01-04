# Это телефонный справочник на Python c ф-ями:
# добавление контакта в БД, 
# поиск контакта
# редактирование контакта. 


import sqlite3
import easygui

# Подключение к БД
conn = sqlite3.connect('contacts.db')
c = conn.cursor()

# Создание таблицы контактов
c.execute('''
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(16) NOT NULL,
        last_name VARCHAR(16),
        phone VARCHAR(14) NOT NULL,
        comment TEXT)
    ''')
conn.commit()

def contact_add():
    # Создание нового id для контакта
    c.execute('SELECT MAX(id) FROM contacts')
    max_id = c.fetchone()[0]
    if max_id is None:
        new_id = 1
    else:
        new_id = max_id + 1

    # Запрос ввода имени
    while True:
        name = easygui.enterbox('Введите ваше имя (не более 16 символов):')
        if len(name) <= 16:
            break
        else:
            easygui.msgbox('Поле заполнено не верно')

    # Запрос ввода фамилии
    last_name = easygui.enterbox('Введите вашу фамилию (не более 16 символов):')

    # Запрос ввода телефона
    while True:
        phone = easygui.enterbox('Введите номер телефона (не более 14 цифр):')
        if len(phone) <= 14 and phone.isdigit():
            break
        else:
            easygui.msgbox('Поле заполнено не верно')

    # Запрос ввода комментария
    comment = easygui.enterbox('Введите комментарий (не более 265 символов):')

    # Проверка наличия телефонного номера в базе данных
    c.execute('SELECT id FROM contacts WHERE phone=?', (phone,))
    existing_contact = c.fetchone()

    if existing_contact:
        result = easygui.buttonbox('Контакт с таким номером существует. Добавить повторно контакт?', choices=['Да', 'Нет'])
        if result == 'Да':
            name += ' (Второй)'
        else:
            return

    # Запись контакта в базу данных
    c.execute('INSERT INTO contacts VALUES (?, ?, ?, ?, ?)', (new_id, name, last_name, phone, comment))
    conn.commit()

    easygui.msgbox(f'Контакт "{name} {last_name} {phone}" успешно записан.')

def contact_search():
    # Запрос на поиск
    search_term = easygui.enterbox('Кого ищем?')

    # Поиск по имени, фамилии и телефону
    c.execute('SELECT * FROM contacts WHERE first_name LIKE ? OR last_name LIKE ? OR phone LIKE ?', 
              (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
    results = c.fetchall()

    if len(results) == 0:
        easygui.msgbox('Контакты не найдены')
    elif len(results) == 1:
        contact = results[0]
        contact_menu(contact)
    else:
        # Вывод списка контактов
        choices = []
        for contact in results:
            choices.append(f'{contact[0]} - {contact[1]} {contact[2]} {contact[3]}')
        
        choice = easygui.buttonbox('Найдены несколько контактов, выберите контакт:', choices=choices)
        index = choices.index(choice)
        contact = results[index]
        contact_menu(contact)
        
        def contact_edit(contact):
    # Запрос выбора поля для редактирования
    while True:
        field = easygui.buttonbox('Какое поле редактируем?', choices=['Имя', 'Фамилия', 'Телефон', 'Комментарий'])
        
        if field == 'Имя':
            while True:
                name = easygui.enterbox('Введите новое имя (не более 16 символов):')
                if len(name) <= 16:
                    break
                else:
                    easygui.msgbox('Поле заполнено не верно')
            c.execute('UPDATE contacts SET first_name=? WHERE id=?', (name, contact[0]))
        
        elif field == 'Фамилия':
            last_name = easygui.enterbox('Введите новую фамилию (не более 16 символов):')
            c.execute('UPDATE contacts SET last_name=? WHEREid=?', (last_name, contact[0]))
        
        elif field == 'Телефон':
            while True:
                phone = easygui.enterbox('Введите новый телефон (не более 14 цифр):')
                if len(phone) <= 14 and phone.isdigit():
                    break
                else:
                    easygui.msgbox('Поле заполнено не верно')
                    c.execute('UPDATE contacts SET phone=? WHERE id=?', (phone, contact[0]))
                    
        elif field == 'Комментарий':
            comment = easygui.enterbox('Введите новый комментарий (не более 265 символов):')
            c.execute('UPDATE contacts SET comment=? WHERE id=?', (comment, contact[0]))
            conn.commit()         
            result = easygui.buttonbox('Продолжить редактирование?', choices=['Да', 'Нет'])
            if result == 'Нет':
                break
        easygui.msgbox('Контакт успешно отредактирован.')

def contact_delete(contact):
    result = easygui.buttonbox(f'Удалить контакт "{contact[1]} {contact[2]} {contact[3]}"?', choices=['Да', 'Нет'])
    if result == 'Да':
        c.execute('DELETE FROM contacts WHERE id=?', (contact[0],))
        conn.commit()
        easygui.msgbox('Контакт успешно удален.')

def contact_menu(contact):
    choices = ['Просмотреть', 'Редактировать', 'Удалить']
    choice = easygui.buttonbox(f'Выбран контакт "{contact[1]} {contact[2]} {contact[3]}", выберите действие:',
    choices=choices)
    if choice == 'Просмотреть':
        easygui.msgbox(f'Имя: {contact[1]}\nФамилия: {contact[2]}\nТелефон: {contact[3]}\nКомментарий: {contact[4]}')
    elif choice == 'Редактировать':
        contact_edit(contact)
    elif choice == 'Удалить':
        contact_delete(contact)

ef main_menu():
    choices = ['Добавить', 'Поиск']
    while True:
        choice = easygui.buttonbox('Выберите действие:', choices=choices)
        if choice == 'Добавить':
            contact_add()
        elif choice == 'Поиск':
            contact_search()
            result = easygui.buttonbox('Вернуться в главное меню?', choices=['Да', 'Нет'])
            if result == 'Нет':
                break
            main_menu()

# Закрытие соединения с базой данных
conn.close()