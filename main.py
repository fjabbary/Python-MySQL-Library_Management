print("\033[1m", "Welcome to the Library Management System!", "\033[0m")

from library import Library
import uuid


def sub_main(library):
        while True:
            try: 
                operation = input("What operation you want to do? Enter 'user', 'author', 'genre', 'book', or 'exit': ")
                if operation == 'user':
                    op = input("Choose type of operation for user. Enter 'add' or 'display': ")
                    if op == 'add':
                        library.add_user()
                    elif op == 'display':
                        library.display_users()
                
                elif operation == 'author':
                    op = input("Choose type of operation for author. Enter 'add', 'display', or 'search': ")
                    if op == 'add':
                        library.add_author()
                    elif op == 'display':
                        library.display_authors()
                    elif op == 'search':
                        library.search_author()
                    
                elif operation == 'genre':
                    op = input("Choose type of operation for genre. Enter 'add' or 'display': ")
                    if op == 'add':
                        library.add_genre()
                    elif op == 'display':
                        library.display_genres()
                
                elif operation == 'book':
                    op = input("Choose type of operation for book. Enter 'add', 'display', 'display_all_info', 'checkout', 'checkin', 'display_borrowed_books', 'display_borrowed_users', 'search': ")
                    if op == 'add':
                        library.add_book()
                    elif op == 'display':
                        library.display_books()
                    elif op == 'display_all_info':
                        library.display_book_author_genre()
                    elif op == 'checkout':
                        library.checkout_book()
                    elif op == 'checkin':
                        library.checkin_book()
                    elif op == 'display_borrowed_books':
                        library.display_borrowed_books()
                    elif op == 'display_borrowed_users':
                        library.display_borrower_users()
                    elif op == 'search':
                        library.search_book()
                        
              
                elif operation == "exit":
                    exit()
                    
                elif operation == "":
                    print("Thanks for supporting your public Library! Have a nice day :)")
                    break
                else:
                    print("Please enter a valid choice")
            except Exception as e:
                print(f"An error occurred: {e}")



def main_app():
    library = Library()
    library.connect_database()
   
    with library.connect_database() as conn:
         print("\033[1m", "Please login with name and library ID to use the app", "\033[0m")
         # Authentication
         user_name = input("Enter user name: ")
         library_id = input("Enter library id: ")
         with conn.cursor() as cursor:
            query = "SELECT * FROM users WHERE name=%s AND library_id=%s"
            cursor.execute(query, (user_name, library_id))
            user = cursor.fetchone()
            conn.commit()
            
            if user: 
                print('\33[32m', f'{user[1]} is authenticated', "\033[0m")
                sub_main(library)
            else:
                print("\033[91m", 'User is not authenticated. You need to register before using App', "\033[0m")
                user_name = input("Enter name you want to register as a username: ")
                # System generate library id assigned to user who wants to register (10 charaters only to match with table field VARCHAR(10))
                library_id = str(uuid.uuid4())[:10:]
                with conn.cursor() as cursor:
                    query = "INSERT INTO users(name, library_id) VALUES(%s, %s)"
                    cursor.execute(query, (user_name, library_id))
                    conn.commit()
                    print("\033[32m", f"User {user_name} is registered. Your library id is {library_id}. Please keep note this ID since it is required to login in the future in order to manage the library", "\033[0m")
                        
                
      
if __name__ == "__main__":
    main_app()