from main import db, app , Pokemon
import csv

db.create_all(app=app)

# add code to parse csv, create and save pokemon objects
with open('App/pokemon.csv', newline='') as csvfile:
  reader = csv.DictReader(csvfile)
  for row in reader:
  # replace any null values with None to avoid db errors
    if row['height_m'] == '':
      row['height_m'] = None
    if row['weight_kg'] == '':
      row['weight_kg'] = None
    if row['type2'] == '':
      row['type2'] = None

    pokemon = Pokemon(name=row['name'], attack=row['attack'], defense=row['defense'], sp_attack=row['sp_attack'], sp_defense=row['sp_defense'], weight=row['weight_kg'], height=row['height_m'], hp=row['hp'], speed=row['speed'], type1=row['type1'], type2=row['type2'])

    db.session.add(pokemon)
  db.session.commit()


