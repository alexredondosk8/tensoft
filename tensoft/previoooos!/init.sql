-- SE DEBE CREAR UNA BASE DE DATOS Y UN USUARIO CON LOS SIGUIENTES DATOS
/*
 DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': 'inmobiliarias_tensoft',
        'USER': 'univalle',
        'PASSWORD': 'univalle',
        'HOST': 'localhost',
        'PORT': '5433',
    }
}
*/

-- NOTA: EL USUARIO CREADO DEBE TENER TODOS LOS PERMISOS PARA OPERAR LA BASE DE DATOS SATISFACTORIAMENTE


-- HACER MAKEMIGRATIONS Y MIGRATE_SCHEMAS
-- CORRER ESTE SQL ANTES DE COMENZAR A DESARROLLAR

-- CREAR UN SUPERUSUARIO POR MEDIO DE python3 manage.py createsuperuser
-- EL USUARIO Y CONTRASEÑA NO IMPORTAN. SON PARÁMETROS LOCALES

-- INSERTANDO UN CLIENTE (EL SUPER USER SERÁ UN CLIENTE) NECESARIO PARA CREAR EL PRIMER TENANT QUE ES EL PÚBLICO;
-- VERIFICAR EL ID DEL SUPERUSUARIO PARA LA COLUMNA USUARIO_ID

insert into inmobiliaria_tenant_cliente ("nombre", "apellidos", "cedula", "correo", "estado", "usuario_id")
values ('Super administrador', 'Inmobiliarias Tensoft', '1','admin@super.tf', True, 1);

-- INSERTANDO EL PRIMER TENANT (PÚBLICO)

insert into inmobiliaria_tenant_inmobiliaria ("schema_name", "nombre", "estado", "representante_id", "fecha_registro", "solicitud_baja")
values ('public', 'Superadmin', True, '1', now(), false);

-- INSERTANDO EL DOMINIO LOCALHOST (VERIFICAR EL ID DEL TENANT EN LA DB!!!!!)

insert into inmobiliaria_tenant_domain ("domain", "is_primary", "tenant_id", "estado")
values ('localhost', true, 1, true);

-- !!!! NUEVOOOO !!!!
-- INICIAR EL SERVIDOR python3 manage.py runserver
-- ingresar a la URL localhost:8000/admin e iniciar sesión con el superusuario
-- CREAR UN GRUPO "superadministrador" (SIN COMILLAS) Y ASOCIARLO AL SUPERADMINISTRADOR CREADO
-- !!!! FIN DE NUEVO !!!!
