from sqlalchemy import create_engine



# use of SQlite 
engine = create_engine('sqlite:///college.db', echo = True)

# Use of MySQL
# For example, if you are using PyMySQL driver with MySQL, use the following command −
# mysql+pymysql://<username>:<password>@<host>/<dbname>
# To hide the verbose output, set echo attribute to None. 
# engine = create_engine("mysql://user:pwd@localhost/college",echo = True)

# Create Table
# Hence an object of MetaData class from SQLAlchemy Metadata is a collection of Table objects and their associated schema constructs. It holds a collection of Table objects as well as an optional binding to an Engine or Connection.
from sqlalchemy import MetaData
meta = MetaData()
# Next, we define our tables all within above metadata catalog, using the Table construct, which resembles regular SQL CREATE TABLE statement.
# An object of Table class represents corresponding table in a database. The constructor takes the following parameters −

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
meta = MetaData()

students = Table(
   'students', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('lastname', String), 
)

# The create_all() function uses the engine object to create all the defined table objects and stores the information in metadata.
# meta.create_all(engine)


# methods like update(), delete() and select() 
# ins = students.insert()
# ins.compile().params  # {'name': 'Karan'}
# In order to execute the resulting SQL expressions, we have to obtain a connection object 
# representing an actively checked out DBAPI connection resource and then feed the expression object as shown in the code below.
# conn = engine.connect()
# ins = students.insert().values(name = 'Bijan', lastname = 'khan')
# result = conn.execute(ins) # need to commit the insert 
# print(result)

# Following is the entire snippet that shows the execution of INSERT query using SQLAlchemy’s core technique
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///college.db', echo = True)
meta = MetaData()

students = Table(
   'students', meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('lastname', String), 
)
addresses = Table(
   'addresses', meta, 
   Column('id', Integer, primary_key = True), 
   Column('st_id', Integer, ForeignKey('students.id')), 
   Column('postal_add', String), 
   Column('email_add', String))
   


ins = students.insert()
ins = students.insert().values(name = 'Ravi', lastname = 'Kapoor')
conn = engine.connect()
result = conn.execute(ins)

# feed table
conn.execute(students.insert(), [
   {'name':'Ravi', 'lastname':'Kapoor'},
   {'name':'Rajiv', 'lastname' : 'Khanna'},
   {'name':'Komal','lastname' : 'Bhandari'},
   {'name':'Abdul','lastname' : 'Sattar'},
   {'name':'Priya','lastname' : 'Rajhans'},
])
conn.execute(addresses.insert(), [
   {'st_id':1, 'postal_add':'Shivajinagar Pune', 'email_add':'ravi@gmail.com'},
   {'st_id':1, 'postal_add':'ChurchGate Mumbai', 'email_add':'kapoor@gmail.com'},
   {'st_id':3, 'postal_add':'Jubilee Hills Hyderabad', 'email_add':'komal@gmail.com'},
   {'st_id':5, 'postal_add':'MG Road Bangaluru', 'email_add':'as@yahoo.com'},
   {'st_id':2, 'postal_add':'Cannought Place new Delhi', 'email_add':'admin@khanna.com'},
])


# Select --------------------------------------------
# SELECT students.id, students.name, students.lastname FROM students
select = students.select() 
result = conn.execute(select)
# The resultant variable is an equivalent of cursor in DBAPI. We can now fetch records using fetchone() method.
# row = result.fetchone()
# OR
for row in result:
   print (row)

# Use WHERE clause
# Here c attribute is an alias for column.
s = students.select().where(students.c.id>2)
result = conn.execute(s)
for row in result:
   print (row)

# Here, we have to note that select object can also be obtained by select() function in sqlalchemy.sql module
# from sqlalchemy.sql import select
# s = select([users])
# result = conn.execute(s)

# Use Text fo querying
from sqlalchemy import text
t = text("SELECT * FROM students")
result = conn.execute(t)

# or 
s = text("select students.name, students.lastname from students where students.name between :x and :y")
conn.execute(s, x = 'A', y = 'L').fetchall()
# or
# The text() construct supports pre-established bound values using the TextClause.bindparams() method. The parameters can also be explicitly typed as follows −
from sqlalchemy.sql.expression import bindparam
stmt = text("SELECT * FROM students WHERE students.name BETWEEN :x AND :y")
stmt = stmt.bindparams(
   bindparam("x", type_= String), 
   bindparam("y", type_= String)
)
result = conn.execute(stmt, {"x": "A", "y": "L"})
# or
from sqlalchemy.sql import select
s = select([text("students.name, students.lastname from students")]).where(text("students.name between :x and :y"))
conn.execute(s, x = 'A', y = 'L').fetchall()

# and_() function to combine multiple conditions in WHERE clause created with the help of text() function.
from sqlalchemy import and_
from sqlalchemy.sql import select
s = select([text("* from students")]) \
.where(
   and_(
      text("students.name between :x and :y"),
      text("students.id>2")
   )
)
conn.execute(s, x = 'A', y = 'L').fetchall()

# Aliases ----------------------------------
from sqlalchemy.sql import alias
st = students.alias("a")
# This alias can now be used in select() construct to refer to students table −
s = select([st]).where(st.c.id>2) # This translates to SQL expression as follows − SELECT a.id, a.name, a.lastname FROM students AS a WHERE a.id > 2

# Update -----------------------------------
# table.update().where(conditions).values(SET expressions)
# 'UPDATE students SET lastname = :lastname WHERE students.lastname = :lastname_1'
# Node : where clause is case sensitive
stmt = students.update().where(students.c.lastname == 'Kapoor').values(lastname = 'aaaaa')
conn.execute(stmt)
s = students.select()
# conn.execute(s).fetchall()

