-- HACER MAKEMIGRATIONS Y MIGRATE_SCHEMAS
-- CORRER ESTE SQL ANTES DE COMENZAR A DESARROLLAR

-- CREAR UN SUPERUSUARIO POR MEDIO DE python3 manage.py createsuperuser
-- INSERTANDO UN CLIENTE (EL SUPER USER SERÁ UN CLIENTE) NECESARIO PARA CREAR EL PRIMER TENANT QUE ES EL PÚBLICO;
-- VERIFICAR EL ID DEL SUPERUSUARIO PARA LA COLUMNA USUARIO_ID

insert into inmobiliaria_tenant_cliente ("nombre", "apellidos", "cedula", "correo", "estado", "usuario_id")
values ('Supera dministrador', 'Inmobiliarias Tensoft', '1','admin@super.tf', True, 1);

-- INSERTANDO EL PRIMER TENANT (PÚBLICO)

insert into inmobiliaria_tenant_inmobiliaria ("schema_name", "nombre", "estado", "representante_id", "fecha_registro", "solicitud_baja")
values ('public', 'Superadmin', True, '1', now(), false);

-- INSERTANDO EL DOMINIO LOCALHOST (VERIFICAR EL ID DEL TENANT EN LA DB!!!!!)

insert into inmobiliaria_tenant_domain ("domain", "is_primary", "tenant_id", "estado")
values ('localhost', true, 1, true);
