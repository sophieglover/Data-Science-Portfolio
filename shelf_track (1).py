# import library
import sqlite3
from contextlib import closing


def get_connection():
    return sqlite3.connect("ebookstore.db")


def databases():
    """
    Creates tables 'book' and 'author' if they don't
    already exist.
    Adds data to the tables.
    """

    with closing(get_connection()) as db:

        with closing(db.cursor()) as cursor:

            # create a table called 'book'
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS book(
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    authorID INTEGER,
                    qty INTEGER,
                    FOREIGN KEY(authorID) REFERENCES author(id)
                )
            """
            )

            db.commit()

            # add to the table 'book'
            book_list = [
                (3001, "A Tale of Two Cities", 1290, 30),
                (3002, "Harry Potter and the Philosopher's Stone", 8937, 40),
                (3003, "The Lion, the Witch and the Wardrobe", 2356, 25),
                (3004, "The Lord of the Rings", 6380, 37),
                (3005, "Alice's Adventures in Wonderland", 5620, 12),
            ]

            cursor.executemany(
                """INSERT OR IGNORE INTO book(id, title, authorID, qty) 
                VALUES(?, ?, ?, ?)""",
                book_list,
            )

            db.commit()

            # create a table called 'author'
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS author(
                id INTEGER PRIMARY KEY,
                name TEXT,
                country TEXT
                )
            """
            )

            db.commit()

            # add to the table 'author'
            author_list = [
                (1290, "Charles Dickens", "England"),
                (8937, "J.K. Rowling", "England"),
                (2356, "C.S. Lewis", "Ireland"),
                (6380, "J.R.R. Tolkien", "South Africa"),
                (5620, "Lewis Carroll", "England"),
            ]

            cursor.executemany(
                """INSERT OR IGNORE INTO author(id, name, country) 
                VALUES(?, ?, ?)""",
                author_list,
            )

            db.commit()


def enter_book():
    """
    Allows the user to enter information about a new book.
    Checks that the information is valid.
    The new book is then entered into the database.
    """

    with closing(get_connection()) as db:

        with closing(db.cursor()) as cursor:

            print("Please enter the following information:\n")

            while True:

                id = input("Book ID:")

                if len(id) == 4:

                    try:
                        id = int(id)
                        break
                    except ValueError:
                        print("Error: ID entered not an integer.")

                else:
                    print("Error: ID must be 4 digits.")

            while True:

                author_id = input("Author ID:")

                if len(author_id) == 4:

                    try:
                        author_id = int(author_id)
                        break
                    except ValueError:
                        print("Error: Author ID entered not an integer.")

                else:
                    print("Error: Author ID must be 4 digits.")

            title = input("Title:")

            while True:

                qty = input("Quantity:")

                try:
                    qty = int(qty)
                    break
                except ValueError:
                    print("Error: Quantity entered not an integer.")

            cursor.execute(
                """INSERT INTO book VALUES (?, ?, ?, ?)""",
                (id, title, author_id, qty),
            )

            db.commit()

            print("\nDatabase successfully updated!\n")


def update_book():
    """
    Allows the user to update the quantity or author
    information of a book by inputting its ID.
    Updates the quantity/information in the database.
    """

    with closing(get_connection()) as db:

        with closing(db.cursor()) as cursor:

            id = input("Please enter the ID of the book you wish to update:\n")

            cursor.execute(
                """SELECT b.title, b.qty, b.authorID, a.name, a.country 
            FROM book b 
            INNER JOIN author a ON b.authorID = a.id 
            WHERE b.id = ?""",
                (id,),
            )

            book_info = cursor.fetchall()

            if not book_info:

                print(f"No book found with ID {id}")
                return

            for book in book_info:
                print(f"Title: {book[0]}")
                print(f"Quantity: {book[1]}")
                author_id = book[2]
                print(f"Author: {book[3]}")
                print(f"Country: {book[4]}")

            while True:

                choice = input(
                    """\nSelect an option:
                    1. Update Quantity
                    2. Update Author Information
                    3. Update Title
                    4. Return to Main Menu
                    :\n"""
                )

                if choice == "1":

                    while True:

                        try:
                            qty = int(input("New quantity:\n"))
                            break
                        except ValueError:
                            print("Error: Quantity entered not an integer.")

                    cursor.execute(
                        """UPDATE book SET qty = ? WHERE id = ?""", (qty, id)
                    )

                    db.commit()

                    print("Quantity successfully updated!\n")

                elif choice == "2":

                    name = input("Author's name:\n")
                    country = input("Author's country:\n")

                    cursor.execute(
                        """UPDATE author SET name = ?, country = ? WHERE id = ?""",
                        (name, country, author_id),
                    )

                    db.commit()

                    print("Author information successfully updated!\n")

                elif choice == "3":

                    title = input("Title:\n")

                    cursor.execute(
                        """UPDATE book SET title = ? WHERE id = ?""",
                        (title, id),
                    )

                    db.commit()

                    print("Title successfully updated!\n")

                elif choice == "4":

                    break

                else:

                    print("Input not recognised. Please try again!\n")


