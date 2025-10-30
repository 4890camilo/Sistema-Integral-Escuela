
from django.db import migrations

# --- 1. Definición del Pensum (currículum) ---
CURRICULUM = {
    'Primero': [
        'Matemáticas', 'Lengua Castellana', 'Ciencias Naturales', 'Ciencias Sociales',
        'Educación Artística', 'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Segundo': [
        'Matemáticas', 'Lengua Castellana', 'Ciencias Naturales', 'Ciencias Sociales',
        'Educación Artística', 'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Tercero': [
        'Matemáticas', 'Lengua Castellana', 'Ciencias Naturales', 'Ciencias Sociales',
        'Educación Artística', 'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Cuarto': [
        'Matemáticas', 'Lengua Castellana', 'Ciencias Naturales', 'Ciencias Sociales',
        'Educación Artística', 'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión',
        'Inglés' # Se introduce
    ],
    'Quinto': [
        'Matemáticas', 'Lengua Castellana', 'Ciencias Naturales', 'Ciencias Sociales',
        'Educación Artística', 'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión',
        'Inglés'
    ],
    'Sexto': [
        'Matemáticas', 'Lengua Castellana', 'Ciencias Naturales (Biología, Física y Química básica)',
        'Ciencias Sociales (Historia y Geografía)', 'Inglés', 'Educación Artística', 'Educación Física',
        'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Séptimo': [
        'Matemáticas', 'Lengua Castellana', 'Biología', 'Física', 'Química',
        'Ciencias Sociales', 'Inglés', 'Educación Artística', 'Educación Física',
        'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Octavo': [
        'Matemáticas', 'Lengua Castellana', 'Biología', 'Física', 'Química',
        'Ciencias Sociales', 'Inglés', 'Educación Artística', 'Educación Física',
        'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Noveno': [
        'Matemáticas', 'Lengua Castellana', 'Biología', 'Física', 'Química',
        'Ciencias Sociales (Historia, Geografía, Constitución Política)', 'Inglés', 'Educación Artística', 'Educación Física',
        'Ética y Valores', 'Tecnología e Informática', 'Religión'
    ],
    'Décimo': [
        'Matemáticas', 'Lengua Castellana', 'Física', 'Química', 'Biología',
        'Filosofía', 'Ciencias Sociales (Historia, Economía, Política)', 'Inglés',
        'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión',
        'Proyecto de Vida / Orientación Vocacional'
    ],
    'Once': [
        'Matemáticas', 'Lengua Castellana', 'Física', 'Química', 'Biología',
        'Filosofía', 'Ciencias Sociales (Cátedra de la Paz, Política y Economía)', 'Inglés',
        'Educación Física', 'Ética y Valores', 'Tecnología e Informática', 'Religión',
        'Proyecto de Grado o de Investigación'
    ]
}

def poblar_estructura(apps, schema_editor):
    Grado = apps.get_model('academico', 'Grado')
    Curso = apps.get_model('academico', 'Curso')
    Materia = apps.get_model('academico', 'Materia')

    cursos_a_crear = []
    materias_a_crear = []

    for nombre_grado in CURRICULUM.keys():
        # 1. Creamos el Grado (Ej: "Primero")
        grado_obj = Grado.objects.create(nombre=nombre_grado)
        
        # 2. Creamos los Cursos (salones) para ese grado (Ej: "Primero A", "Primero B")
        for seccion in ['A', 'B']:
            cursos_a_crear.append(
                Curso(nombre=f"{nombre_grado} {seccion}", grado=grado_obj)
            )
        
        # 3. Creamos las Materias para ese grado (Ej: "Matemáticas (Primero)")
        for nombre_materia in CURRICULUM[nombre_grado]:
            materias_a_crear.append(
                Materia(nombre=nombre_materia, grado=grado_obj)
            )
            
    # Creamos todo en la base de datos
    Curso.objects.bulk_create(cursos_a_crear)
    Materia.objects.bulk_create(materias_a_crear)

class Migration(migrations.Migration):

    dependencies = [
        # Depende de la migración que crea las tablas
        ('academico', '0002_initial'),
    ]

    operations = [
        # Ejecuta la función de arriba (corregido para el IrreversibleError)
        migrations.RunPython(
            poblar_estructura, 
            reverse_code=migrations.RunPython.noop
        ),
    ]