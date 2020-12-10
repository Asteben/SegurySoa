import socket
import sys
import json

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address given on the command line

server_address = ('200.14.84.235', 5000)
print('starting up on {} port {}'.format(*server_address))
sock.connect(server_address)


def generate_tx_length(tx_length):
    # Cantidad de caracteres máximos para definir el largo de la transacción (5 según formato solicitado por el bus)
    char_ammount = 5
    # Espacios sobrantes para rellenar con 0 a la izquierda
    char_left = char_ammount - len(str(tx_length))

    str_tx_length = ''
    for i in range(char_left):
      str_tx_length += '0'

    str_tx_length += str(tx_length)  # String con el largo de la transacción
    return str_tx_length

############################################################################################


def Envio(servicio, data):

  jsondata = json.dumps(data)
  message = bytes(jsondata, 'utf-8')

  tx_cmd = servicio + message  # Comando de registro de servicio ante el bus
  tx = generate_tx_length(len(tx_cmd)) + tx_cmd

  sock.send(tx.encode(encoding='UTF-8'))

############################################################################################


def getsv(servicio):
	tx_cmd = 'getsv' + service_name  # Comando de registro de servicio ante el bus
    tx = generate_tx_length(len(tx_cmd)) + tx_cmd

  sock.send(tx.encode(encoding='UTF-8'))

  status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)
  return status


############################################################################################
serv_login = 'login'
serv_crearusuario = 'rgstr'
serv_crearcuenta = 'cuent'
serv_info = 'infor'
serv_transferencia = 'trans'
serv_pago = 'servi'
serv_historialpago = 'hspag'
serv_historialtransfemitidas = 'hstem'
serv_historialtransfrecibidas = 'hstrb'

print("BIENVENIDO A SEGURYSOA! =)")

while true:
    print("1.- Realizar LogIn")
    print("2.- Registrar Usuario")
    print("3.- Salir")
    
    opcion = int(input("Ingrese numero respectivo a la opcion que desee realizar:"))

########################## REALIZAR LOGIN ##########################  

    if opcion == 1:
			
        
        
        
        
        recb1 = 'ALGO'
        
        
########################## LUEGO DEL LOGIN ##########################    
        if recb1 == 'true':
            # llama a infocuenta
            print("ELIJA QUE DESEA RELIZAR DENTRO DE SU USUARIO")
            while true:
                print ("1.- crear una cuenta bancaria")
                print ("2.- verificar datos de una cuenta")
                print ("3.- realizar transferencia desde una cuenta")
                print ("4.- realizar pago de servicio desde una cuenta")
                print ("5.- ver trasnferencias emitidas anteriormente desde una cuenta")
                print ("6.- ver transferencias recibidas anteriormente en una cuenta")
                print ("7.- ver pagos realizados desde una cuenta")
                print ("8.- Salir")
                
                
                opcion1 = int(input("Ingrese un número:"))
  
                    
########################## CREAR CUENTA ##########################    
  
                if opcion1 == 1:
                    # llama a crear_cuenta
                    print ("Por favor ingrese los siguiente datos:")
                    Numero = input(("Número de cuenta:"))
                    Nombre = input(("Nombre de usuario:"))
                    Tipo = input(("Tipo de cuenta: 01 para cuenta vista, 02 para cuenta corriente"))
                    
                    pydata = {"map" = true}
        
                    pydata["Numero"] = Numero
                    pydata["Nombre"] = Nombre
                    pydata["Tipo"] = Tipo
                      
                    
                    service_name = 'cuent'
                    tx_cmd = 'getsv'+ service_name  # Comando de registro de servicio ante el bus
										tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    
                    sock.send(tx.encode(encoding='UTF-8'))
                    
                    status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)
                    print(status)
                    print("_______")
                    
                    jsondata = json.dumps(pydata)
                    message = bytes(jsondata, 'utf-8') 
                            
                    tx_cmd = service_name + message # Comando de registro de servicio ante el bus
                    tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    
                    sock.send(tx.encode(encoding='UTF-8'))
                    status = sock.recv(4096).decode('UTF-8')[10:12] 
                    
                    if status == 'OK':
        	              while True: #Espera hasta recibir la respuesta por parte del serivico
                            data = sock.recv(250)
                            print('received {!r}'.format(data))
                            print(data)
                            break
                        
                              
        		               if data == b'False': #Respuesta False -> No se pudo crear cuenta, existe una cuenta con este número
            	                  print ("No se pudo crear la cuenta, ya existe una con este número")
                        
        		                else:
                                Login_user = True #De lo contrario, se crea cuenta.
                                print ( "Cuenta creada con exito")
                         
                    else:
        	              print("un error! a ocurrido =(")
                        
        
                    
########################## DATOS DE UNA CUENTA (INFO) ##########################  
                elif opcion1 == 2:
                    # llama a info
                    
