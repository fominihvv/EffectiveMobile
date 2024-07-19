from biblioteka.services import biblioteka, Book


def get_menu_command() -> int:
    while True:
        print('МЕНЮ управления библиотекой:')
        print('----------------------------')
        print('1. Добавить книгу')
        print('2. Удалить книгу')
        print('3. Поиск книги')
        print('4. Отображение всех книг')
        print('5. Изменить статус книги')
        print('6. Выход')
        print('----------------------------')

        try:
            return int(input('Выберите пункт меню: '))
        except ValueError:
            print('Неверное значение. Пожалуйста, введите целое число.')


def add_book():
    while True:
        print('Добавление книги в библиотеку')
        print('----------------------------')
        title = input('Введите название книги: ')
        author = input('Введите автора книги: ')
        while True:
            try:
                year = int(input('Введите год издания книги: '))
                break
            except ValueError:
                print('Неверное значение. Пожалуйста, введите целое число.')
        break
    book = Book(title, author, year)
    if biblioteka.check_book(book):
        print('Такая книга уже есть в библиотеке')
    else:
        biblioteka.add_book(book)


def delete_book():
    pass


def search_book():
    pass


def show_all_books():
    pass


def change_status():
    pass


def exit():
    biblioteka.save_biblioteka()
    raise SystemExit
