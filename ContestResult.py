class ContestResult():

  def __init__(self, seconds, date, result):
    self.__seconds = seconds
    self.__date = date
    self.__result = result

  def getSeconds(self):
    return self.__seconds

  def getDate(self):
    return self.__date

  def getResult(self):
    return self.__result
