import sqlite3


conn = sqlite3.connect('banco.sqlite')
cur = conn.cursor()

#USUARIO TABLA
cur.execute('DROP TABLE IF EXISTS Usuario')
cur.execute('CREATE TABLE Usuario (idUsuario INTEGER PRIMARY KEY AUTOINCREMENT, Nombre TEXT, Email TEXT, Password TEXT, RUT TEXT, Edad INT, Telefono INT)')

#TIPO DE CUENTA
cur.execute('DROP TABLE IF EXISTS Tipo')
cur.execute('CREATE TABLE Tipo (idTipo INTEGER PRIMARY KEY AUTOINCREMENT, Nombre TEXT, Costo_mantencion INTEGER, Cap_max_transferencia INTEGER, Cap_min_transferencia INTEGER)')

#CUENTA
cur.execute('DROP TABLE IF EXISTS Cuenta')
cur.execute('CREATE TABLE Cuenta (idCuenta INTEGER PRIMARY KEY AUTOINCREMENT, Numero INTEGER, Saldo INTEGER, Usuario_idUsuario INTEGER REFERENCES Usuario(idUsuario), Tipo_idTipo INTEGER REFERENCES Tipo(idTipo))')

#SERVICIO
cur.execute('DROP TABLE IF EXISTS Servicio')
cur.execute('CREATE TABLE Servicio (idServicio INTEGER PRIMARY KEY AUTOINCREMENT, Nombre Text, Saldo INTEGER)')

#TRANSACCION ENVIADA
cur.execute('DROP TABLE IF EXISTS TransaccionEnviada')
cur.execute('CREATE TABLE TransaccionEnviada (idTransaccionEnviada INTEGER PRIMARY KEY AUTOINCREMENT, Monto INTEGER, Comentario TEXT, Fecha TEXT, Cuenta_idCuenta INT REFERENCES Cuenta(idCuenta), Numero_Cuenta_Destino INT)')

#PAGO
cur.execute('DROP TABLE IF EXISTS Pago')
cur.execute('CREATE TABLE Pago (idPago INTEGER PRIMARY KEY AUTOINCREMENT, Monto INTEGER, Fecha TEXT, Cuenta_idCuenta INTEGER REFERENCES Cuenta(idCuenta), Servicio_idServicio INTEGER REFERENCES Servicio(idServicio))')

#TRANSACCION RECIBIDA
cur.execute('DROP TABLE IF EXISTS TransaccionRecibida')
cur.execute('CREATE TABLE TransaccionRecibida (idTransaccionRecibida INTEGER PRIMARY KEY AUTOINCREMENT, Monto INTEGER, Comentario TEXT, Fecha TEXT, Cuenta_idCuenta INT REFERENCES Cuenta(idCuenta), Numero_Cuenta_Origen INT)')

#INSERTAR TIPOS DE CUENTA
cur.execute('INSERT INTO Tipo (Nombre, Costo_mantencion, cap_max_transferencia, cap_min_transferencia) VALUES ("vista", 0, 200000, 1000)')
conn.commit()

cur.execute('INSERT INTO Tipo (Nombre, Costo_mantencion, cap_max_transferencia, cap_min_transferencia) VALUES ("corriente", 1000, 5000000000, 1000)')
conn.commit()

#INSERTAR SERVICIOS
cur.execute('INSERT INTO Servicio (Nombre, Saldo) VALUES ("agua", 0)')
conn.commit()

cur.execute('INSERT INTO Servicio (Nombre, Saldo) VALUES ("luz", 0)')
conn.commit()

