# Vaico works
## Pioneros.
### En camino de la senda dorada

Reconocimiento de cascos en obras de contrucción.

### Uso del cliente para capturar imagenes

Para utilizar el cliente que captura las imagenes, las procesa y las guarda en la base de datos se requiere descargar los pesos del modelo (yolo.h5) que estan en el siguiente enlace https://drive.google.com/drive/folders/1g7rp13kWP2dhKc0GQb7dVORwMFSALiMf?usp=sharing. Una vez descargado, se deben poner en un directorio llamado "models_h5/",despues de esto se debe clonar el repositorio y se deben poner en el mismo directorio la carpeta de los modelos y la carpeta del repositorio: vaico_works/ models_h5/ 

Una vez se haga esto, ya se puede ejecutar el cliente que esta en:

vaico_works/cam_client/cam_client.py

### Inferencia

Para realizar inferencia con el modelo ya entrenado, se deben haber descargado los pesos del modelo (model_ex-055_acc-0.996250.h5) en el siguiente enlace https://drive.google.com/drive/folders/1g7rp13kWP2dhKc0GQb7dVORwMFSALiMf?usp=sharing, y se debe poner en el directorio creado anteriormente, "models_h5/", tambien se debe descargar el archivo "model_class.json" en el cual se hace el mapeo de las predicciones y las clases correspondientes y se debe ubicar en el mismo directorio "models_h5/"
