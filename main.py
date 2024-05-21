print("Welcome to the Library Management System!")

from library import Library

def main_app():
    library = Library()

    while True:
        
        print("\n1. Add User \n2. Display Users \n3. Add Author \n4. Display Authors \n5. Search Author \n6. Add Genre \n7. Display Genres \n8. Add Book \n9. Display Books \n10. Display book_author_genre \n11. Checkout Book \n12. Checkin Book \n13. Display Borrowed Books \n14. Display Borrower Users \n15. Search Book")
        choice = input("Enter your choice: ")
        
        try: 
            if choice == "1":
                library.add_user()
            elif choice == "2":
                library.display_users()   
            elif choice == "3":
                library.add_author()   
            elif choice == "4":
                library.display_authors()  
            elif choice == "5":
                library.search_author()
            elif choice == "6":
                library.add_genre()    
            elif choice == "7":
                library.display_genres() 
            elif choice == "8":
                library.add_book()
            elif choice == "9":
                library.display_books()
            elif choice == "10":
                library.display_book_author_genre()    
            elif choice == "11":
                library.checkout_book()
            elif choice == "12":
                library.checkin_book()
            elif choice == "13":
                library.display_borrowed_books()
            elif choice == "14":
                library.display_borrower_users()  
            elif choice == "15":
                library.search_book()
                
                

            elif choice == "17":
                exit()
                
            elif choice == "":
                print("Thanks for supporting your public Library! Have a nice day :)")
                break
            else:
                print("Please enter a valid choice")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main_app()