def delete_book():
    """
    Allows user to enter the ID of a book they wish to delete.
    The chosen book is removed from the database.
    """

    with closing(get_connection()) as db:

        with closing(db.cursor()) as cursor:

            id = input("Please input the ID of the book you wish to delete:\n")

            cursor.execute("""DELETE FROM book WHERE id = ?""", (id,))

            if cursor.rowcount == 0:
                print(f"No book found with ID {id}.")

            else:

                db.commit()

                print("Book successfully deleted!\n")


def search_books():
    """
    Allows the user to choose whether they would like to search by
    book ID, title or author ID.
    Returns information about the book they have searched.
    """

    with closing(get_connection()) as db:

        with closing(db.cursor()) as cursor:

            choice = input(
                """\nHow would you like to search?:
                1. Book ID
                2. Title
                3. Author ID
                :\n"""
            )

            if choice == "1":

                id = input("Please enter the book ID:")

                cursor.execute(
                    """SELECT title, authorID, qty FROM book 
                WHERE id = ?""",
                    (id,),
                )

                book_choice = cursor.fetchall()

                if book_choice:

                    print(f"\nBooks with ID {id}:")
                    for i in book_choice:
                        print(f"{i[0]} - Author ID: {i[1]} - Quantity: {i[2]}")

                else:
                    print(f"\nNo book found with ID {id}.")

            elif choice == "2":

                title = input("Please enter the book title:")

                cursor.execute(
                    """SELECT id, authorID, qty FROM book WHERE title = ?""",
                    (title,),
                )

                book_choice = cursor.fetchall()

                if book_choice:

                    print(f"\nBooks with title {title}:")
                    for i in book_choice:
                        print(
                            f"ID: {i[0]} - Author ID: {i[1]} - Quantity: {i[2]}"
                        )

                else:
                    print(f"\nNo book found with title '{title}'.")

            elif choice == "3":

                author_id = input("Please enter the author ID:")

                cursor.execute(
                    """SELECT id, title, qty FROM book WHERE authorID = ?""",
                    (author_id,),
                )

                book_choice = cursor.fetchall()

                if book_choice:

                    print(f"\nBooks with author ID {author_id}:")
                    for i in book_choice:
                        print(f"ID: {i[0]} - {i[1]} - Quantity: {i[2]}")

                else:
                    print(f"\nNo book found with author ID {author_id}.")

            else:
                print("Invalid input. Returning to menu.")


def view_details():
    """
    Prints the title, author name and country of the books
    by appending empty lists with information from the
    'book' and 'author' databases.
    """

    with closing(get_connection()) as db:

        with closing(db.cursor()) as cursor:

            cursor.execute(
                """
                SELECT b.title, a.name, a.country 
                FROM book b 
                INNER JOIN author a ON b.authorID = a.id
            """
            )

            results = cursor.fetchall()

            print("Details:")
            print("-------------------------")

            for row in results:
                title, author_name, country = row

                print(f"Title: {title}")
                print(f"Author's Name: {author_name}")
                print(f"Author's Country: {country}")
                print("-------------------------")


# context manager

databases()

# main menu
while True:
    menu = input(
        """\nSelect one of the following options:
1. Enter book
2. Update book
3. Delete book
4. Search books
5. View details of all books
0. Exit
:\n """
    )

    if menu == "1":

        enter_book()

    elif menu == "2":

        update_book()

    elif menu == "3":

        delete_book()

    elif menu == "4":

        search_books()

    elif menu == "5":

        view_details()

    elif menu == "0":
        print("Goodbye!")
        break

    else:
        print("You have entered an invalid input. Please try again")
