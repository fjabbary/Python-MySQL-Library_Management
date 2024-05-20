import re, json, os, pickle, uuid, time
from datetime import date
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

from book import Book
from user import User
from author import Author
from genre import Genre
import variables

import mysql.connector
from mysql.connector import Error

class Library:
  def __init__(self):
    self.books = {}
    self.users = {}  
    self.authors = {}
    self.genres = {}
    self.current_loans = {}
    
  # Connection function used as an in-class method
  def connect_database(self):
    try:
        conn = mysql.connector.connect(
            database = "library_management_system",
            user = "root",
            password = variables.password,
            host = "localhost"
          )
        
        if conn.is_connected():
          print('\33[96m', "Connection to MySQL is successful", "\033[0m")
          return conn
    
    except Error as e:
        print("Error while connecting to MySQL", e)
      
    
  def add_user(self):
    
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
           user_name = input("Enter the user name: ")
           library_id = input("What is the user library id? ")
      
           if not user_name or not library_id:
                raise ValueError("User name and library ID cannot be empty.")
          
           data = (user_name, library_id)
           query = "INSERT INTO users(name, library_id) VALUES (%s, %s)"
          
           cursor.execute(query, data)
           conn.commit()
           print('\33[32m', "User added to database successfully", "\033[0m")  
     
    except Error as e:
      print("\033[91m", "Failed to add user to database", e, "\033[0m")
      
   
    
    
  def display_users(self):
    # Connection Management used using 'with' keyword to remove duplicate codes for closing cursor and connection
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          query = "SELECT * FROM users"
          cursor.execute(query)
          users = cursor.fetchall()
          conn.commit()
          print("\033[92m", "Users fetched successfully!", "\033[0m")
          
          for user in users:
            print("\033[92m", user, "\033[0m")
      
    except Error as e:
      print("\033[91m", "Failed to fetch users from database", e, "\033[0m")
      
      
    
  def add_book(self):
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN number of the book: ")
    publication_date = input("Enter the publication date in the format of MM/DD/YYYY: ")
    genre = input("Enter the genre of the book: ")
    category = input("Enter the category of the book. 'Fiction' or 'Non-fiction': ")
    
    string_regex = r"[a-zA-Z0-9 .]{3,}"
    date_regex = r"\d{2}/\d{2}/\d{3,4}"
    # For simplicity of creation of a book data in cli, no regex validation is used for ISBN (ISBN-13 digits)
    valid_title = re.match(string_regex, title)
    valid_author = re.match(string_regex, author)
    valid_date = re.match(date_regex, publication_date) 
    
    if valid_title and valid_author and valid_date:
          new_book = Book(title, author, isbn, publication_date, genre, category, due_date="")
          self.books[isbn] = new_book
          print("\033[92m", "Book added successfully!", "\033[0m")
      
    else:
      print("\033[31m", "Book title, author have to be at least 3 characters and date has to be in valid format and refers to the past date", '\033[0m')
       

  def display_books(self):
    output = {}
    for isbn, book in self.books.items():
          one_book = {  
            isbn: {
                'title': book.get_title(),
                'author': book.get_author(),
                'ISBN': book.get_isbn(),
                'publication_date': book.get_publication_date(),
                'is_available': book.get_is_available(),
                'genre': book.get_genre_name(),
                'category': book.get_category()
            }
          }
          output.update(one_book)
          
    print("\033[92m",json.dumps(output, indent=4, sort_keys=True), "\033[0m")
     
        

  def checkout_book(self):
    isbn = input("Enter the ISBN of the book to borrow: ")
    library_id = input("What is the user's id? ")
    if library_id in self.users: # ony person with library id can checkout the book
      if isbn in self.books and self.books[isbn].borrow_book():
        self.current_loans[isbn] = self.users[library_id]
        
        # Due date set 3 months from borrowing date
        self.books[isbn].set_due_date(str(date.today() + relativedelta(months=+3)))
        self.users[library_id].borrowed_books.append(self.books[isbn])
        print('\33[32m', f"Book {self.books[isbn].get_title()} checked out to {self.users[library_id].name}","\033[0m")
        
      elif isbn in self.books and not self.books[isbn].get_is_available():
        self.users[library_id].wait_list.append(self.books[isbn])
        
        
    else:
      print('\33[31m', f"User with id of {library_id} is not a member or book is not available.", "\033[0m")

   
  def checkin_book(self):
    try:
      isbn = input("Enter the ISBN of the book to return: ")
      library_id = input("What is the users id that wants to return the book? ")
      if isbn in self.books and isbn in self.current_loans and library_id:
        self.books[isbn].return_book()
        self.current_loans.pop(isbn)
        
        for item in self.users[library_id].borrowed_books:
            if time.strptime(item.get_due_date(),"%Y-%m-%d") < time.strptime(str(date.today()),"%Y-%m-%d"):
              print('There will be late fee for this user')
            
        
        self.users[library_id].borrowed_books.remove(self.books[isbn])
      print(f"Book {self.books[isbn].get_title()} checked in")

      for user in self.users.values():
        for item in user.wait_list:
          if self.books[isbn].get_title() in item.get_title():
            user.notification = f"{self.books[isbn].get_title()} book is now available"
      
    except:
      print('\33[31m', f"Book with ISBN {isbn} is not in the library or has not been checked out.", "\033[0m")
  
  
  # Displays books and relevant users that borrowed the books
  def display_borrower_users(self):
    output = {}
    for library_id, user in self.current_loans.items():
      one_book_user = {
        library_id: {
          'library_id': user.library_id,
          'name': user.name
        }
      }
      output.update(one_book_user)
    
    print("\033[92m",json.dumps(output, indent=4, sort_keys=True), "\033[0m")
    


  def search_book(self):
    try:
      search_criteria = input("Do you want to search based on 'isbn' or 'title'? ")
      if search_criteria == 'isbn':
        isbn = input("Enter the ISBN of the book you are looking for: ")
        found_book = self.books[isbn]
        print("\033[92m",{
                  'title': found_book.get_title(),
                  'author': found_book.get_author(),
                  'ISBN': found_book.get_isbn(),
                  'publication_date': found_book.get_publication_date(),
                  'is_available': found_book.get_is_available(),
                  'genre': found_book.get_genre_name()
        }, "\033[0m")
        
      elif search_criteria == 'title':
        title = input("Enter the title of the book you are looking for: ")
        for book in self.books.values():
          # Find book even if search query partially matches with the title of the book
          if title.lower() in book.get_title().lower():
              print("\033[92m",{
                    'title': book.get_title(),
                    'author': book.get_author(),
                    'ISBN': book.get_isbn(),
                    'publication_date': book.get_publication_date(),
                    'is_available': book.get_is_available(),
                    'genre': book.get_genre_name()
                }, "\033[0m")
    except:
      print("No resilt found")

  def add_author(self):
    id = str(uuid.uuid4())
    name = input("Enter the name of the author: ")
    biography = input("Enter biography: ")
    author = Author(name, biography)
    self.authors[id] = author
    
    
  def display_authors(self):
    all_authors = {}
    for id, author in self.authors.items():
      one_author = { id: {'name': author.name, 'biography': author.biography} } 
      all_authors.update(one_author)
    print("\033[92m",json.dumps(all_authors, indent=4, sort_keys=True), "\033[0m")
    # Display them in the tabular format:
    data = [{'author': item.name, 'biography': item.biography} for item in self.authors.values()]
    table = tabulate(data, headers="keys", tablefmt="grid")
    print('\033[96m', table, '\033[0m')
    

  def display_author_details(self):
    id = input("Enter the id of the author: ")
    one_author = {id: {'name': self.authors[id].name, 'biography': self.authors[id].biography }}
    print("\033[92m", one_author, "\033[0m")
  
  
  def add_genre(self):
    id = str(uuid.uuid4())
    name = input("Enter the genre: ")
    category = input("Enter category. 'Fiction' or 'Non-fiction': ")
    genre = Genre(name, category)
    self.genres[id] = genre
  
    
  def display_genres(self):
    all_genres = {}
    for id, genre in self.genres.items():
      one_genre = { id: {'name': genre.get_genre_name(), 'category': genre.get_category()} } 
      all_genres.update(one_genre)
    print("\033[92m",json.dumps(all_genres, indent=4, sort_keys=True), "\033[0m")


  def display_genre_details(self):
    id = input("Enter the id of the genre: ")
    one_genre = {id: {'genre_name': self.genres[id].get_genre_name(), 'category': self.genres[id].get_category() }}
    print("\033[92m", one_genre, "\033[0m")



  #export data in binary mode and save them inside /data directory
  def export_data(self):
    directory = './data'
    file_path = os.path.join(directory, 'books.txt')
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    try:
      with open(file_path, 'wb') as file:
          pickle.dump(self.books, file)
          
      with open('data/users.txt', 'wb') as file:   
          pickle.dump(self.users, file)
          
      with open('data/authors.txt', 'wb') as file:   
          pickle.dump(self.authors, file)
          
      with open('data/genres.txt', 'wb') as file:   
          pickle.dump(self.genres, file)
          
      with open('data/current_loans.txt', 'wb') as file:   
          pickle.dump(self.current_loans, file)
    except:
      print("Error while exporting data")


  # Import data in binary mode from /data directory  convert it to dictionary 
  def import_data(self):
    with open('data/books.txt', 'rb') as file:
       books_dict = pickle.load(file)
       self.books = books_dict
       
    with open('data/users.txt', 'rb') as file:
       users_dict = pickle.load(file)
       self.users = users_dict  
 
    with open('data/authors.txt', 'rb') as file:
       authors_dict = pickle.load(file)
       self.authors = authors_dict  
     
    with open('data/genres.txt', 'rb') as file:
       genres_dict = pickle.load(file)
       self.genres = genres_dict       

    with open('data/current_loans.txt', 'rb') as file:
       curren_loans_dict = pickle.load(file)
       self.curren_loans = curren_loans_dict  