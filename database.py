import sqlite3
conn=sqlite3.connect("data")
cursor=conn.cursor()
cursor.execute("CREATE TABLE details ( `playingid` INT NOT NULL , `one` INT NOT NULL DEFAULT '0' , `two` INT NOT NULL DEFAULT '0' );")
cursor.execute("CREATE TABLE fight ( `playingid` INT NOT NULL , `one` INT NOT NULL DEFAULT '50' , `two` INT NOT NULL DEFAULT '50' );")
cursor.execute("insert into details(playingid) values('1')")
cursor.execute("insert into fight(playingid) values('1')")
conn.commit()
