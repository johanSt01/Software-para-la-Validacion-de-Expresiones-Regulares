import re

#iniciar la ejecucio del codigo
def ejecutarCodigo():
    """
        Comenzar con la ejecucion del programa obteniendo la expresion y validandola
    """

    expresion_regular = leerExpresionRegular() #se obtiene la exprecion

    analisisLexico(expresion_regular)#analisis lexico

    print (analisisSintactico(expresion_regular))#analisis sintactico

    pertenece_a_expresion(expresion_regular,'holamundooooooo')


#hacer el analisis lexico a la expresion
def analisisLexico(expresion_regular: str):
    """
    Realizar el análisis léxico a la expresión regular, asegurándose de que todos
    los elementos ingresados sean procesables.
    
    Parametros:
    - expresion_regular (str): La expresión regular a analizar.
    
    Retorna:
    - bool: True si todos los tokens son válidos, False en caso contrario.
    """
    # Conjunto de tokens válidos
    operadores_validos = {'*', '+', '{', '}', '|', '.', '@', ',',':',';','-'}
    
    # Tokeniza cada carácter individual de la expresión
    tokens = list(expresion_regular)
    
    for token in tokens:
        # Se verifica si el token es un número, una letra o un operador válido
        if not (token.isalnum() or token in operadores_validos):
            print(f"Token inválido encontrado: '{token}'")
            return False  
    
    print("Todos los tokens son válidos.")
    return True  # Retorna True si todos los tokens son válidos



#hacer el analisis sintactico a la expresion
def analisisSintactico(expresion_regular: str) -> bool:
    """
    Realizar el análisis sintáctico a la expresión, asegurando que sigue una sintaxis
    establecida mediante el uso de un autómata con las reglas especificadas.
    
    Parametros:
    - expresion_regular (str): La expresión regular a analizar.
    
    Retorna:
    - bool: True si la sintaxis es correcta, False en caso contrario.
    """
    # Estados iniciales y configuraciones
    estado = "INICIO"
    balance_llaves = 0
    i = 0
    longitud = len(expresion_regular)
    
    while i < longitud:
        token = expresion_regular[i]
        
        # Estado de inicio: espera una letra, número, o un operador válido (excluye *, +, |, {, })
        if estado == "INICIO":
            if token.isalnum():
                estado = "OPERANDO"
            elif token == '{':
                balance_llaves += 1
                estado = "EN_LLAVE"
            else:
                print(f"Error sintáctico: carácter inesperado '{token}' en el inicio.")
                return False

        # Estado OPERANDO: tras una letra, número o conjunto, puede seguir un operador o llave.
        elif estado == "OPERANDO":
            if token in {'*', '+'}:
                estado = "OPERADOR_UNARIO"
            elif token == '|':
                estado = "OPERADOR_BINARIO"
            elif token == '{':
                balance_llaves += 1
                estado = "EN_LLAVE"
            elif token == '}':
                print("Error sintáctico: llave de cierre sin apertura.")
                return False

        # Estado EN_LLAVE: espera letras, números, o un operador válido, pero no permite *, +, | al inicio o final del conjunto
        elif estado == "EN_LLAVE":
            if token == '}':
                balance_llaves -= 1
                estado = "OPERANDO"
            elif token in {'*', '+', '|'} and (i == 0 or expresion_regular[i-1] == '{'):
                print(f"Error sintáctico: operador '{token}' en posición inválida dentro de llaves.")
                return False
            elif token.isalnum() or token in {'.', '@', ',', '(', ')'}:
                estado = "EN_LLAVE"
            else:
                print(f"Error sintáctico: carácter '{token}' inesperado dentro de llaves.")
                return False

        # Estado OPERADOR_UNARIO: después de * o +, puede continuar con otro operador o llaves
        elif estado == "OPERADOR_UNARIO":
            if token == '|':
                estado = "OPERADOR_BINARIO"
            elif token.isalnum():
                estado = "OPERANDO"
            elif token == '{':
                balance_llaves += 1
                estado = "EN_LLAVE"
            else:
                print(f"Error sintáctico: carácter '{token}' inesperado tras operador unario.")
                return False

        # Estado OPERADOR_BINARIO: espera un operando después de un operador binario
        elif estado == "OPERADOR_BINARIO":
            if token.isalnum():
                estado = "OPERANDO"
            elif token == '{':
                balance_llaves += 1
                estado = "EN_LLAVE"
            else:
                print(f"Error sintáctico: carácter '{token}' inválido tras operador binario.")
                return False

        i += 1

    # Al finalizar, validar que las llaves estén balanceadas
    if balance_llaves != 0:
        print("Error sintáctico: llaves desbalanceadas.")
        return False

    print("La sintaxis es correcta.")
    return True



