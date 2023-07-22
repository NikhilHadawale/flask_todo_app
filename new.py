import json

# we can read json string with the help of json.loads() --> dict will be return
x =  '{ "name":"John", "age":30, "city":"New York"}'

y = json.loads(x)

print(y)