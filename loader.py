#pip install peewee
def algorithm_run(inti):
	left_arr={}
	for i in range(1,9):
		left_arr['xp'+str(inti)+str(i)] = str(random.randint(1, 15))
	return {**left_arr}
    
import sqlite3
import csv
import random

connection = sqlite3.connect("db.sqlite3")
connection.set_trace_callback(print)
cursor = connection.cursor()


#rows = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print([k for k in rows])

count=0
with open("Compositors.csv") as csvfile:
	filereader = csv.reader(csvfile, delimiter=';')
	for row in filereader:
		print("-------find: "+row[0])
		if cursor.execute("select * from astro_histpersons where fio=?",(row[0],)).fetchall():
			print("already exist")
		else:
			print("not found")
			count=count+1
			sqlite_insert_with_param = """INSERT INTO astro_histpersons(fio, date, result, note) VALUES (?, ?, ?, ?);"""
			data_tuple = (row[0],row[1],str(algorithm_run(count)),"compositor")
			cursor.execute(sqlite_insert_with_param, data_tuple)
			print("created")
#rows = cursor.execute("select * from astro_histpersons").fetchall()
#print([i for i in rows])

connection.commit()
connection.close()
