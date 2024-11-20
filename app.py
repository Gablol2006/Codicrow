from flask import Flask, render_template, request, redirect, session, url_for, flash
import sqlite3 as sql

from flask import Flask, render_template, request, jsonify
import subprocess
import os

app = Flask(__name__)  #Inicializar app

#Enlaces html ##############################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Alglory')
def Alglory():
    return render_template('Alglory.html')

@app.route('/Categoria')
def Categoria():
    return render_template('Categoria.html')

@app.route('/cuenta')
def cuenta():
    if 'user' in session:   
        user_email = session['user']   
        try:
            con = sql.connect("registro_usuarios.db")
            cur = con.cursor()
            cur.execute("SELECT name, mail FROM Usuarios WHERE mail = ?", (user_email,))
            user_data = cur.fetchone()  # Obtiene los datos del usuario
            
            if user_data:
                user_info = {
                    'name': user_data[0],
                    'mail': user_data[1]
                }
                return render_template('cuenta.html', user_info=user_info)  # Pasa la información a la plantilla
            else:
                return redirect(url_for('login'))
        except sql.Error as e:
            return redirect(url_for('cuenta'))
        finally:
            if con:
                con.close()
    else:
        return redirect(url_for('login'))

    return redirect(url_for('cuenta'))

@app.route('/cambiarcontra')
def cambiarcontra():
    return render_template('cambiarcontra.html')

@app.route('/cambiarfoto')
def cambiarfoto():
    return render_template('cambiarfoto.html')

@app.route('/editarPerfil')
def editarPerfil():
    return render_template('editarPerfil.html')

@app.route('/modificarContraseña', methods=['POST'])
def modificarContraseña():
    user_mail = request.form['mail']
    new_pin = request.form['pin']

    try:
        # Usar un contexto seguro para la conexión
        with sql.connect("registro_usuarios.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE Usuarios SET pin = ? WHERE mail = ?", (new_pin, user_mail))
            con.commit()
            flash("Contraseña actualizada correctamente.", "success")

    except sql.Error as e:
        flash("Ocurrió un error al guardar los cambios.", "error")
    return redirect(url_for('login')) 


@app.route('/guardar_cambios', methods=['POST'])
def guardar_cambios():
    if 'user' in session:
        user_email = session['user']
        new_name = request.form['name']
        new_email = request.form['email']
        new_pin = request.form['pin']
        
        try:
            con = sql.connect("registro_usuarios.db")
            cur = con.cursor()
            cur.execute("UPDATE Usuarios SET name = ?, mail = ?, pin = ? WHERE mail = ?", (new_name, new_email, new_pin, user_email))
            con.commit()

            session['user'] = new_email

        except sql.Error as e:
            flash("Ocurrió un error al guardar los cambios.", "error")
        finally:
            if con:
                con.close()
        
        return redirect(url_for('index')) 
    else:
        flash("No has iniciado sesión", "error")
        return redirect(url_for('login'))


@app.route('/recuperarContra')
def recuperarContra():
    return render_template('recuperarContra.html')

@app.route('/ejercicio')
def ejercicio():
    return render_template('ejercicio.html')

@app.route('/registro', methods=['POST', 'GET'])
def registro():
    if request.method == 'POST':
        try:
            name = request.form['name']
            mail = request.form['mail']
            city = request.form['city']
            pin = request.form['pin']
            
            with sql.connect("registro_usuarios.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Usuarios (name, mail, city, pin) VALUES (?, ?, ?, ?)", (name, mail, city, pin))
                con.commit()
                msg = "Record successfully added!"
        except:
            con.rollback()
            msg = "Error in insert operation"
        
        return render_template("login.html", msg=msg)
 
    return render_template("registro.html")

@app.route('/cerrar_sesion')
def cerrar_sesion():
    session.pop('user', None)   
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for('index'))   

@app.route('/eliminar_cuenta', methods=['POST'])
def eliminar_cuenta():
    if 'user' in session:
        user_email = session['user']
        try:
            con = sql.connect("registro_usuarios.db")
            cur = con.cursor()
            cur.execute("DELETE FROM Usuarios WHERE mail = ?", (user_email,))
            con.commit()
            flash("Cuenta eliminada correctamente", "success")
        except sql.Error as e:
            flash(f"Ocurrió un error al eliminar la cuenta: {str(e)}", "error")
        finally:
            if con:
                con.close()
        session.pop('user', None)  
        return redirect(url_for('index'))
    else:
        flash("No has iniciado sesión", "error")
        return redirect(url_for('index'))

@app.route('/ide')
def ide():
    return render_template('ide.html')

app.secret_key = 'victor x akemy'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['mail']
        pin = request.form['pin']

        try:
            con = sql.connect("registro_usuarios.db")
            cur = con.cursor()

            cur.execute("SELECT * FROM Usuarios WHERE mail = ? AND pin = ?", (mail, pin))
            user = cur.fetchone()

            if user:
                session['user'] = mail
                return redirect(url_for('index'))  
            else:
                return redirect(url_for('login'))
        except sql.Error as e:
            flash(f"Ocurrió un error: {str(e)}", "error")
            return redirect(url_for('login'))
        finally:
            if con:
                con.close() 

    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/puntuacion')
def puntuacion():
    return render_template('puntuacion.html')

@app.route('/seleccionLenguaje')
def seleccionLenguaje():
    return render_template('seleccionLenguaje.html')

@app.route('/seleccionLenguajeInt')
def seleccionLenguajeInt():
    return render_template('seleccionLenguajeInt.html')

@app.route('/seleccionLenguajeAv')
def seleccionLenguajeAv():
    return render_template('seleccionLenguajeAv.html')

#-------------------------------(IDE)-----------------------------------------------

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    code = data['code']
    language = data['language']

    # Guardar el código en un archivo según el lenguaje
    if language == 'python':
        filename = 'temp.py'
        with open(filename, 'w') as f:
            f.write(code)
        try:
            # Ejecutar el código Python
            result = subprocess.run(['python', filename], capture_output=True, text=True)

            output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = str(e)

    elif language == 'c':
        filename = 'temp.c'
        with open(filename, 'w') as f:
            f.write(code)
        try:
            # Compilar el código C
            compile_result = subprocess.run(['gcc', filename, '-o', 'temp_c'], capture_output=True, text=True)
            if compile_result.returncode != 0:
                output = compile_result.stderr
            else:
                # Ejecutar el archivo compilado
                result = subprocess.run(['./temp_c'], capture_output=True, text=True)
                output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = str(e)

    elif language == 'cpp':
        filename = 'temp.cpp'
        with open(filename, 'w') as f:
            f.write(code)
        try:
            # Compilar el código C++
            compile_result = subprocess.run(['g++', filename, '-o', 'temp_cpp'], capture_output=True, text=True)
            if compile_result.returncode != 0:
                output = compile_result.stderr
            else:
                # Ejecutar el archivo compilado
                result = subprocess.run(['./temp_cpp'], capture_output=True, text=True)
                output = result.stdout if result.returncode == 0 else result.stderr
        except Exception as e:
            output = str(e)

    # Limpiar archivos temporales (opcional)
    try:
        os.remove(filename)
        if language == 'c':
            os.remove('temp_c')
        elif language == 'cpp':
            os.remove('temp_cpp')
    except:
        pass

    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(debug=True)

#-------------------------------------(IDE)-------------------------------------------
