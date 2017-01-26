"""

  Aorta (c) 2017 by s4ros

"""

class User(object):
# -----------------------------------------
  def __init__(self, nick):
    """
      Constructor ;)
    """
    self.nickname = nick
    # - get points stored in DB
    # self.points = read_from_db()

# -----------------------------------------
  def __str__(self):
    """
      Returns User.nickname when print()ed
    """
    return str(self.nick)

# -----------------------------------------
  def set_points(self, new_points):
    """
      SEt new amount of User Points
    """
    self.points = new_points

# -----------------------------------------
  def get_point(self):
    """
      Returns amount of stored User Points
    """
    return self.points

# -----------------------------------------
# -----------------------------------------
if __name__ == "__main__":
  users = []
  users.append( User("s4ros") )
  users.append( User("emi") )
  users.append( User("fantusia") )

  for u in users:
    print u