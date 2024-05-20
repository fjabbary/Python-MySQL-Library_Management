print("Welcome to the Library Management System!")

from library import Library

def main_app():
    library = Library()

    while True:
        
        print("\n1. Add User \n2. Display Users \n3. Checkout Book \n4. Checkin Book \n5. Add User \n6. Display Users \n7. Display Borrowers \n8. Search Book \n9. Add Author \n10. Display Authors \n11. Display Author details \n12. Add Genre \n13. Displays Genres \n14. Display Genre Details \n15. Export Data \n16. Import Data \n17. exit ")
        choice = input("Enter your choice: ")
        
        try: 
            if choice == "1":
                # library.add_book()
                library.add_user()
            elif choice == "2":
                library.display_users()   
                
                
                
            # elif choice == "2":
            #     library.display_books() 
            # elif choice == "3":
            #     library.checkout_book()
            # elif choice == "4":
            #     library.checkin_book()
            # elif choice == "5":
            #     library.add_user()
            # elif choice == "6":
            #     library.display_users()        
            # elif choice == "7":
            #     library.display_borrower_users()  
            # elif choice == "8":
            #     library.search_book() 
            # elif choice == "9":
            #     library.add_author() 
            # elif choice == "10":
            #     library.display_authors()
            # elif choice == "11":
            #     library.display_author_details()
            # elif choice == "12":
            #     library.add_genre()
            # elif choice == "13":
            #     library.display_genres()
            # elif choice == "14":
            #     library.display_genre_details()
            # elif choice == "15":
            #     library.export_data()
            # elif choice == "16":
            #     library.import_data()
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