# OR
# from sqlalchemy.sql.expression import update
# stmt = update(students).where(students.c.lastname == 'Khanna').values(lastname = 'Kapoor')

# Delete --------------------------------
stmt = students.delete().where(students.c.id > 2)
conn.execute(stmt)

# Multiple table  Select --------------------------------
from sqlalchemy.sql import select
s = select([students, addresses]).where(students.c.id == addresses.c.st_id)
result = conn.execute(s)

for row in result:
   print (row)

# Multiple table Update --------------------------------
# UPDATE students 
# SET email_add = :addresses_email_add, name = :name 
# FROM addresses 
# WHERE students.id = addresses.id
stmt = students.update().values({
   students.c.name:'xyz',
   addresses.c.email_add:'abc@xyz.com'
}).where(students.c.id == addresses.c.id)
# Note SQLite dialect however doesn’t support multiple-table criteria within UPDATE and shows following error −
# NotImplementedError: This backend does not support multiple-table criteria within UPDATE
# conn.execute(stmt)

# Parameter-Ordered Updates --------------------------------
# In some cases, the order of parameters rendered in the SET clause are significant. 
# In MySQL, providing updates to column values is based on that of other column values.
# Following statement’s result −
# UPDATE table1 SET x = y + 10, y = 20
# will have a different result than −
# UPDATE table1 SET y = 20, x = y + 10
# SET clause in MySQL is evaluated on a per-value basis and not on per-row basis. For this purpose, the preserve_parameter_order is used.
# stmt = table1.update(preserve_parameter_order = True).values([(table1.c.y, 20), (table1.c.x, table1.c.y + 10)])
# The List object is similar to dictionary except that it is ordered. This ensures that the “y” column’s SET clause will render first, then the “x” column’s SET clause.

# Multiple tables Delete --------------------------------
# More than one table can be referred in WHERE clause of DELETE statement in many DBMS dialects. For PG and MySQL, “DELETE USING” syntax is used; and for SQL Server, using “DELETE FROM” expression refers to more than one table.
# stmt = students.delete().\
#    where(students.c.id == addresses.c.id).\
#    where(addresses.c.email_add.startswith('xyz%'))
# conn.execute(stmt)

# Using Join
# The join() method returns a join object from one table object to another.
# join(right, onclause = None, isouter = False, full = False)
# # right − the right side of the join; this is any Table object
# # onclause − a SQL expression representing the ON clause of the join. If left at None, it attempts to join the two tables based on a foreign key relationship
# # isouter − if True, renders a LEFT OUTER JOIN, instead of JOIN
# # full − if True, renders a FULL OUTER JOIN, instead of LEFT OUTER JOIN
# print(students.join(addresses)) #students JOIN addresses ON students.id = addresses.st_id

# Explicitly mention joining criteria as follows −
j = students.join(addresses, students.c.id == addresses.c.st_id)
# print("j : ",j)
stmt = select([students]).select_from(j)
# This will result in following SQL expression −
# SELECT students.id, students.name, students.lastname
# FROM students JOIN addresses ON students.id = addresses.st_id
print ("---------------")
result = conn.execute(stmt)
# result.fetchall()
# for row in result:
#      print (row)

# Using Conjunctions --------------------------------
# SELECT * from EMPLOYEE WHERE salary>10000 AND age>30
# SQLAlchemy functions and_(), or_() and not_() respectively implement AND, OR and NOT operators.

# and_()
from sqlalchemy import and_, or_, asc, desc, between
print(
# This translates to: students.name = :name_1 AND students.id < :id_1
   and_(
      students.c.name == 'Ravi',
      students.c.id <3
   )
)
# and_ using in select 
stmt = select([students]).where(and_(students.c.name == 'Ravi', students.c.id <3))
# SELECT statement of the following nature will be constructed −
# SELECT students.id, 
#    students.name, 
#    students.lastname
# FROM students
# WHERE students.name = :name_1 AND students.id < :id_1

# or_ using in select
stmt = select([students]).where(or_(students.c.name == 'Ravi', students.c.id <3))

# asc()
# It produces an ascending ORDER BY clause. The function takes the column to apply the function as a parameter.
stmt = select([students]).order_by(asc(students.c.name))

# desc()
stmt = select([students]).order_by(desc(students.c.lastname))
# SELECT students.id, 
#    students.name, 
#    students.lastname
# FROM students 
# ORDER BY students.lastname DESC

# between() 
stmt = select([students]).where(between(students.c.id,2,4))
print (stmt) # SELECT students.id, students.name, students.lastname FROM students WHERE students.id  BETWEEN :id_1 AND :id_2

# func ----------------------------------------------------------------
from sqlalchemy.sql import func
result = conn.execute(select([func.now()]))
print (result.fetchone())

result = conn.execute(select([func.count(students.c.name)]))
print(select([func.count(students.c.name)]))
# print (result.fetchone())
# max() min() avg()
result = conn.execute(select([func.max(students.c.id)]))
result = conn.execute(select([func.min(students.c.id)]))
result = conn.execute(select([func.avg(students.c.id)]))

# Union ----------------------------------------------------------------
print("Union --------------------------------------------------------------")
from sqlalchemy import union
u = union(addresses.select().where(addresses.c.email_add.like('%@gmail.com'), addresses.select().where(addresses.c.email_add.like('%@yahoo.com'))))
result = conn.execute(u)
print (result.fetchall())
