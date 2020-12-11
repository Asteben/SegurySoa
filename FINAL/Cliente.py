import socket
import sys
import json
from datetime import date


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('200.14.84.235', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.connect(server_address)

def generate_tx_length(tx_length):
    char_ammount = 5 # Cantidad de caracteres máximos para definir el largo de la transacción (5 según formato solicitado por el bus)
    char_left = char_ammount - len(str(tx_length)) # Espacios sobrantes para rellenar con 0 a la izquierda

    str_tx_length = ''
    for i in range(char_left):
      str_tx_length += '0'
    
    str_tx_length += str(tx_length) # String con el largo de la transacción
    return str_tx_length

####################################################################################

def Envio(servicio, data):
  jsondata = json.dumps(data, default=str)  
  tx_cmd = servicio + jsondata # Comando de registro de servicio ante el bus    
  tx = generate_tx_length(len(tx_cmd)) + tx_cmd
  sock.send(tx.encode(encoding='UTF-8'))

####################################################################################

def getsv(servicio):
  tx_cmd = 'getsv' + servicio  # Comando de registro de servicio ante el bus
  tx = generate_tx_length(len(tx_cmd)) + tx_cmd
  sock.send(tx.encode(encoding='UTF-8'))
  status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)
  print(status)
  return status

####################################################################################

print("BIENVENIDO A SEGURYSOA! =)")

while True:
  print("1.- Realizar LogIn")
  print("2.- Registrar Usuario")
  print("3.- Salir")
  opcion = int(input("Ingrese numero respectivo a la opcion que desee realizar:"))

####################################################################################
############################ LOGEAR CUENTA #########################################
####################################################################################

  if opcion == 1:
    Login_user = False
    id_login = 0
    rut_login = 0
    if getsv('login') == 'OK':
      print("Por favor ingresar los siguientes datos")
      Email = input("Email:")
      Password = input("Password:")
      pydata= {
      "Email":"",
      "Password": "",
      }
      pydata["Email"] = Email
      pydata["Password"] = Password

      Envio('login',pydata)

      while True: #Espera hasta recibir la respuesta por parte del serivico
        data = sock.recv(250)
        print('received {!r}'.format(data))
        print(data)

        break

      if data[12:16] == b'True': #Respuesta False -> No se pudo logear
        print ( "Logeado")
        Login_user = True #De lo contrario, se logea.
        dataeval = eval(data[16:])
        id_login = dataeval[0][0]
        rut_login = dataeval[0][1]
        #id_login = data[16:].decode("utf-8") 
        print(rut_login)
        print(id_login)

        #USUARIO LOGEADO, NUEVAS OPCIONES
        while True:
          print ("1.- crear una cuenta bancaria")
          print ("2.- verificar datos de usuario")
          print ("3.- realizar transferencia desde una cuenta")
          print ("4.- realizar pago de servicio desde una cuenta")
          print ("5.- ver datos de una cuenta")
          print ("6.- Salir")
          opcion = int(input("Ingrese numero respectivo a la opcion que desee realizar:"))

######################################################################
######################################################################
######################################################################
          if opcion == 1:
            if getsv('crcue') == 'OK':
                print("Por favor ingresar los siguientes datos")
                Numero = input("Numero de cuenta:")
                Tipo_idTipo = input("Tipo de cuenta: 1 para cuenta vista, 2 para cuenta corriente")
   
                pydata= {
                "Numero":0,
                "Saldo":0,
                "Usuario_idUsuario":0,
                "Tipo_idTipo":0,
                }

                pydata["Tipo_idTipo"] = int(Tipo_idTipo)
                ruts = str(rut_login)
                RutCuenta = ruts[0:(len(ruts)-1)]
                numero = int(str(Tipo_idTipo) + str(RutCuenta))
                pydata["Numero"] = numero
                pydata["Usuario_idUsuario"] = id_login

                Envio('crcue', pydata)

                while True:
                  data = sock.recv(250)
                  #dataeval = eval(data[16:])
                  if data[12:16] == 'True':
                    print("Cuenta creada con éxito")
                  elif data[12:24] == 'Falsecuenta':
                    print("Cuenta ya creada anteriormente")
                  elif data[12:16] == 'Falsenumero':
                    print("Ingrese un tipo de cuenta correcto, intente otra vez")
                  break

          elif opcion == 2:
            print("hola")

            pydata= {
              "Rut":rut_login
            }
            print(pydata["Rut"])
            Envio('infor',pydata)

            while True: #Espera hasta recibir la respuesta por parte del serivico
              data = sock.recv(250)
              break

            if data[12:16] == b'True':
              print("DATOS ->", data[16:])
            else:
              print("ERROR")

###############################################################
############################################################### TRANSFERENCIA
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
                          #idnumeros.append(dataeval[aux][2])
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
                        "cuenta":0,
                        "comentario":"",
                        "cuentadestino":0,
                        }

                        now = str(date.today())
                        pydata["monto"] = int(monto)
                        pydata["fecha"] = now
                        pydata["cuenta"] = idcuentas[select-1]
                        pydata["comentario"] = comentario
                        pydata["cuentadestino"] = int(cuentadestino)

                        Envio('rtran', pydata)

                        while True:
                            data = sock.recv(250)
                            break
                            
                        if data[12:16] == 'True':
                            print("Transferencia realizada con éxito con éxito")
                        elif data[12:22] == 'Falsesaldo':
                            print("Saldo insuficiente para realizar pago")
                        elif data[12:23] == 'Falsecuenta':
                            print("No existe la cuenta desde donde quiere transferir")
