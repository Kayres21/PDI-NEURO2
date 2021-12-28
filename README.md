# Prototipo de Modelado de Jugador

## Dependencias

### Ejecución del código

Antes de instalar los paquetes, se recomienda el uso de un entorno virtual, ya sea mediante virtualenv o conda.

~~~
pip install numpy matplotlib opencv-python fpdf pyside6 
~~~


### Creación de Ejecutable

Si se quiere crear un ejecutable, hay que instalar otro paquete.

~~~
pip install auto-py-to-exe
~~~

La instalación puede realizarse vía auto-py-to-exe, lo que permite realizar configuraciones y personalizar. Sin embargo, para crear el ejecutable se ocupó el siguiente comando:

~~~
pyinstaller --noconfirm --onefile --console --add-data "PATH/TO/CODE/mediapipe;mediapipe/"  "PATH/TO/CODE/main.py"
~~~
