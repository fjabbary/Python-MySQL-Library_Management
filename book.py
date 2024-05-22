from genre import Genre
class Book:
  def __init__(self, title, author_id, genre_id, ISBN, publication_date):
    self.title = title
    self.author_id = author_id
    self.genre_id = genre_id
    self.ISBN = ISBN
    self.publication_date = publication_date
    self.is_available = 1
    
