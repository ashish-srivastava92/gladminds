import MySQLdb
db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="hasher123", # your password
                      db="gladminds_qa") # name of the data base

# you must create a Cursor object. It will let
cur = db.cursor() 

cur.execute("SELECT distinct (user_id) FROM aftersell_ucnrecovery")
ucn = cur.fetchall()

cur.execute("SELECT * FROM auth_user")
user = cur.fetchall()

cur.execute("SELECT * FROM gladminds_userprofile")
userprofile = cur.fetchall()

cur.execute("SELECT * FROM aftersell_ucnrecovery")
ucns = cur.fetchall()

#for gm in gmuser:
 #   gmuser_id = gm[1]
 #   phone_number = gm[5]
  #  cur.execute("INSERT INTO gladminds_userprofile (user_id, phone_number) VALUES (%s, %s)",(gm[1],phone_number))
   # db.commit()

#cur.execute("alter table gladminds_gladmindusers drop foreign key user_id_refs_id_fbd3c2bc")
#cur.execute("alter table gladminds_gladmindusers drop column user_id")
#cur.execute("alter table gladminds_gladmindusers add user_id integer, add constraint foreign key (user_id) references gladminds_userprofile####(user_id)")

#for user in ucn:
 # user_id = user[0]
  #cur.execute("select * from auth_user where id = (%s)", user_id)
  #gmuser = cur.fetchall()
  #id=gmuser[0]
  #print id[0]
  #cur.execute("insert into gladminds_userprofile (user_id) values (%s)", (id[0])) 
  #db.commit()

#cur.execute("alter table aftersell_ucnrecovery add users_id integer, add constraint foreign key (user_id) references gladminds_userprofile(user_id)")

#for user in ucns:
# id = user[0]
# user_id = user[2]
# cur.execute("update aftersell_ucnrecovery set users_id = (%s) where id =(%s)", (user_id,id))
# db.commit()

#cur.execute("alter table aftersell_ucnrecovery drop foreign key aftersell_ucnrecovery_ibfk_1")
#cur.execute("alter table aftersell_ucnrecovery drop column user_id")
#cur.execute("alter table aftersell_ucnrecovery add user_id integer, add constraint foreign key (user_id) references gladminds_userprofile(user_id)")


#for user in ucns:
#    id=user[0]
#    user_id=user[6]
#    cur.execute("update aftersell_ucnrecovery set user_id = (%s) where id =(%s)", (user_id,id))
#    db.commit()

#alter table aftersell_ucnrecovery drop column users_id







