'''
Make sure you have downloaded the book's source code from the companion website at www.pearson.com/gaddis.
In this chapter's source code folder, you will find a program named create_cities_db.py. 
Run the program.
The program will create a database named cities.db. 
The cities.db database will have a table named Cities,
with the following columns:

CityID: INTEGER PRIMARY KEY
CityName: TEXT
Population: REAL

The CityName column stores the name of a city and the Population column stores the population of that city. 
After you run the create_cities_db.py program, 
the Cities table will contain 20 rows with various cities and their populations.

Next, write a program that connects to the cities.db database, 
and allows the user to select any of the following operations:

Display a list of cities sorted by population, in ascending order.
Display a list of cities sorted by population, in descending order.
Display a list of cities sorted by name.
Display the total population of all the cities.
Display the average population of all the cities.
Display the city with the highest population.
Display the city with the lowest population.
'''

import sqlite3

db = sqlite3.connect("cities.db")
cursor = db.cursor()

# Objective 1 - Display a list of cities sorted by population, in ascending order.

# Select the Table
cursor.execute("SELECT CityName, Population FROM Cities ORDER BY population ASC")
#Fetch All Rows
rows = cursor.fetchall()
# Run a For lop to print each city, by population.
print("Cities sorted by population:")
for name, population in rows:
    print(f"{name}: {int(population):,}")

print("\n")

# Objective 2 - Display a list of cities sorted by population, in descending order.

# Select the Table
cursor.execute("SELECT CityName, Population FROM Cities ORDER BY population DESC")
#Fetch All Rows
rows = cursor.fetchall()
# Run a For lop to print each city, by population.
print("Cities sorted by population:")
for name, population in rows:
    print(f"{name}: {int(population):,}")

print("\n")

# Display a list of cities sorted by name.
# Select the Table
cursor.execute("SELECT CityName, Population FROM Cities ORDER BY CityName DESC")
#Fetch All Rows
rows = cursor.fetchall()
# Run a For lop to print each city, by population.
print("Cities sorted by population:")
for name, population in rows:
    print(f"{name}: {int(population):,}")

print("\n")

# Display the total population of all the cities.
# Select the population column and sum
cursor.execute("SELECT SUM(population) FROM cities")

# Fetch the single result
total_population = cursor.fetchone()[0]

print(f"Total population: {int(total_population):,}")

print("\n")

# Display the average population of all the cities.
# Select the population column and average
cursor.execute("SELECT AVG(population) FROM cities")

# Fetch the single result
total_population = cursor.fetchone()[0]

print(f"Average population: {int(total_population):,}")

print("\n")

# Display the city with the highest population.
# Select the population column and Max
# Query to get the city with the highest population
cursor.execute("""
    SELECT CityName, Population
    FROM Cities
    WHERE Population = (SELECT MAX(Population) FROM Cities)
""")

# Fetch the result
city, population = cursor.fetchone()

print(f"City with highest population: {city} {int(population):,}")

print("\n")

# Display the city with the lowest population.
# Query to get the city with the lowest population
cursor.execute("""
    SELECT CityName, Population
    FROM Cities
    WHERE Population = (SELECT MIN(Population) FROM Cities)
""")

# Fetch the result
city, population = cursor.fetchone()

print(f"City with lowest population: {city} {int(population):,}")

print("\n")

db.close()