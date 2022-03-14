import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select_set(True) # ...excepto el buscado

def seleccionarTodos():
    bpy.ops.object.select_all(action='SELECT')

def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.context.scene.objects.active = bpy.data.objects[nombreObjeto]

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')
    
    def duplicar(v, nombreObjeto):
        bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'},\
                                      TRANSFORM_OT_translate={"value":v})
        bpy.context.object.name = nombreObjeto
    
    def unir(nombreObjeto): #une todos los objetos seleccionados.
        bpy.ops.object.join()
        bpy.context.object.name = nombreObjeto

    def añadirMaterial(color, nombreMaterial):
        mat = bpy.data.materials.new(nombreMaterial)
        mat.diffuse_color = color
        bpy.context.selected_objects[0].active_material = mat

'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
        
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(radius=1, depth=1, location=(0, 0, 0))
        Activo.renombrar(objName)

        

'''************'''
''' M  A  I  N '''
'''************'''

'''
WARNING: YOU SHOULD ONLY CHANGE THE FLOAT VALUES (x.x), DO NOT CHANGE OR DELETE ANY VARIABLE NAME OR INT NUMBER.
'''

WHEEL_OUTER_PART_RADIUS = 0.75
WHEEL_OUTER_PART_WIDTH = 0.15
WHEEL_INNER_PART_RADIUS = 0.45
WHEEL_INNER_PART_WIDTH = 0.35

WHEEL_RADIUS = WHEEL_OUTER_PART_RADIUS
WHEEL_WIDTH = WHEEL_OUTER_PART_WIDTH*2 + WHEEL_INNER_PART_WIDTH
WHEEL_COLOR = (0.7, 1.0, 0.1, 1.0)

WHEEL_AXIAL_DISTANCE = 3.5 #distance between the 2 wheel centers of the same axis.
WHEEL_AXIS_LENGTH = WHEEL_AXIAL_DISTANCE - WHEEL_WIDTH #distace of the physical axis (substracting the WHEEL_WIDTH).
WHEEL_AXIS_RADIUS = 0.1
WHEEL_AXIS_COLOR = (0.1, 0.1, 0.4, 1.0) #RGB

AXIS_SEPARATION_DISTANCE = 4.0 #distance from one axis to another.

CHASIS_WIDTH = WHEEL_AXIS_LENGTH
CHASIS_LENGTH = WHEEL_AXIAL_DISTANCE + 1
CHASIS_HEIGHT = 2
CHASIS_SIZE = (CHASIS_WIDTH, CHASIS_LENGTH, CHASIS_HEIGHT)

if __name__ == "__main__":
    #resetear escenario:
    borrarObjetos()
    
    #right outer part of the wheel:
    Objeto.crearCilindro('cilindro_exterior_derecho')
    Seleccionado.rotarY(3.14/2)
    Seleccionado.escalar((WHEEL_OUTER_PART_WIDTH, WHEEL_OUTER_PART_RADIUS, WHEEL_OUTER_PART_RADIUS))
    Seleccionado.mover((WHEEL_OUTER_PART_WIDTH/2 + WHEEL_INNER_PART_WIDTH/2, 0, 0))
    
    #left outer part of the wheel:
    Seleccionado.duplicar((-WHEEL_OUTER_PART_WIDTH - WHEEL_INNER_PART_WIDTH, 0, 0), 'cilindro_exterior_izquierdo')
    
    #inner part of the wheel:
    Objeto.crearCilindro('cilindro_interior')
    Seleccionado.rotarY(3.14/2)
    Seleccionado.escalar((WHEEL_INNER_PART_WIDTH, WHEEL_INNER_PART_RADIUS, WHEEL_INNER_PART_RADIUS))
    
    #joinning the different parts of the wheel:
    seleccionarTodos()
    Seleccionado.unir('rueda_posterior_derecha')
    Seleccionado.añadirMaterial(WHEEL_COLOR, 'WHEEL')
    
    #duplicating and translating the wheels:
    Seleccionado.mover((WHEEL_AXIAL_DISTANCE/2, 0, 0))
    Seleccionado.duplicar((-WHEEL_AXIAL_DISTANCE, 0, 0), 'rueda_posterior_izquierda')
    
    #creating the axis and joinning it with the 2 wheels:
    Objeto.crearCilindro('eje_posterior')
    Seleccionado.rotarY(3.14/2)
    Seleccionado.escalar((WHEEL_AXIS_LENGTH, WHEEL_AXIS_RADIUS, WHEEL_AXIS_RADIUS))
    Seleccionado.añadirMaterial(WHEEL_AXIS_COLOR, 'AXIS')
    
    seleccionarTodos()
    Seleccionado.unir('eje_y_ruedas_posteriores')
    
    Seleccionado.mover((0, -AXIS_SEPARATION_DISTANCE/2, 0))
    Seleccionado.duplicar((0, AXIS_SEPARATION_DISTANCE, 0), 'eje_y_ruedas_anteriores')
    
    Objeto.crearCubo('carroceria')
    #Seleccionado.escalar(CHASIS_SIZE)


    #lights and camera:
    bpy.ops.object.light_add(type='SUN', radius=1, location=(0.0, 0.0, 5.0))
    bpy.ops.object.light_add(type='POINT', location=(4.5, 1.5, 3.7))
    bpy.ops.object.camera_add(align='VIEW',\
                              location=(7.0, -7.0, 5.0),\
                              rotation=(1.06, 0.00771012, 0.765167))

