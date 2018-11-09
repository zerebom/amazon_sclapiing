
class Book:
  def __init__(self) : 
    self.siteID  = ''
    self.book_name  = ''
    self.comment = []
    self.comment_page_num = 0

class Comment:
  def __init__(self) :
    author = ''
    star   = 0.0
    author_id   = ''
    comment = ''
    time = ''


if __name__ == '__main__' :
  abook = Book();
