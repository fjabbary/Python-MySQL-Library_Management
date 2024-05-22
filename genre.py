class Genre:
  def __init__(self, genre_name, genre_details):
    self.__genre_name = genre_name
    self.__genre_details = genre_details
    
  def get_genre_name(self):
    return self.__genre_name
  
  def get_genre_details(self):
    return self.__genre_details