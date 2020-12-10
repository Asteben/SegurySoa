###############################################################
###############################################################
          elif opcion == 3:
            if getsv('rtran') == 'OK':
                print("Por favor ingresar los siguientes datos")
                monto = input("Monto a pagar:")
                cuenta = input("Cuenta desde donde va a pagar:")
                servicio = input("Numero del servicio a donde va a pagar")
   
                pydata= {
                "monto":"",
                "fecha":"",
                "cuenta":"",
                "servicio":"",
                }

                now = datetime.now()
                pydata["monto"] = monto
                pydata["fecha"] = now
                pydata["cuenta"] = cuenta
                pydata["servicio"] = servicio

                Envio('rpago', pydata)

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
