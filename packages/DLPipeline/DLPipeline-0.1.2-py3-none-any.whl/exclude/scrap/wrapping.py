from functools import wraps


def augmentor(func):
  '''
  A function that accepts another function
  '''

  @wraps(func)
  def wrapper():
    '''
    A wrapping function
    '''
    return f'The result of {func()} is {eval(func())}'

  return wrapper


@augmentor
def useless():
  '''
    A pretty useless function
  '''
  return "1+1*2/2"


if __name__ == "__main__":

  print(useless())
  print(useless.__name__)
  print(useless.__doc__)
