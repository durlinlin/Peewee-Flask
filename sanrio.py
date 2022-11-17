from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('sanrio', user='', password='', host='localhost', port=5432)

class BaseModel(Model):
  class Meta:
    database = db

class SanrioChar(BaseModel):
  name = CharField()
  debutYear = IntegerField()
  species = CharField()
  gender = CharField()
  hobbies = CharField([])

db.connect()
db.drop_tables([SanrioChar])
db.create_tables([SanrioChar])

SanrioChar(name='Hello Kitty', debutYear= 1974, species= 'Cat', gender='Female', hobbies = ['Baking cookies', 'Collecting cute things']).save()
SanrioChar(name='Cinnamoroll', debutYear= 2001, species= 'Dog', gender='Male', hobbies = ['Eating']).save()
SanrioChar(name='Pompompurin', debutYear= 1996, species= 'Dog', gender='Male', hobbies = ['Collects and hides shoes', 'Hanging out with friends', 'Purin aerobics']).save()
SanrioChar(name='Keroppi', debutYear= 1988, species= 'Frog', gender='Male', hobbies = ['']).save()
SanrioChar(name='My Melody', debutYear= 1975, species= 'Rabbit', gender='Female', hobbies = ['Baking almond cakes']).save()
SanrioChar(name='Kuromi', debutYear= 2005, species= 'Rabbit', gender='Female', hobbies = ['Writing in her diary', 'Cooking']).save()

app = Flask(__name__)

@app.route('/sanrio/', methods=['GET', 'POST'])
@app.route('/sanrio/<name>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(name=None):
  if request.method == 'GET':
    if name:
        return jsonify(model_to_dict(SanrioChar.get(SanrioChar.name == name)))
    else:
        charList = []
        for char in SanrioChar.select():
            charList.append(model_to_dict(char))
        return jsonify(charList)

  if request.method =='PUT':
    body = request.get_json()
    SanrioChar.update(body).where(SanrioChar.name == name).execute()
    return f"Sanrio character {name} has been updated."

  if request.method == 'POST':
    new_char = dict_to_model(SanrioChar, request.get_json())
    new_char.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    SanrioChar.delete().where(SanrioChar.name == name).execute()
    return f"Sanrio character {name} deleted."

app.run(debug=True, port=8000)
