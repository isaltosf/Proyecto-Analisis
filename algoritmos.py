def procesarXOR(cadenaNumerica, clave = "abcd"):
    if len(cadenaNumerica) == 0 or len(clave) == 0:
      return ""

    resultado = ""

    for i in range(len(cadenaNumerica)):
      valorCharMensaje = ord(cadenaNumerica[i])
      indiceClave = i % len(clave)
      valorCharClave = ord(clave[indiceClave])
      valorXOR = valorCharMensaje ^ valorCharClave
      resultado += chr(valorXOR)

    return resultado

def codificar(cadenaNumerica):

  indice = 0
  digitoEncontrado = 0
  resultado = ""
  mascaraVisitados = [False, False, False, False, False, False, False, False, False, False]
  mascaraDigitosPresentes = [False, False, False, False, False, False, False, False, False, False]
  key = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
  
  for digito in cadenaNumerica:
    digitoNumerico = int(digito)
    mascaraDigitosPresentes[digitoNumerico] = True
  
  for digito in cadenaNumerica:
    digitoNumerico = int(digito)
    if(not mascaraVisitados[digitoNumerico]):
      resultado += digito
      mascaraVisitados[digitoNumerico] = True
    else:
      digitoIzquierda = digitoNumerico - 1
      digitoDerecha = digitoNumerico + 1
      if(digitoIzquierda < 0):
        digitoIzquierda = 0
      if(digitoDerecha > 9):
        digitoDerecha = 9

      while(mascaraDigitosPresentes[digitoIzquierda] and mascaraDigitosPresentes[digitoDerecha]):
        if(digitoIzquierda > 0):
          digitoIzquierda -= 1
        if(digitoDerecha < 9):
          digitoDerecha += 1

      if(not mascaraDigitosPresentes[digitoIzquierda]):
        digitoEncontrado = digitoIzquierda
      else:
        digitoEncontrado = digitoDerecha

      key[indice] = str(digitoEncontrado - digitoNumerico)
      mascaraDigitosPresentes[digitoEncontrado] = True
      mascaraVisitados[digitoEncontrado] = True
      resultado += str(digitoEncontrado)
    indice += 1
  resultado = resultado + "|" + ",".join(key)
  return resultado

def decodificar(cadenaCodificada, key):
  indice = 0
  resultado = ""
  
  for digito in cadenaCodificada:
    digitoNumerico = int(digito)
    digitoKey = int(key[indice])
    digitoFinal = digitoNumerico
    if(digitoKey != 0):
      digitoFinal = digitoNumerico + (-1 * digitoKey)
    resultado += str(digitoFinal)
    indice += 1
  
  return resultado


'''
cadena = "202312583"
clave = "holamundo"

cadenaCodificada = procesarXOR(cadena, clave)
print(cadenaCodificada)
print(len(cadenaCodificada))
cadenaOriginal = procesarXOR(cadenaCodificada, clave)
print(cadenaOriginal)

'''

'''
cadena = "202312583"

cadenaCodificada = codificar(cadena)
print(cadenaCodificada)

arrayCadena = cadenaCodificada.split("|")


cadenaOriginal = decodificar(arrayCadena[0], arrayCadena[1].split(','))
print(cadenaOriginal)
'''

