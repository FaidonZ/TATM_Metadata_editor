import random
def random_code():
      chars="abcdef"+"1234567890"
      random_code=""
      random_code +="".join(random.choice(chars) for char in range(8))
      random_code+="".join("-")
      random_code+="".join(random.choice(chars) for char in range(4))
      random_code+="".join("-")
      random_code+="".join(random.choice(chars) for char in range(4))
      random_code+="".join("-")
      random_code+="".join(random.choice(chars) for char in range(4))
      random_code+="".join("-")
      random_code+="".join(random.choice(chars) for char in range(12))
      return random_code
