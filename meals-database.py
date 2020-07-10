#The goal of this program is to source data using an API and build a database in MySQL from that data.

import requests

#Connect to MySQL database.
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

conn_string = 'mysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
    host = '35.194.90.172:3306',
    user = 'root', 
    db = 'lab3',
    password = 'dwdstudent2015',
    encoding = 'utf8mb4')

engine = create_engine(conn_string)
con = engine.connect()

#Create a database to hold the data from the API.
db_name = 'lab3'
create_db_query = "CREATE DATABASE IF NOT EXISTS {db} DEFAULT CHARACTER SET 'utf8'".format(db=db_name)
con.execute(create_db_query)

#Create table to hold data.
table_name = 'meals' 
create_table_query = '''CREATE TABLE IF NOT EXISTS {db}.{table} 
                                (meal varchar(255),
                                meal_id varchar(255),
                                category varchar(255),
                                area varchar(255),
                                ingredients varchar(255), 
                                instructions varchar(255),
                                PRIMARY KEY(meal_id) 
                                )'''.format(db=db_name, table=table_name)
con.execute(create_table_query)
#PRIMARY KEY ensures meal_id is a unique value

query_template = '''INSERT IGNORE INTO {db}.{table}(meal, 
                                        meal_id, 
                                        category,
                                        area,
                                        ingredients,
                                        instructions) 
                    VALUES (%s, %s, %s, %s, %s, %s)'''.format(db=db_name, table=table_name)

for i in range(1,250):
    url = 'https://www.themealdb.com/api/json/v1/1/random.php'
    results = requests.get(url).json()
    data = results["meals"][0]
    meal = data["strMeal"]
    meal_id = data["idMeal"]
    category = data["strCategory"]
    area = data["strArea"]
    measure_def = ['strMeasure1','strMeasure2','strMeasure3','strMeasure4','strMeasure5','strMeasure6','strMeasure7','strMeasure8','strMeasure9','strMeasure10','strMeasure11','strMeasure12','strMeasure13','strMeasure14','strMeasure15','strMeasure16','strMeasure17','strMeasure18','strMeasure19','strMeasure20']
    ingredient_def = ['strIngredient1','strIngredient2','strIngredient3','strIngredient4','strIngredient5','strIngredient6','strIngredient7','strIngredient8','strIngredient9','strIngredient10','strIngredient11','strIngredient12','strIngredient13','strIngredient14','strIngredient15','strIngredient16','strIngredient17','strIngredient18','strIngredient19','strIngredient20']
    measure_list = []
    ingredient_list = []
    instructions = data["strInstructions"]
    ingredients = ''
    print("Inserting meal", meal)
    for measure in measure_def:
        measure_list.append(data[measure])
    for ingredient in ingredient_def:
        ingredient_list.append(data[ingredient])
    for i in range(0,20):
        if measure_list[i]=='': #ingredient_list[i] sometimes shows up as null, which is a NoneType
            break
        else:
            print(ingredients)
            ingredients += measure_list[i] + ' ' + ingredient_list[i] + ', '
    query_parameters = (meal, meal_id, category, area, ingredients, instructions)
    con.execute(query_template, query_parameters)
    print("Inserting meal", meal)
