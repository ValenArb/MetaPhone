###############################################################
#--------------------------VARIABLES--------------------------#
###############################################################
Max_Record_Time = 120 
# ↑ ↑ ↑ Tiempo maximo de grabacion en segundos
Max_Timeout_Start_Menu = 20 #BASE ---> 20 seconds
# ↑ ↑ ↑ Tiempo maximo que si el usuario, una vez terminado el audio de bienvenida, 
# tiene para apretar una tecla, sino aprieta nada, lleva a el audio de finalizacion
Max_Timeout_Record_Menu = 5 #BASE ---> 5 seconds
# ↑ ↑ ↑ Tiempo maximo en que si el usuario no aprieta 9 al terminar de grabar lo lleva a la finalizacion de la grabacion
Max_Timeout_Code_Keypress = 10
# ↑ ↑ ↑ Tiempo maximo para el ingreso del codigo. Cualquie tecla presionada durante este tiempo se guarda
Volume_Multiplier = 3 #Multiplier
# ↑ ↑ ↑ Multiplicador de volumen para el parlante
Send_Message_Key = 1
# ↑ ↑ ↑ Tecla usada para enviar mensaje
Random_Message_Key = 2
# ↑ ↑ ↑ Tecla usada para recibir un mensaje aleatorio
Code_Message_Key = 3
# ↑ ↑ ↑ Tecla usada para ingresar un codigo
Stop_Record_Key = 0
# ↑ ↑ ↑ Tecla usada para detener la grabacion
Retry_Record_Key = 9
# ↑ ↑ ↑ Tecla usada para reintentar la grabacion