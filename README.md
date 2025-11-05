1.- Ingresar al Instagram y aceptar ¿Guardar tu información de inicio de sesión?
2.- Mantener el Instagram abierto
3.- Ingresar al proyecto Instagram service.
4.- Delete session.json
5.- correr python3 session.py(cuando finaliza ya se puede cerrar    
    Instagram).
    👤 Usuario de Instagram:
    🔑 Contraseña: 
    🔐 Intentando iniciar sesión...
6.- Se genera el archivo session.json
    copiar el session.json que se genera y guardarlo en la variable
    de entorno SESSION_JSON en https://dashboard.render.com
7.- Deploy y esperar ( tarda varios minutos generalmente).
8.- copiar y pegar el session.json en el nodo de N8N llamado 
    session.
9.- colocar en los nodos HTTPS de Followers y Following el 
    👤 Usuario de Instagram (solamente usuario)
10.- Correr el workflow N8N Instagram followers-following
     se guardaran los followers y following en sus respectivas sheet
     del Google Sheet.
     
    https://docs.google.com/spreadsheets/d/1c5rjZOuP8uqDoq_plD85yb3wOYiXJMVajqdmKEZ0B2M/edit?pli=1&gid=1621531578#gid=1621531578

