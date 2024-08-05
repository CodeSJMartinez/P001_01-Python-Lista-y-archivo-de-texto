# ¿Dónde se Almacena la Lista de Tareas?

Actualmente, las tareas se almacenan en una lista de Python dentro de la aplicación (Proyecto P001):

``` python 
tareas = []
```
Esta lista está definida en el ámbito de la aplicación Flask y se mantiene en la memoria del servidor mientras la aplicación está en ejecución. Sin embargo, esto significa que:

*Volatilidad de Datos:* La lista tareas reside en la memoria RAM del servidor, que es un almacenamiento temporal. Cuando la aplicación se cierra o se reinicia, esta memoria se borra, y con ella, las tareas almacenadas.

## ¿Por qué se Pierden las Tareas al Cerrar la Aplicación?

*Memoria Temporal:* Al estar en la memoria RAM, los datos no se guardan permanentemente.

*No Hay Persistencia:* No se utiliza un almacenamiento persistente (como una base de datos o un archivo) para guardar las tareas, por lo que no se pueden recuperar después de reiniciar la aplicación.

## Cómo Solucionar el Problema de Persistencia

Para mantener las tareas incluso después de cerrar y volver a abrir la aplicación, podemos usar una base de datos o un archivo de texto. Aquí te explicaré cómo implementar una solución simple utilizando un archivo de texto para guardar las tareas.

## Implementación Usando un Archivo de Texto
Vamos a modificar el código para guardar las tareas en un archivo de texto, lo que proporcionará persistencia a las tareas.

### Paso 1: Crear Funciones para Leer y Escribir Tareas
Primero, definiremos dos funciones: una para leer las tareas desde un archivo y otra para guardarlas.

``` python
def cargar_tareas():
    try:
        with open('tareas.txt', 'r') as archivo:
            return [linea.strip() for linea in archivo.readlines()]
    except FileNotFoundError:
        return []

def guardar_tareas(tareas):
    with open('tareas.txt', 'w') as archivo:
        for tarea in tareas:
            archivo.write(tarea + '\n')
```

*cargar_tareas():* Lee las tareas desde tareas.txt y las devuelve como una lista. Si el archivo no existe, devuelve una lista vacía.

*guardar_tareas(tareas):* Guarda las tareas actuales en tareas.txt.

### Paso 2: Modificar el Código para Usar estas Funciones
Modificaremos el código de app.py para utilizar estas funciones.

``` python
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# Cargar tareas al inicio
tareas = cargar_tareas()

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas)

@app.route('/add', methods=['POST'])
def add_tarea():
    tarea = request.form.get('tarea')
    if tarea:
        tareas.append(tarea)
        guardar_tareas(tareas)  # Guardar tareas en el archivo
    return redirect('/')

@app.route('/delete/<int:index>')
def delete_tarea(index):
    if 0 <= index < len(tareas):
        tareas.pop(index)
        guardar_tareas(tareas)  # Guardar tareas en el archivo
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
```

## Cómo Funciona el Código Modificado

*Persistencia de Datos:* Ahora, las tareas se guardan en tareas.txt. Cada vez que se agrega o elimina una tarea, la lista completa de tareas se guarda en este archivo.

*Recuperación de Datos:* Al iniciar la aplicación, las tareas se cargan desde tareas.txt para que el usuario pueda continuar donde lo dejó.

## Beneficios y Consideraciones

*Persistencia Sencilla:* Usar un archivo de texto es una manera sencilla de lograr persistencia sin complicaciones de configuración.

*Limitaciones:* Los archivos de texto son adecuados para aplicaciones pequeñas o pruebas, pero para aplicaciones más grandes o con más datos, una base de datos sería más apropiada.

*Escalabilidad:* Para escalar este proyecto, podrías usar SQLite, PostgreSQL, o cualquier otra base de datos para un manejo más eficiente y robusto de los datos.

Ahora, con estas modificaciones, las tareas permanecerán incluso después de cerrar la aplicación.

## Resumen de las Mejoras Realizadas

Las dos funciones que creamos para trabajar con el archivo de texto, cargar_tareas() y guardar_tareas(), deben ser definidas dentro del archivo app.py. Esto se debe a que son parte de la lógica central de la aplicación y deben ser accesibles por las rutas que manejan la adición y eliminación de tareas.

Aquí te muestro cómo debe quedar el archivo app.py con estas funciones integradas:

Archivo app.py Completo
``` python
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# Funciones para cargar y guardar tareas desde un archivo
def cargar_tareas():
    try:
        with open('tareas.txt', 'r') as archivo:
            return [linea.strip() for linea in archivo.readlines()]
    except FileNotFoundError:
        return []

def guardar_tareas(tareas):
    with open('tareas.txt', 'w') as archivo:
        for tarea in tareas:
            archivo.write(tarea + '\n')

# Cargar tareas al inicio desde el archivo
tareas = cargar_tareas()

@app.route('/')
def index():
    return render_template('index.html', tareas=tareas)

@app.route('/add', methods=['POST'])
def add_tarea():
    tarea = request.form.get('tarea')
    if tarea:
        tareas.append(tarea)
        guardar_tareas(tareas)  # Guardar tareas en el archivo
    return redirect('/')

@app.route('/delete/<int:index>')
def delete_tarea(index):
    if 0 <= index < len(tareas):
        tareas.pop(index)
        guardar_tareas(tareas)  # Guardar tareas en el archivo
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
```

## Ubicación de las Funciones

*Definición de Funciones:* Las funciones cargar_tareas() y guardar_tareas() se definen cerca del inicio del archivo app.py, después de la inicialización de Flask (app = Flask(__name__)) y antes de cargar las tareas y definir las rutas. Esto asegura que estén disponibles para su uso durante todo el ciclo de vida de la aplicación.

### Uso de las Funciones:

*cargar_tareas():* Se llama una vez al inicio para cargar las tareas existentes desde tareas.txt cuando la aplicación se inicia.

*guardar_tareas(tareas):* Se llama cada vez que se añade o elimina una tarea, asegurando que los cambios se reflejen en el archivo tareas.txt.

## Por Qué Guardarlas Aquí
Centralización de la Lógica: Al definir estas funciones dentro de app.py, mantenemos toda la lógica de manejo de tareas en un solo lugar, lo que hace que el código sea más fácil de seguir y mantener.

*Facilidad de Acceso:* Las funciones están fácilmente disponibles para todas las rutas y manejadores de eventos que necesitan cargar o guardar tareas, asegurando que siempre trabajen con la versión más actualizada de la lista de tareas.

## Consideraciones Adicionales

*Manejo de Archivos:* Asegúrate de que el archivo tareas.txt esté en la misma carpeta que app.py para que las funciones puedan acceder a él sin problemas.

*Persistencia Sencilla:* Esta solución es adecuada para aplicaciones pequeñas. Si necesitas manejar una cantidad mayor de datos o realizar operaciones más complejas, considera usar una base de datos como SQLite para un mejor manejo y escalabilidad.

Con esta configuración, tu aplicación estará lista para manejar tareas de manera persistente utilizando un archivo de texto. 