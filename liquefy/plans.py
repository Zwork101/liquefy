from liquefy.errors import TooLongError
from liquefy.headers import *

from typing import Any, ClassVar
from struct import pack

plans = {}

def liquefy(item: Any):
  return plans[type(item)](item)

def mark(typ: ClassVar):
  def func_wrap(func):
    plans[typ] = func
    return func
  return func_wrap

@mark(int)
def tranform_int(number: int):
  if 0 <= number:
    if number <= 0xFFFF:
      return pack("!BH", SHORT_POS_HEADER, number)
    elif number <= 0xFFFFFFFF:
      return pack("!BI", INT_POS_HEADER, number)
    elif number <= 0xFFFFFFFFFFFFFFFF:
      return pack("!BQ", LONG_POS_HEADER, number)
    elif number > 0:
      raise TooLongError("Integers must be less than 0xFFFFFFFFFFFFFFFF.")
  else:
    if number >= -0xFFFF:
      return pack("!BH", SHORT_NEG_HEADER, -number)
    elif number >= -0xFFFFFFFF:
      return pack("!BI", INT_NEG_HEADER, -number)
    elif number >= -0xFFFFFFFFFFFFFFFF:
      return pack("!BQ", LONG_NEG_HEADER, -number)
  
  raise TooLongError("Integers must be greater than -0xFFFFFFFFFFFFFFFF")
