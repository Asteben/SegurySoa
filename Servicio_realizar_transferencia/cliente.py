###############################################################
###############################################################
          elif opcion == 3:
              idcuentas = []
              if getsv('idcnt') == 'OK':
                pydata = {
                    "idUsuario" : id_login
                }

                Envio('idcnt', pydata)

                error = False
                data = b''
                while True:
                    data = sock.recv(250)
                    if data[12:16] == b'True':
                        dataeval = eval(data[16:])
                        print("Las cuentas bancarias propias son:")
                        aux = 0
                        while aux < len(dataeval):
                        idcuentas.append(dataeval[aux][0])
                        idnumeros.append(dataeval[aux][2])
                        print(aux+1,"- Tipo:",dataeval[aux][1],"Numero de cuenta:",dataeval[aux][2],"Saldo:",dataeval[aux][3])
                        aux = aux + 1
                    else:
                        print("ha ocurrido un error!")
                        error = True
                        break
                    break
                
                if error == False:
                    select= int(input("Seleccione cuenta con la cual desea realizar la transferencia, ingrese 0 para volver"))
                    if select <= 0 or select > len(idcuentas):
                        break
                    elif getsv('rtran') == 'OK':
                        print("Por favor ahora ingresar los siguientes datos")
                        monto = input("Monto a pagar:")
                        comentario = input("Comentario:")
                        cuentadestino = input("Numero de la cuenta destino")
        
                        pydata= {
                        "monto":0,
                        "fecha":"",
                        "cuenta":"",
                        "comentario":"",
                        "cuentadestino":0,
                        }

                        now = datetime.now()
                        pydata["monto"] = monto
                        pydata["fecha"] = now
                        pydata["cuenta"] = idcuentas[select-1]
                        pydata["comentario"] = comentario
                        pydata["cuentadestino"] = cuentadestino

                        Envio('rtran', pydata)

                        while True:
                            data = sock.recv(250)
                            dataeval = eval(data[16:])
                            break
                            
                        if data[12:16] == 'True':
                            print("Transferencia realizada con éxito con éxito")
                        elif data[12:22] == 'Falsesaldo'
                            print("Saldo insuficiente para realizar pago")
                        elif data[12:23] == 'Falsecuenta'
                            print("No existe la cuenta desde donde quiere transferir")
###############################################################
###############################################################
