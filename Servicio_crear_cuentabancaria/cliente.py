######################################################################
######################################################################
######################################################################
          elif opcion == 1:
            if getsv('crcue') == 'OK':
                print("Por favor ingresar los siguientes datos")
                Numero = input("Numero de cuenta:")
                Tipo_idTipo = input("Tipo de cuenta: 1 para cuenta vista, 2 para cuenta corriente")
   
                pydata= {
                "Numero":"",
                "Saldo":"0",
                "Usuario_idUSuario":"",
                "Tipo_idTipo":"",
                }

                RutCuenta = string[0:(len(rut_login-2))]
                pydata["Numero"] = Numero
                pydata["Usuario_idUsuario"] = RutCuenta
                pydata["Tipo_idTipo"] = Tipo_idTipo

                Envio('crcue', pydata)

                while True:
                    data = sock.recv(250)
                    dataeval = eval(data[16:])
                    break
                    
                if data[12:16] == 'True':
                    print("Cuenta creada con éxito")
                elif data[12:24] == 'Falsecuenta'
                    print("Cuenta ya creada anteriormente")
                elif data[12:16] == 'Falsenumero'
                    print("Ingrese un tipo de cuenta correcto, intente otra vez")
          