###############################################################
###############################################################
########################## Realizar pago servicio ############################## 
          elif opcion == 4:
            if getsv("pserv") == 'OK':
              print("PAGO DE SERVICIO")
              tipo_cuenta = input("1 -> pagar con cuenta vista  -  2 -> pagar con cuenta corriente")
              print("Si desea pagar el agua escriba: agua")
              print("Si desea pagar la luz escriba: luz")
              servicio_tipo = input("opcion:")
              print("Ingrese monto a pagar:")
              monto = input("monto:")

              pydata= {
              #"Tipo": "01" # 01+RUT cuenta vista 02+RUT cuenta corriente
              "Rut": rut_login,
              "Id_login": id_login,
              "Servicio": servicio_tipo,
              "Tipo_cuenta": int(tipo_cuenta),
              "Monto": int(monto),
              }
              Envio('pserv',pydata)

              data = b''
              while True:
                data = sock.recv(250)
                break

              if data[12:16] == b'True':
                print("PAGADO CTM", data)
              else:
                print("NO SE PUDO PAGAR", data)



########################## Cuentas ############################## 
          elif opcion == 5:
            if getsv('idcnt') == 'OK':
              pydata = {
                "idUsuario" : id_login
              }

              Envio('idcnt', pydata)

              idcuentas = []
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
                      #idnumeros.append(dataeval[aux][2])
                      print(aux+1,"- Tipo:",dataeval[aux][1],"Numero de cuenta:",dataeval[aux][2],"Saldo:",dataeval[aux][3])
                      aux = aux + 1
                  else:
                    print("ha ocurrido un error!")
                    error = True
                    break
                  break
              
              if error == False:
                while True:
                  select= int(input("Seleccione cuenta para ver datos historicos, ingrese 0 para volver"))
                  if select <= 0:
                    break
                  else:
                    print ("1.- ver trasnferencias emitidas anteriormente desde una cuenta")
                    print ("2.- ver transferencias recibidas anteriormente en una cuenta")
                    print ("3.- ver pagos realizados desde una cuenta")
                    print ("4.- Volver")
                    opcion = int(input("Ingrese numero respectivo a la opcion que desee realizar:"))

########################## TRANSFERENCIAS EMITIDAS ##############################  
      
                    if opcion == 1:
                      if getsv('hstem') == 'OK':
                        pydata = {
                          "idCuenta" : idcuentas[select-1]
                        }

                        Envio('hstem', pydata)

                        data = b''
                        while True:
                          data = sock.recv(250)
                          if data[12:16] == b'True':
                            dataeval = eval(data[16:])
                            print("Las transacciones enviadas historicamente son:")
                            aux = 0
                            while aux < len(dataeval):
                                print(dataeval[aux][3])
                                print(aux,"- Numero de cuenta destino:",dataeval[aux][2],"Monto:",dataeval[aux][0],"Fecha:",dataeval[aux][1],"Comentario:",dataeval[aux][3])
                                aux = aux + 1
                          else:
                            break
                          break
          
########################## TRANSFERENCIAS RECIBIDAS #############################
                    
                    elif opcion == 2:
                      if getsv('hstrb') == 'OK':
                        pydata = {
                          "idCuenta" : idcuentas[select-1]
                        }

                        Envio('hstrb', pydata)

                        data = b''
                        while True:
                          data = sock.recv(250)
                          if data[12:16] == b'True':
                            dataeval = eval(data[16:])
                            print("Las transacciones recividas historicamente son:")
                            aux = 0
                            while aux < len(dataeval):
                                print(aux,"- Numero de cuenta origen:",dataeval[aux][2],"Monto:",dataeval[aux][0],"Fecha:",dataeval[aux][1],"Comentario:",dataeval[aux][3])
                                aux = aux + 1
                          else:
                            break
                          break

########################## Pagos Realizados ####################################
                    
                    elif opcion == 3:
                      if getsv('hspag') == 'OK':
                        pydata = {
                          "idCuenta" : idcuentas[select-1]
                        }

                        Envio('hspag', pydata)

                        data = b''
                        while True:
                          data = sock.recv(250)
                          if data[12:16] == b'True':
                            dataeval = eval(data[16:])
                            print("Los Pagos efectuados historicamente son:")
                            aux = 0
                            while aux < len(dataeval):
                                print(aux,"- Servicio:",dataeval[aux][0],"Monto:",dataeval[aux][1],"Fecha:",dataeval[aux][2])
                                aux = aux + 1
                          else:
                            break
                          break

          else:
            print("Hasta luego =)")
            break






      else:
        
        print ("no se pudo logar")

############################ CREAR CUENTA #########################################
  elif opcion == 2:
    if getsv('crear'):
      print("Por favor ingresar los siguientes datos")
      Nombre = input("Nombre:")
      Email = input("Email:")
      Password = input("Password:")
      RUT = input("RUT sin punto ni guion:")
      Edad = input("Edad:")
      Telefono = input("Telefono (9 digitos):")

      pydata= {
        "Nombre":"",
        "Email":"",
        "Password":"",
        "RUT":"",
        "Edad": 0,
        "Telefono": 0,
      }
      pydata["Nombre"] = Nombre
      pydata["Email"] = Email
      pydata["Password"] = Password
      pydata["RUT"] = RUT
      pydata["Edad"] = int(Edad)
      pydata["Telefono"] = int(Telefono)
      Envio('crear',pydata)

      while True:
        data = sock.recv(250)
        print(data)
        break

      if data[10:] == b'False':
        print ("no se pudo crear la cuenta")
      else:
        print ( "Cuenta creada")

####################################################################################
####################################################################################
####################################################################################
####################################################################################
  else:
    print("ADIOS")
    break
