import mysql.connector
import json

mydb = mysql.connector.connect(
  host="localhost",
  user="Eduard",
  password="2comTbaci",
  database="ImobiliareDatabase"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE Apartment (ApartmentId INT PRIMARY KEY, Url VARCHAR(255), City VARCHAR(255),Neighbourhood VARCHAR(255),Price INT,Partitioning VARCHAR(255),Comfort_Level VARCHAR(255))")

with open('reports/apartments.json','r')as file:
    data = json.load(file)
l = []
print(len(data['products']))

for d in data['products']:
    if d['ID'] not in l:
        l.append(d['ID'])
        mycursor.execute("INSERT INTO Apartment (ApartmentId, Url, City,Neighbourhood,Price,Partitioning,Comfort_Level) VALUES (%s,%s,%s,%s,%s,%s,%s)", (int(d["ID"]), d["url"], d["city"],d['neighbourhood'],d['price'],d['partitioning'],d['comfort_level']))

sql_select = "select * from Apartment"
mycursor.execute(sql_select)
records = mycursor.fetchall()
print("Total number of rows in Apartment is: ", mycursor.rowcount)
for row in records:
    print("Id= ", row[0])
    print("Url= ", row[1])
    print("City= ", row[2])
    print("Neighbourhood= ", row[3])
    print("Price= ", row[4])
    print("Partitioning= ", row[5])
    print("Comfort_Level= ", row[6])
    print("____________________________")

mydb.commit()
mycursor.close()