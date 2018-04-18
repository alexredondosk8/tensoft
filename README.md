# tensoft

Repositorio para el desarrollo de Tensoft para administración de inmobiliarias como servicio. Ver indicaciones previas en la carpeta previooos! Allí hay indicaciones de SQL que se deben hacer antes de desarrollar en la aplicación.

## Requeriments:
* Django==1.11
* django-bootstrap3==9.1.0
* django-recaptcha==1.4.0
* django-tenant-schemas==1.9.0
* django-tenants==1.3.3
* psycopg2==2.7.4
* pytz==2018.3

## Indicaciones previas

1. **Se debe crear una base de datos y un usuario con los siguientes datos:**

    *NAME*: 'inmobiliarias_tensoft'

    *USER*: 'univalle'

    *PASSWORD*: 'univalle'

    *HOST*: 'localhost'

    *PORT*: '5433'

    *NOTA*: *El usuario creado debe tener todos los permisos para operar la base de datos satisfactoriamente*

2. **Correr:**

    `python3 manage.py makemigrations` 

    `python3 manage.py makemigrations inmobiliaria_tenant`

    `python3 manage.py migrate_schemas` 


3. **correr el sql antes de comenzar a desarrollar**
    
    ```sql
    insert into inmobiliaria_tenant_cliente ("nombre", "apellidos", "cedula", "correo", "estado", "usuario_id")
    values ('Supera dministrador', 'Inmobiliarias Tensoft', '1','admin@super.tf', True, 1);
    ```

    *insertando el primer tenant (público)*

    ```sql
     insert into inmobiliaria_tenant_inmobiliaria ("schema_name", "nombre", "estado", "representante_id", "fecha_registro",        "solicitud_baja")

     values ('public', 'Superadmin', True, '1', now(), false);
     ```

    *insertando el dominio localhost (**verificar el id del tenant en la db!**)*

    ```sql
    insert into inmobiliaria_tenant_domain ("domain", "is_primary", "tenant_id", "estado")
    values ('localhost', true, 1, true);
    ```

4. **crear un superusuario**

    `python3 manage.py createsuperuser`

      - *el usuario y contraseña no importan. son parámetros locales*

      - *insertando un cliente (el super user será un cliente) necesario para crear el primer tenant que es el público*;

      - *verificar el id del superusuario para la columna usuario_id*
