import re, json, os, pickle, uuid, time
from datetime import date, datetime


from book import Book
from user import User
from author import Author
from genre import Genre
import variables

import mysql.connector
from mysql.connector import Error

from collections import namedtuple

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
    # Connection Management used using 'with' keyword to remove duplicate codes for closing cursor and connection
    # Regex used for name of user. Similar validations can be used for other fields.
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
           user_name = input("Enter the user name: ")
           library_id = str(uuid.uuid4())[:10:]
           user_name_regex = r"[A-Za-z0-9]{3,}"
              
           if not re.match(user_name_regex, user_name):
             raise ValueError("User name must contain only alphanumeric characters and must be at least 3 characters long.")
          
           data = (user_name, library_id)
           query = "INSERT INTO users(name, library_id) VALUES (%s, %s)"
          
           cursor.execute(query, data)
           conn.commit()
           print('\33[32m', "User added to database successfully", "\033[0m")  
     
    except Error as e:
      print("\033[91m", "Failed to add user to database", e, "\033[0m")
    
    
  def display_users(self):
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
      
      
  def add_author(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
           name = input("Enter the name of the author: ")
           biography = input("Enter biography: ")
           data = (name, biography)
           
           query = "INSERT INTO authors(name, biography) VALUES(%s, %s)"
           cursor.execute(query, data)
           conn.commit()
           print('\33[32m', "Author added to database successfully", "\033[0m")
      
    except Error as e:
      print("\033[91m", "Failed to add author to the database", e, "\033[0m")
   
    
    
  def display_authors(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          query = "SELECT * FROM authors"
          cursor.execute(query)
          authors = cursor.fetchall()
          conn.commit()
          print("\033[92m", "Authors fetched successfully!", "\033[0m")
          
          for author in authors:
            print("\033[92m", author, "\033[0m")
    
    except Error as e:
      print("\033[91m", "Failed to fetch authors from database.", e, "\033[0m")
    

  def search_author(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          name = input("Enter the name of the author: ")
          query = f"SELECT * FROM authors WHERE name Like '%{name}%'"
          cursor.execute(query)
          author = cursor.fetchone()
          conn.commit()
          
          print("\033[92m", "Author details fetched successfully!", "\033[0m")
          print(author)
    
    except Error as e:
          print("\033[91m", "Failed to fetch author details from database", e, "\033[0m")       
  
  
  def add_genre(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          genre_name = input("Enter the genre name: ")
          genre_details = input("Enter the genre details: ")
          query = "INSERT INTO genres(genre_name, genre_details) VALUES(%s, %s)"
          cursor.execute(query, (genre_name, genre_details))
          conn.commit()
          
          print("\033[92m", "Genre added successfully!", "\033[0m")
    
    except Error as e:
          print("\033[91m", "Failed to add genre into database", e, "\033[0m")       
  
    
  def display_genres(self):
    try:
        with self.connect_database() as conn:
          with conn.cursor() as cursor:
            query = "SELECT * FROM genres"
            cursor.execute(query)
            genres = cursor.fetchall()
            conn.commit()
            print("\033[92m", "Genres fetched successfully!", "\033[0m")
            
            for genre in genres:
              print("\033[92m", genre, "\033[0m")
      
    except Error as e:
        print("\033[91m", "Failed to fetch genres from database.", e, "\033[0m")

      
      
    
  def add_book(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
            title = input("Enter the title of the book: ")
            author_id = input("Enter the author id: ")
            genre_id = input("Enter the genre id: ")
            isbn = input("Enter the ISBN number of the book: ")
            publication_date = input("Enter the publication date in the format of YYYY-MM-DD: ")

            data = (title, author_id, genre_id, isbn, publication_date)
            query = "INSERT INTO books(title, author_id, genre_id, isbn, publication_date) VALUES(%s, %s, %s, %s, %s)"
            cursor.execute(query, data)
            conn.commit()
            print('\33[32m', "Book added to database successfully", "\033[0m")
      
    except Error as e:
      print("\033[91m", "Failed to add book to the database", e, "\033[0m")
    

  def display_books(self):
    try:
        with self.connect_database() as conn:
          with conn.cursor() as cursor:
            query = "SELECT * FROM books"
            cursor.execute(query)
            books = cursor.fetchall()
            conn.commit()
            print("\033[92m", "Books fetched successfully!", "\033[0m")
            
            for book in books:
              print("\033[92m", book, "\033[0m")
      
    except Error as e:
        print("\033[91m", "Failed to fetch books from database.", e, "\033[0m")
        
        
  def display_book_author_genre(self):
      try:
        with self.connect_database() as conn:
          with conn.cursor() as cursor:
            query = """
              SELECT 
                  books.id AS book_id,
                  books.title AS book_title,
                  authors.name AS author_name,
                  authors.biography AS author_biography,
                  genres.genre_name AS genre_name,
                  genres.genre_details AS genre_details,
                  books.isbn,
                  books.publication_date,
                  books.availability
              FROM 
                  books
              JOIN 
                  authors ON books.author_id = authors.id
              JOIN 
                  genres ON books.genre_id = genres.id;
            """
            cursor.execute(query)
            data = cursor.fetchall()
            conn.commit()
            print("\033[92m", "Joined tables fetched successfully!", "\033[0m")
            
            for row in data:
              print("\033[92m", row, "\033[0m")
      
      except Error as e:
        print("\033[91m", "Failed to fetch books from database.", e, "\033[0m")
        
        
  # Once checkout the book, availibility set to 0 in books table,
  def checkout_book(self):
    isbn = input("Enter the ISBN of the book to borrow: ")
    user_id = input("What is the user's id? ")
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          query = f"SELECT id, title FROM books WHERE isbn='{isbn}'"
          cursor.execute(query)
          book = cursor.fetchone()
          conn.commit()
          print(book)
          book_id = book[0]
          today_date = datetime.today().strftime('%Y-%m-%d')
          
          query = "UPDATE books SET availability = %s WHERE id = %s"
          cursor.execute(query, (0, book_id))
          conn.commit()
          
          borrowed_book_info = (user_id, book_id, today_date)
          print(borrowed_book_info)
          query = "INSERT INTO borrowed_books(user_id, book_id, borrow_date) VALUES(%s, %s, %s)"
          cursor.execute(query, borrowed_book_info)
          conn.commit()
          
          print("\033[92m", f"Book {book[1]} has been borrowd", "\033[0m")

    except Error as e:
        print("\033[91m", "Failed to borrow the book.", e, "\033[0m")
      

   
  def checkin_book(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          isbn = input("Enter the ISBN of the book to return: ")
          user_id = input("What is the users id that wants to return the book? ")
          query = f"SELECT id, title FROM books WHERE isbn='{isbn}'"  
          cursor.execute(query)
          book = cursor.fetchone()
          conn.commit()
          book_id = book[0]
          today_date = datetime.today().strftime('%Y-%m-%d')
          
          query = "UPDATE books SET availability =%s WHERE isbn=%s"
          cursor.execute(query, (1, isbn))
          conn.commit()
          
          
          query = "UPDATE borrowed_books SET return_date = %s WHERE user_id = %s AND book_id = %s"
          cursor.execute(query, (today_date, user_id, book_id))
          conn.commit()
          
          print(f"Book {book[1]} has been check in")
      
    except:
      print('\33[31m', f"Book with ISBN {isbn} is not in the library or has not been checked out.", "\033[0m")
  
  # Borrowed books table shows the history of the books that were borrowed now or in the past. 
  # Other scenario would be to remove the book from table once checkin
  # In this case, first scenario has been used
  def display_borrowed_books(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          query = "SELECT * FROM borrowed_books"
          query = """
            SELECT
             borrowed_books.id AS book_id,
             borrowed_books.borrow_date AS borrow_date,
             borrowed_books.return_date AS return_date,
             users.name AS user_name,
             users.id AS user_id,
             books.title AS book_title,
             books.isbn AS book_isbn
             FROM borrowed_books
             INNER JOIN books ON books.id = borrowed_books.book_id
             INNER JOIN users ON borrowed_books.user_id = users.id
          """
          cursor.execute(query)
          borrowed_books = cursor.fetchall()
          conn.commit()
          
          for book in borrowed_books:
            print('\33[33m', book, '\033[0m')
            
    except Error as e:
      print("\033[91m", "Failed to display the borrowed books.", e, "\033[0m")
  
  # Displays books and relevant users that borrowed the books
  def display_borrower_users(self):
     try:
       with self.connect_database() as conn:
         with conn.cursor() as cursor:
           query = """
              SELECT 
              borrowed_books.user_id AS user_id,
              borrowed_books.borrow_date AS borrow_date,
              borrowed_books.return_date AS return_date,
              users.name AS user_name,
              users.library_id AS library_id
              FROM borrowed_books
              INNER JOIN users ON borrowed_books.user_id = users.id
           """
           cursor.execute(query)
           borrowed_books = cursor.fetchall()
           conn.commit()
           
           for book in borrowed_books:
             print('\33[33m', book, '\033[0m')
      
     except:
       print("\033[91m", "Failed to users who borrowed books.", "\033[0m")
    

  def search_book(self):
    try:
      with self.connect_database() as conn:
        with conn.cursor() as cursor:
          isbn = input("Enter the ISBN of the book you are looking for: ")
          title = input("Enter the title of the book you are looking for: ")
          query = "SELECT * FROM books WHERE isbn = %s OR title = %s"
          cursor.execute(query, (isbn, title))
          book = cursor.fetchone()
          conn.commit()
          
          print("\033[92m", "Book details fetched successfully!", "\033[0m")
          print(book)
    
    except Error as e:
          print("\033[91m", "Failed to fetch book details from database", e, "\033[0m")     
      
      
      
      