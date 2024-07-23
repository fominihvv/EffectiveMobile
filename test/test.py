from biblioteka.services import Library


def run_test():
    l1 = Library()
    l2 = Library()
    assert l1 == l2, "Должен создаваться только один экземпляр библиотеки"
    assert len(l1.books) == 0, "Должна создаваться пустая библиотека"

    l1.add_book('title1', 'author1', 2000)
    l1.add_book('title2', 'author2', 2001)
    l1.add_book('title3', 'author3', 2002)

    assert len(l1.books) == 3, "В библиотеке должно быть 3 книги"
    assert l1.get_status(1) == 'в наличии', "Книга должна иметь статус 'В наличии'"

    l1.change_status(1, 'выдана')
    assert l1.get_status(1) == 'выдана', "Книга должна иметь статус 'выдана'"

    l1.delete_book(1)
    assert len(l1.books) == 2, "В библиотеке должно остаться 2 книги"
    assert l1.get_status(1) is None, "Книга должна быть удалена"

    l1.add_book('title2', 'author2', 2001)
    assert len(l1.books) == 2, "В библиотеке должно быть 2 книги"

    l1.delete_book(1)
    assert len(l1.books) == 2, "В библиотеке должно остаться 2 книги"

    l1.add_book('title1', 'author2', 2000)
    assert len(l1.search_books('', 'author2')) == 2, "В выдаче должно быть 2 книги"
    assert len(l1.search_books('', 'thor')) == 3, "В выдаче должно быть 2 книги"
    assert len(l1.search_books()) == 3, "В выдаче должно быть 3 книги"

    print('Все тесты пройдены!')


if __name__ == '__main__':
    run_test()
