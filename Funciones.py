from PIL import Image
import numpy as np

def get_grid_coords(h, w, dot_size, angle_deg):
    positions = []
    angle_rad = np.radians(angle_deg)
    cx, cy = w / 2, h / 2 # centro de la imagen

    # calcular la dimension de la grilla
    diag = int(np.hypot(w, h))
    num_x = diag // dot_size + 3
    num_y = diag // dot_size + 3

    # alinear el centro de la grilla con el centro de la imagen
    offset_x = cx - (num_x * dot_size) / 2 
    offset_y = cy - (num_y * dot_size) / 2

    # recorrer la grilla y calcular las posiciones (geometría 👻) 
    for i in range(num_y):
        for j in range(num_x):
            gx = offset_x + j * dot_size + dot_size / 2 - cx
            gy = offset_y + i * dot_size + dot_size / 2 - cy
            rx = gx * np.cos(angle_rad) - gy * np.sin(angle_rad) + cx
            ry = gx * np.sin(angle_rad) + gy * np.cos(angle_rad) + cy

            ix, iy = int(round(rx)), int(round(ry))
            if 0 <= iy < h and 0 <= ix < w:
                positions.append((ix, iy))
    return positions

def cargarImg(ruta_imagen:str) -> tuple:
    """
    Funcion utilizada para cargar la imagen y verificar que se haya cargado correctamente.
    Args:
        ruta_imagen (str): Ruta de la imagen a cargar
    Returns:
        estado (int): Estado de la carga de la imagen (0 si se cargo correctamente, 1 si hubo un error)
        img (PIL.Image): Imagen cargada
    """
    
    try:
        img = Image.open(ruta_imagen).convert("RGB")
    except:
        print("Error importando la imagen")
        return 1, None
    return 0 , img

def dibujar_circulo(matriz: np.array, centro_x: int, centro_y: int, radio: float):
    """
    Funcion utilizada en el metodo halftone para generar el circulo de radio "n" lleno de "0" en la matriz de un color en especifico.

    Args:
        matriz (np.array): matriz del color en el que se va a dibujar el circulo
        centro_x (int): Valor x del centro del circulo
        centro_y (int): Valor y del centro del circulo
        radio (float): Radio del circulo
    """
    
    alto, ancho = matriz.shape # Obtener dimensiones de la matriz
    
    for y in range(int(centro_y - radio), int(centro_y + radio) + 1):
        for x in range(int(centro_x - radio), int(centro_x + radio) + 1):
            if 0 <= x < ancho and 0 <= y < alto: # Verificar que el pixel este dentro de la matriz
                if (x - centro_x)**2 + (y - centro_y)**2 <= radio**2: # Verificar que el pixel este dentro del circulo
                    matriz[y, x] = 0 # Asignar el valor del pixel a 0

def efecto_Halftone(img: Image, tam_puntos:int, ang_rot_red:int, ang_rot_green: int, ang_rot_blue: int)-> Image:
    '''
    Funcion utilizada para aplicar el efecto halftone a la imagen.
    Args:
        img (PIL.Image): Imagen a la que se le va a aplicar el efecto halftone
        tam_puntos (int): Tamaño de los puntos del efecto halftone
        ang_rot_red (int): Angulo de rotacion del color rojo
        ang_rot_green (int): Angulo de rotacion del color verde
        ang_rot_blue (int): Angulo de rotacion del color azul
    
    returns:
        imagen_efecto_halftone (PIL.Image): Imagen con el efecto halftone aplicado
    '''
    
    ancho , alto = img.size # Obtener dimensiones de la imagen
    
    pixels = np.array(img) # Convertir la imagen a un array de numpy

    rojo = pixels[:, :, 0]   # Separar canal R
    verde = pixels[:, :, 1]  # Separar canal G
    azul = pixels[:, :, 2]   # Separar canal B
    
    array_full_rojo = np.full((alto, ancho), 255) # Crear una matriz llena de 255 para el canal rojo
    array_full_verde = np.full((alto, ancho), 255) # Crear una matriz llena de 255 para el canal rojo
    array_full_azul = np.full((alto, ancho), 255) # Crear una matriz llena de 255 para el canal rojo
        
    puntos_centrados_rojo = get_grid_coords(alto, ancho, tam_puntos, ang_rot_red) # Obtener las coordenadas de los puntos para el canal rojo
    puntos_centrados_verde = get_grid_coords(alto, ancho, tam_puntos, ang_rot_green) # Obtener las coordenadas de los puntos para el canal verde
    puntos_centrados_azul = get_grid_coords(alto, ancho, tam_puntos, ang_rot_blue) # Obtener las coordenadas de los puntos para el canal azul
       
    # Dibujar los circulos en la matriz de cada color
    # Rojo
    for coords_rojo in puntos_centrados_rojo:
        x , y = coords_rojo
        intensidad = rojo[y, x]
        radio = (1 - (intensidad / 255)) * tam_puntos * 0.7
        dibujar_circulo(array_full_rojo, x, y, radio)

    # Verde
    for coords_verde in puntos_centrados_verde:
        x , y = coords_verde
        intensidad = verde[y, x]
        radio = (1 - (intensidad / 255)) * tam_puntos * 0.7
        dibujar_circulo(array_full_verde, x, y, radio)
        
    # Azul
    for coords_azul in puntos_centrados_azul:
        x, y = coords_azul
        intensidad = azul[y, x]
        radio = (1 - (intensidad / 255)) * tam_puntos * 0.7
        dibujar_circulo(array_full_azul, x, y, radio)
    
    # Junta las 3 arrays de colores en una sola
    array_final = np.stack((array_full_rojo, array_full_verde, array_full_azul), axis=2)

    # Convierte el array a una imagen
    imagen_efecto_halftone = Image.fromarray(array_final.astype(np.uint8))
    
    return imagen_efecto_halftone

def k_means(img: Image, cant_colores:int)-> Image:
    '''
    Funcion utilizada para aplicar el efecto k-means a la imagen.
    Args:
        img (PIL.Image): Imagen a la que se le va a aplicar el efecto k-means
        cant_colores (int): Cantidad de colores deseados
    Returns:
        imagen_efecto_k_means (PIL.Image): Imagen con el efecto k-means aplicado
    '''
    pixels = np.array(img)
    lista_pixeles = pixels.reshape(-1, 3)
    centroides = lista_pixeles[np.random.choice(len(lista_pixeles), cant_colores , replace = False)]
    
    for _ in range(100):  #Cantidad de iteraciones para terminar la cuantizacion K_means
        etiquetas = asignar_clusters(lista_pixeles, centroides)
        nuevos_centroides = np.array([lista_pixeles[etiquetas == i].mean(axis=0) if np.any(etiquetas == i) else centroides[i] for i in range(cant_colores)])
        if np.allclose(centroides, nuevos_centroides):
            break
        centroides = nuevos_centroides

    nueva_img_data = centroides[etiquetas].astype(np.uint8)
    nueva_img = nueva_img_data.reshape(pixels.shape)
    imagen_efecto_k_means = Image.fromarray(nueva_img)
    return imagen_efecto_k_means

def asignar_clusters(lista_pixeles, centroides) -> np.array:
    '''
    Funcion utilizada para asignar los pixeles a los centroides mas cercanos.
    Args:
        lista_pixeles (np.array): Lista de pixeles de la imagen
        centroides (np.array): Centroides de los colores
    Returns:
        np.array: Array con las etiquetas de los clusters
    '''
    
    distancias = np.linalg.norm(lista_pixeles[:, None] - centroides[None, :], axis=2) #Distancia euclidiana en el espacio RGB
    return np.argmin(distancias, axis=1)
