class Genre:
  def __init__(self, genre_name, category):
    self.__genre_name = genre_name
    self.__category = category
    
  def get_genre_name(self):
    return self.__genre_name
  
  def get_category(self):
    return self.__category