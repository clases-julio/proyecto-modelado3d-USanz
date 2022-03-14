import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.data.objects[nombreObjeto].select_set(True) # ...excepto el buscado

def seleccionarObjetos(nombresObjetos):
    bpy.ops.object.select_all(action='DESELECT')
    for nombreObjeto in nombresObjetos:
        bpy.data.objects[nombreObjeto].select_set(True)

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
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=1, location=(0, 0, 0))
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

CHASSIS_WHEEL_SEPARATION = 0.2
CHASSIS_WIDTH = WHEEL_AXIS_LENGTH - 2*CHASSIS_WHEEL_SEPARATION
CHASSIS_LENGTH = AXIS_SEPARATION_DISTANCE
CHASSIS_HEIGHT = 1.0
CHASSIS_SIZE = (CHASSIS_WIDTH, CHASSIS_LENGTH, CHASSIS_HEIGHT) #its multiplied by 2 because default cube dimensions are (0.5, 0.5, 0.5) so we duplicate to get (1, 1, 1) and then resize

BONNET_WIDTH = CHASSIS_WIDTH - 0.1
BONNET_LENGTH = 0.8
BONNET_HEIGHT = CHASSIS_HEIGHT - 0.2
BONNET_SIZE = (BONNET_WIDTH, BONNET_LENGTH, BONNET_HEIGHT)

TRUNK_WIDTH = CHASSIS_WIDTH
TRUNK_LENGTH = 0.8
TRUNK_HEIGHT = CHASSIS_HEIGHT - 0.2
TRUNK_BORDER_WIDTH = 0.1
TRUNK_SIZE = (TRUNK_WIDTH, TRUNK_LENGTH, TRUNK_HEIGHT)

BODY_COLOR = (0.0, 0.7, 0.85, 1.0) #RGB

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
    
    Objeto.crearCubo('chasis_parte_central')
    Seleccionado.escalar(CHASSIS_SIZE)
    Seleccionado.mover((0, 0, CHASSIS_HEIGHT/2))
    
    Objeto.crearCubo('capó')
    Seleccionado.escalar(BONNET_SIZE)
    Seleccionado.mover((0, CHASSIS_LENGTH/2 + BONNET_LENGTH/2, BONNET_HEIGHT/2))
    
    Objeto.crearCubo('maletero_parte_izquierda')
    Seleccionado.escalar((TRUNK_BORDER_WIDTH, TRUNK_LENGTH, TRUNK_HEIGHT))
    Seleccionado.mover((-TRUNK_WIDTH/2 + TRUNK_BORDER_WIDTH/2, -CHASSIS_LENGTH/2 - TRUNK_LENGTH/2, BONNET_HEIGHT/2))

    Seleccionado.duplicar((TRUNK_WIDTH - TRUNK_BORDER_WIDTH, 0, 0), 'maletero_parte_derecha')

    Objeto.crearCubo('maletero_parte_inferior')
    Seleccionado.escalar((TRUNK_WIDTH - TRUNK_BORDER_WIDTH*2, TRUNK_LENGTH, TRUNK_BORDER_WIDTH))
    Seleccionado.mover((0, -CHASSIS_LENGTH/2 - TRUNK_LENGTH/2, TRUNK_BORDER_WIDTH/2))
    
    Seleccionado.duplicar((0, -TRUNK_LENGTH/2 + TRUNK_BORDER_WIDTH/2, TRUNK_LENGTH/2 - TRUNK_BORDER_WIDTH/2), 'maletero_parte_trasera')
    Seleccionado.rotarX(3.14/2)
    
    seleccionarObjetos(['maletero_parte_inferior', 'maletero_parte_derecha', 'maletero_parte_izquierda', 'maletero_parte_trasera'])
    Seleccionado.unir('maletero')
    
    seleccionarObjetos(['capó', 'chasis_parte_central', 'maletero'])
    Seleccionado.unir('cuerpo_robot')
    Seleccionado.añadirMaterial(BODY_COLOR, 'BODY')
    




    #lights and camera:
    bpy.ops.object.light_add(type='SUN', radius=1, location=(0.0, 0.0, 5.0))
    bpy.ops.object.light_add(type='POINT', location=(4.5, 1.5, 3.7))
    bpy.ops.object.camera_add(align='VIEW',\
                              location=(7.0, -7.0, 5.0),\
                              rotation=(1.06, 0.00771012, 0.765167))

