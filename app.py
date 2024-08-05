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


