
data = [['kisha'], ['jane'],['kisha'], ['kisha']]

def checkEqual1(iterator):
      try:
         iterator = iter(iterator)
         first = next(iterator)
         return all(first == rest for rest in iterator)
      except StopIteration:
         return True

print checkEqual1(data)
