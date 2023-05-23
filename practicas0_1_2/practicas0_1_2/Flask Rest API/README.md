#--------------------------------------------------------------------------------------------
Hacer una segunda versión del api usando la librería flask-restfull, como en Python REST API Tutorial - Building a Flask REST API.
#--------------------------------------------------------------------------------------------

El código de la aplicación está contenido en la carpeta "app". Dentro de esta carpeta encontramos:

- Archivo "app.py":

Ejemplo de ejecución para cada petición:

        - Primero descargamos el fichero "recipes.json" con las recetas del repositorio 
        https://github.com/mongodb-developer/rewrite-it-in-rust/tree/master/data y lo incorporamos al 
        directorio "dump > cockteles"

        - En una terminal en el directorio "Flask REST API" lanzar el contenedor con: 
        > docker-compose up

        - y en otra terminal, abrimos una sesión de bash en el contenedor de mongo:
        > docker-compose exec mongo /bin/bash

        - y en la terminal del contenedor:
        > mongoimport --db cockteles --collection recipes dump/cockteles/recipes.json

        - Para cada ejercicio abrir el fichero de prueba "requests.http" en el directorio "templates" 
        (para que Visual Studio nos indique la opción para enviar la petición encima de cada una de ellas, 
        debemos tener instalada la extensión "REST Client" y abajo en la barra azul, en "Select Language Mode" 
        debemos seleccionar el lenguaje HTTP) y realizar una a una cada petición:

        1)  Devolverá una lista con todos los registrosn 
            GET http://localhost:5000/f_restfull/api/recipes HTTP/1.1

        2)  Devolverá una lista con las recetas que tengan el ingrediente de la búsqueda
            GET http://localhost:5000/f_restfull/api/recipes?con=vodka HTTP/1.1

        3)  Creará un registro nuevo a partir de los parámetros 
        que enviemos con el POST, y devolverá el id del registro creado, y sus datos
            POST http://localhost:5000/f_restfull/api/recipes HTTP/1.1
            Content-Type: application/json

            {
                "name":"Cubatillapara2",
                "ingredients":[{"name":"Coke","quantity":{"unit":"ml","amount":40}}],
                "instructions":["Shake the cup and shout."],
                "slug":"cubatillapara2"
            }

        4)  Devolver el resgistro correspondiente al id dado
            GET http://localhost:5000/f_restfull/api/recipes/5f7b4b6204799f5cf837b1e1 HTTP/1.1

        5)  Modificará el registro a partir de los parámetros enviados en el PUT y 
        devolverá el id del registro modificado y sus datos
            PUT http://localhost:5000/f_restfull/api/recipes/5f7b4b6204799f5cf837b1e1 HTTP/1.1
            Content-Type: application/json

            {
                "name":"Cubatillapara3",
                "ingredients":[{"name":"Coke","quantity":{"unit":"ml","amount":40}}],
                "instructions":["Shake the cup and shout very loud!!."],
                "slug":"cubatillapara3"
            }

        6)  Borrará el registro correspondiente y devolverá el id del registro borrado
            DELETE http://localhost:5000/f_restfull/api/recipes/5f7daa018ec9dfb536781afa HTTP/1.1   
