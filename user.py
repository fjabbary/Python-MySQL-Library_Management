class User:
  def __init__(self, name, library_id):
    self.name = name
    self.library_id = library_id
    self.borrowed_books = []
    self.wait_list = []
    self.notification = ''
    