#validar si una cadena cumple una expresion regular
def pertenece_a_expresion(expresion_regular: str, cadena: str) -> bool:
    """
    Valida si una cadena pertenece a la expresión regular dada, considerando
    cerradura estrella (*), cerradura positiva (+) y unión (|), con concatenación.
    
    Parametros:
    - expresion_regular (str): La expresión regular en formato personalizado.
    - cadena (str): La cadena que se desea validar contra la expresión.
    
    Retorna:
    - bool: True si la cadena pertenece a la expresión regular, False en caso contrario.
    """
    # Se pasa la expresión personalizada a una expresión compatible con Python
    regex = convertir_a_regex(expresion_regular)
    
    # Se verifica si la cadena completa coincide con la expresión regular
    resultado = re.fullmatch(regex, cadena)
    
    # Si hay coincidencia, la cadena pertenece; si no, no pertenece
    if resultado:
        print(f"La cadena '{cadena}' pertenece a la expresión regular '{expresion_regular}'.")
        return True
    else:
        print(f"La cadena '{cadena}' NO pertenece a la expresión regular '{expresion_regular}'.")
        return False



#convertir la expresion personalidada a una expresion manejada por python
def convertir_a_regex(expresion_regular: str) -> str:
    """
    Convierte una expresión regular en formato personalizado a una expresión regular
    estándar de Python.
    
    Parametros:
    - expresion_regular (str): La expresión regular en formato personalizado.
    
    Retorna:
    - str: La expresión regular convertida para ser utilizada en re.fullmatch().
    """
    # Cadena donde se irá construyendo la expresión compatible con Python
    regex = ""
    i = 0
    longitud = len(expresion_regular)
    
    while i < longitud:
        token = expresion_regular[i]
        
        if token == '*':
            # Cerradura estrella, se agrega tal cual
            regex += '*'
        elif token == '+':
            # Cerradura positiva, se agrega tal cual
            regex += '+'
        elif token == '|':
            # Unión, se agrega tal cual
            regex += '|'
        elif token == '{':
            # Si se encuentra una llave abierta, se captura todo el conjunto dentro de ella
            conjunto = ""
            i += 1  # Avanza para saltar la llave abierta '{'
            while i < longitud and expresion_regular[i] != '}':
                conjunto += expresion_regular[i]
                i += 1
            # Agrupa el conjunto sin capturarlo
            regex += f"(?:{conjunto})"
        elif token.isalnum() or token in {'.', '@', ',', '(', ')'}:
            # Los operandos válidos se agregan directamente
            regex += token
        else:
            # Si hay un carácter no reconocido, se retorna una cadena vacía
            print(f"Carácter no reconocido en la expresión: {token}")
            return ""
        
        i += 1
    
    return regex




#leer una expresion regular
def leerExpresionRegular():
    """
        Solitiar al usuario una expresion regular para trabajar
    """
    return str(input('hola, por favor digita la exprecion regular'))







#iniciar programa
if __name__ == '__main__':
    ejecutarCodigo()