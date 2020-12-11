import sqlite3

conn = sqlite3.connect('banco.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Usuario')
myresult = cur.fetchall()
conn.commit()

print(myresult)

cur.execute('SELECT * FROM Tipo')
myresult = cur.fetchall()
conn.commit()

print(myresult)


cur.execute('SELECT * FROM Cuenta')
myresult = cur.fetchall()
conn.commit()

print(myresult)


cur.execute('SELECT * FROM Servicio')
myresult = cur.fetchall()
conn.commit()

print(myresult)


cur.execute('SELECT * FROM TransaccionEnviada')
myresult = cur.fetchall()
conn.commit()

print(myresult)


cur.execute('SELECT * FROM Pago')
myresult = cur.fetchall()
conn.commit()

print(myresult)


cur.execute('SELECT * FROM TransaccionRecibida')
myresult = cur.fetchall()
conn.commit()

print(myresult)
