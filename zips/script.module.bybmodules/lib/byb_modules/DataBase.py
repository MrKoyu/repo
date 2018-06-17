'''
    Copyright (C) 2018 BYB

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sqlite3 
import koding



TableNames = []
DB_list = []

def check_is_in_DB_table(file,table,row_header,check_item):
    '''Returns True or False if item is a row'''
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute("select "+str(row_header)+" from "+str(table)+" where "+str(row_header)+"=?", (check_item,))
    data = cursor.fetchall()
    if not data:
        check = False
    if data:
        check = True   
    return check


def check_table_DB(filename,table):
	conn = sqlite3.connect(filename)
	cursor = conn.cursor()
	cursor.execute("SHOW TABLES LIKE %s"%table)
	result = cursor.fetchone()
	if result:
		check = 1
	else:
		check = 0
	return check

def count_item_DB(file,table,row,match,operator=None):
	''' Counts matches in DB either single row match or multiple row match with operator
	 if more the one coloum is to be matched row and match must be list in order
	file = path to file 
	table = table of file to be checked
	row = row to be checked if more then 1 row to match sent as a list of strings
	match = if multiple match sent through as tuple of strings, single row to match sent as string 
	operator = AND,OR or NOT do not pass through if using single row to match

	              ######multiple match example####
	count = count_item_DB(file=filename,table='sixteen_seventeen',row=['Comp','awayteam'],match=("premier league","tottenham"),operator='AND')

	              ######single row match example##### 
	count = count_item_DB(file=filename,table='sixteen_seventeen',row=['Comp','awayteam'],match=("premier league","tottenham"),operator='AND')''' 

	conn = sqlite3.connect(file)
	cursor = conn.cursor()
	if operator==None:
		match = (match,)
		cursor.execute("SELECT count(*) FROM %s WHERE %s LIKE ?"%(table,row),match)
	else:
		sql = "SELECT count(*) FROM %s WHERE"%table
		for Row in row:
			if not row.index(Row) == len(row)-1:
				sql += " lower(%s) LIKE ? %s" %(Row,operator)
			if row.index(Row) == len(row)-1:
				sql +=" lower(%s) LIKE ?" %Row
		cursor.execute(sql,match)
		koding.dolog(sql,line_info=True)
	count = cursor.fetchone()
	count = count[0]
	koding.dolog(count,line_info=True)
	return count

def del_all_data_DB(filename):
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for name in res:
        sql = 'DELETE FROM '+name[0]
        print sql
        cursor.execute(sql)
        conn.commit()

def delete_table(filename,table):
	conn = sqlite3.connect(filename)
	cursor = conn.cursor()
	sql = "DROP TABLE IF EXISTS %s;" % table
	cursor.execute(sql)
	conn.commit()

def headers_create(file,table,headers):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS %s(%s)'%(table,headers)) 

def readall_DB(file,table):
    conn = sqlite3.connect(file)
    cursor = conn.cursor()
    for row in cursor.execute('SELECT * FROM '+str(table)):
        DB_list.append(row)

def read_DB_row_match(filename,table,row,match):
	conn = sqlite3.connect(filename)
	cursor = conn.cursor()
	match = (match,)
	cursor.execute("SELECT * FROM %s WHERE %s=?"%(table,row),match)
	res = cursor.fetchall()
	for matches in res:
		DB_list.append(matches)
	koding.dolog('read_DB_row_match = %s'%DB_list,line_info=True)

def read_DB_col(filename,table,col):
	#read entire contents of a coloum  
	conn = sqlite3.connect(filename)
	cursor = conn.cursor()
	cursor.execute('SELECT %s FROM %s'%(col,table))
	res = cursor.fetchall()
	for items in res:
		DB_list.append(items)
	koding.dolog('read_DB_col = %s'%DB_list,line_info=True)
			
def table_names_DB(filename):
	conn = sqlite3.connect(filename)
	res = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
	for name in res:
		TableNames.append(name[0])
	koding.dolog(TableNames,line_info=True)
	#return TableNames

def update_item_DB(file,table,row_to_update,coloum_to_update,coloum_check,update_item):
	conn =  sqlite3.connect(file)
	cursor = conn.cursor()
	sql = "UPDATE "+str(table)+" SET "+str(coloum_to_update)+" = (?) WHERE "+str(coloum_check)+"=(?)" 
	cursor.execute(sql,(update_item,row_to_update))   
	conn.commit() 

def write_to_DB(file,table,headers,items):
	if not '?' in headers:
		a = headers.split(',')
		for x in a:
			headers = headers.replace((x),'?')
	conn = sqlite3.connect(file)
	cursor = conn.cursor()    
	cursor.execute("INSERT INTO "+table+" VALUES ("+headers+")",items)
	conn.commit()




