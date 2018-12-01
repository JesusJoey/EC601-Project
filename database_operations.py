#author Yang Qiao
#!/usr/bin/env python
# encoding: utf-8
import miniproj1_mysql
import pymongo
import pymsql
import sys

password=""
keyword='fashion'


def search(keyword):
	db = pymysql.connect("localhost","root",password,"miniproj_database")
	cursor = db.cursor()
	sql='select labels with "%{}%"'.format(keyword)
	cursor.execute(sql)
	data = cursor.fetchall()

	result=[]
	for item in data:
		if not i[0] in result:
			result.append(i[0])

	if result:
		print(result)
	else:
		print("No account has this description label")

def statistics():
	db = pymysql.connect("localhost","root",password,"miniproj_database")
	cursor = db.cursor()
	sql1 = 'SELECT username,count(*) FROM label GROUP BY username'
	sql2 = 'SELECT labels,count(*) FROM label GROUP BY labels order by count(*) desc limit 10'
	try:
		cursor.execute(sql1)
		data1 = cursor.fetchall()
		cursor.execute(sql2)
		data2 = cursor.fetchall()
	except Exception as e:
		print("Error: unable to fetch data")
		raise e
    print("\n Number of labels:")
    print(data1)
    print("\nMost 10 popular descriptions:")
    print(data2)

    


search(keyword)
statistics()
