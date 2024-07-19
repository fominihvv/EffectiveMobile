from menu import menu

while True:
    command = menu.get_menu_command()
    match command:
        case 1: menu.add_book()
        case 2: menu.delete_book()
        case 3: menu.search_book()
        case 4: menu.show_all_books()
        case 5: menu.change_status()
        case 6: menu.exit()


