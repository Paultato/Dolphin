from peewee import *

# Connect to a MySQL database on network.
mysql_db = MySQLDatabase('dolphin', user='root', password='',
                         host='127.0.0.1', port=3306)