########################## REALIZAR TRANSFERENCIA ##########################  
                elif opcion1 == 3:
                    # llama a realizar_transferencia
                    print ("Por favor ingrese los siguiente datos:")
                    Monto = input(("Monto a transferir:"))
                    Comentario = input(("Comentario:"))
                    Cuenta_idCuenta = input(("Numero de cuenta emisora:"))
                    Numero_cuenta_destino = input(("Numero de cuenta destino:"))
                    
                    pydata = {"map" = true}
        
                    pydata["Monto"] = Monto
                    pydata["Comentario"] = Comentario
                    pydata["Cuenta_idCuenta"] = Cuenta_idCuenta
                    pydata["Numero_cuenta_destino"] = Numero_cuenta_destino

                    service_name = 'trans'
                    tx_cmd = 'getsv'+ service_name  # Comando de registro de servicio ante el bus
										tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    
                    sock.send(tx.encode(encoding='UTF-8'))
                    
                    status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)
                    print(status)
                    print("_______")
                    
                    jsondata = json.dumps(pydata)
                    message = bytes(jsondata, 'utf-8') 
                            
                    tx_cmd = service_name + message # Comando de registro de servicio ante el bus
                    tx = generate_tx_length(len(tx_cmd)) + tx_cmd
                    
                    sock.send(tx.encode(encoding='UTF-8'))
                    status = sock.recv(4096).decode('UTF-8')[10:12] 
                    
                    if status == 'OK':
        	              while True: #Espera hasta recibir la respuesta por parte del serivico
                            data = sock.recv(250)
                            print('received {!r}'.format(data))
                            print(data)
                            break
                        
                              
        		               if data == b'False_monto': #Respuesta False -> No hay dinero suficiente para hacer la transferencia
            	                  print ("No se pudo realizar la transferencia, no hay dinero suficiente")
        		               
                           elif data == b'False_cuenta': #Respuesta False -> El número de cuenta no es correcto
            	                  print ("No se pudo realizar la transferencia, el número de cuenta no es correcto")
                            
                        
        		               else:
                                print ( "Transferencia realizada con éxito")
                         
                    else:
        	          	print("un error! a ocurrido =(")
                    
########################## REALIZAR PAGO ##########################                  
                elif opcion1 == 4:
                    # llama a realizar_pago
                    
########################## TRANSFERENCIAS EMITIDAS ##########################  
      
                elif opcion1 == 5:
                	pydata = {"map" = true}
                  pydata["idCuenta"] = recb1["idCuenta"]

                  service_name = 'rgstr'

                  tx_cmd = 'getsv'+ service_name  # Comando de registro de servicio ante el bus
                  tx = generate_tx_length(len(tx_cmd)) + tx_cmd

                  sock.send(tx.encode(encoding='UTF-8'))

                  status = sock.recv(4096).decode('UTF-8')[10:12] # 'OK' (exitoso) o 'NK' (fallido)
                  # print(status)
                  # print("_______")

                  jsondata = json.dumps(pydata)  
                  message = bytes(jsondata, 'utf-8') 

                  tx_cmd = service_name + message # Comando de registro de servicio ante el bus
                  tx = generate_tx_length(len(tx_cmd)) + tx_cmd

                  sock.send(tx.encode(encoding='UTF-8'))

                  status = sock.recv(4096).decode('UTF-8')[10:12] 
        
                  while True:
                      data = sock.recv(250)
                      dataeval = eval(data)
                      print("Las transacciones enviadas historicamente son:")
                      aux = 0
                      while aux < len(dataeval):
                          print(dataeval[aux][3])
                          print(aux,"- Numero de cuenta destino:",dataeval[aux][2],"Monto:",dataeval[aux][0],"Fecha:",dataeval[aux][1],"Comentario:",dataeval[aux][3])
                          aux = aux + 1
                      break
                    
########################## TRANSFERENCIAS RECIBIDAS ##########################  
                    
                elif opcion1 == 6:
                
                    jsondata = json.dumps(pydata)
                    bjson = b'' + jsondata
                    sock.sendall(bjson)

                    data = b''
                    while True:
                        data = sock.recv(250)
                        dataeval = eval(data)
                        print("Las transacciones recividas historicamente son:")
                        aux = 0
                        while aux < len(dataeval):
                            print(aux,"- Numero de cuenta origen:",dataeval[aux][2],"Monto:",dataeval[aux][0],"Fecha:",dataeval[aux][1],"Comentario:",dataeval[aux][3])
                            aux = aux + 1
                        break
                    
########################## PAGOS REALIZADOS ##########################    
                
                elif opcion1 == 7:
                    # llama a historialpago
                    
########################## BREAK ##########################  

                elif opcion1 == 8:
                    break
                  
########################## REGISTRO ##########################     

    elif opcion == 2:
    		print("Por favor ingresar los siguientes datos")
        Nombre = input("Nombre:")
        Email = input("Email:")
        Password = input("Password:")
        RUT = input("RUT sin punto ni guion:")
        Edad = input("Edad:")
        Telefono = input("Telefono (9 digitos):")
        
        pydata = {"map" = true}
        
        pydata["Nombre"] = Nombre
        pydata["Email"] = Email
        pydata["Password"] = Password
        pydata["RUT"] = RUT
        pydata["Edad"] = Edad
        pydata["Telefono"] = Telefono
        
        status = getsv("crear")
        
        if status == 'OK':
        	Envio("rgstr", pydata)
        	while True: #Espera hasta recibir la respuesta por parte del serivico
        		data = sock.recv(250)
            print('received {!r}'.format(data))
            print(data)
            break

        		if data[10:] == b'False': #Respuesta False -> No se pudo crear cuenta
            	print ("No se pudo crear la cuenta")

        		else:
              Login_user = True #De lo contrario, se crea cuenta.
              print ( "Cuenta creada con exito")

        else:
        	print("un error! a ocurrido =(")
          
########################## SALIR ##########################  
    elif opcion == 3:
    		print("Hasta luego =)")
        break
        
########################## ERROR ##########################  
    else:
        print("Ha ocurrido un error! por favor intentelo de nuevo =(")

