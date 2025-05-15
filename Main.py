from Funciones import *

while True:
    metodo = (input("Seleccione el método de cuantización (halftone/kmeans): ")).lower()
    if metodo == "halftone" or metodo == "kmeans":
        break
    else:
        print("Ingrese un metodo valido")

estado = 1

while estado != 0:
    ruta = input("Ingrese el nombre de la imagen (nombre.formato): ")
    estado, imagen = cargarImg(ruta)
    if estado == 0:
        print("Imagen cargada correctamente!")

if metodo == "halftone":
    nombrefinal = ruta.split(".")[0] + "_halftone.png"
    
    while True:
        tamaño_puntos = input("Ingrese el tamaño de los puntos: ")
        if tamaño_puntos == "":
            tamaño_puntos = 5
            break
        else:
            try:
                tamaño_puntos = int (tamaño_puntos)
                if tamaño_puntos <= 0:
                    print("El tamaño de puntos debe ser mayor a 0")
                    continue
                else:
                    break
            except:
                print("Ingrese un numero valido")
    while True:
        angulo_rotacion_rojo = input("Ingrese el angulo de rotación rojo: ")
        if angulo_rotacion_rojo == "":
            angulo_rotacion_rojo = 15
            break
        else:
            try:
                angulo_rotacion_rojo = int(angulo_rotacion_rojo)
                if angulo_rotacion_rojo <= 0:
                    print("El angulo de rotacion debe ser mayor a 0")
                    continue
                else:
                    break
            except:
                print("Ingrese un numero valido")
                
        
    while True:    
        angulo_rotacion_verde = input("Ingrese el angulo de rotación verde: ")
        if angulo_rotacion_verde == "":
            angulo_rotacion_verde = 45
            break
        else:
            try:
                angulo_rotacion_verde = int(angulo_rotacion_verde)
                if angulo_rotacion_verde <= 0:
                    print("El angulo de rotacion debe ser mayor a 0")
                    continue
                else:
                    break
            except:
                print("Ingrese un numero valido")
    
    while True:   
        angulo_rotacion_azul = input("Ingrese el angulo de rotación azul: ")
        if angulo_rotacion_azul == "":
            angulo_rotacion_azul = 0
            break      
        else: 
            try:
                angulo_rotacion_azul = int(angulo_rotacion_azul)
                if angulo_rotacion_azul <= 0:
                    print("El angulo de rotacion debe ser mayor a 0")
                    continue
                else:
                    break
            except:
                print("Ingrese un numero valido")
                
    imagen_modificada = efecto_Halftone(imagen, tamaño_puntos, angulo_rotacion_rojo, angulo_rotacion_verde , angulo_rotacion_azul)
    
elif metodo == "kmeans":
    nombrefinal = ruta.split(".")[0] + "_kmeans.png"
    while True:
        cant_colores = input("Ingrese la cantidad de colores deseados: ")
        if cant_colores == "":
            cant_colores = 8
            break
        else:
            try:
                cant_colores = int(cant_colores)
                if cant_colores <= 0:
                    print("La cantidad de colores debe ser mayor a 0")
                    continue
                break
            except:
                print("Ingrese un numero valido")
                
    imagen_modificada = k_means(imagen , cant_colores)

while True:
    respuesta = input("¿Que quiere hacer? \n 1. Mostrar imagen modificada\n 2. Mostrar ambas imagenes\n 3. Guardar imagen modificada \n")
    if respuesta == "1":
        imagen_modificada.show()
        break
    elif respuesta == "2":            
        # Crear una nueva imagen donde se van a pegar las dos imágenes
        # La imagen combinada tendrá el doble de ancho que la imagen original para que entren ambas imagenes
        imagen_combinada = Image.new("RGB", (imagen.width*2+10, imagen.height))

        # Pegar las imágenes
        imagen_combinada.paste(imagen, (0, 0))
    
        # Pego la imagen modificada a la derecha de la original con una separación de 10 píxeles
        imagen_combinada.paste(imagen_modificada, (imagen.width+10, 0))

        # Mostrar la imagen combinada
        imagen_combinada.show()
        
        break
    elif respuesta == "3":
        imagen_modificada.save(nombrefinal)
        print("Imagen guardada como: ", nombrefinal)
        break
    else:
        print("Ingrese una opcion valida")