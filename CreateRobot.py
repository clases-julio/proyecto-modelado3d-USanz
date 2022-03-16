import bpy
from math import pi

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

def borrarMateriales():
    for m in bpy.data.materials:
        bpy.data.materials.remove(m)
def borrarLuces():
    for m in bpy.data.lights:
        bpy.data.lights.remove(m)
def borrarMallas():
    for m in bpy.data.meshes:
        bpy.data.meshes.remove(m)

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
CHASSIS_HEIGHT = 1.5
CHASSIS_SIZE = (CHASSIS_WIDTH, CHASSIS_LENGTH, CHASSIS_HEIGHT) #its multiplied by 2 because default cube dimensions are (0.5, 0.5, 0.5) so we duplicate to get (1, 1, 1) and then resize

BONNET_WIDTH = CHASSIS_WIDTH - 0.3
BONNET_LENGTH = 0.8
BONNET_HEIGHT = CHASSIS_HEIGHT / 2
BONNET_SIZE = (BONNET_WIDTH, BONNET_LENGTH, BONNET_HEIGHT)

TRUNK_WIDTH = CHASSIS_WIDTH
TRUNK_LENGTH = 0.8
TRUNK_HEIGHT = CHASSIS_HEIGHT / 3 * 2
TRUNK_BORDER_WIDTH = 0.1
TRUNK_SIZE = (TRUNK_WIDTH, TRUNK_LENGTH, TRUNK_HEIGHT)

BODY_COLOR = (0.0, 0.7, 0.85, 1.0) #RGB


AERIAL_BASE_RADIUS = 0.1
AERIAL_BASE_HEIGHT = 0.05
AERIAL_BASE_SIZE = (AERIAL_BASE_RADIUS, AERIAL_BASE_RADIUS, AERIAL_BASE_HEIGHT)
AERIAL_BASE_POS = (-CHASSIS_WIDTH/2 + AERIAL_BASE_RADIUS + 0.1, -CHASSIS_LENGTH/2 + AERIAL_BASE_RADIUS + 0.1, CHASSIS_HEIGHT + AERIAL_BASE_HEIGHT/2)

AERIAL_STICK_RADIUS = 0.05
AERIAL_STICK_HEIGHT = 1
AERIAL_STICK_SIZE = (AERIAL_STICK_RADIUS, AERIAL_STICK_RADIUS, AERIAL_STICK_HEIGHT)
AERIAL_TIP_RADIUS = 0.05
AERIAL_STICK_POS = (AERIAL_BASE_POS[0], AERIAL_BASE_POS[1], AERIAL_BASE_POS[2] + AERIAL_BASE_HEIGHT/2 + AERIAL_STICK_HEIGHT)
AERIAL_COLOR = (0.25, 0.05, 0.85, 1.0)


LASER_GLASS_RADIUS_X = 0.2
LASER_GLASS_RADIUS_Y = LASER_GLASS_RADIUS_X - 0.1
LASER_GLASS_HEIGHT = 0.1
LASER_GLASS_SIZE = (LASER_GLASS_RADIUS_X, LASER_GLASS_RADIUS_Y, LASER_GLASS_HEIGHT)
LASER_GLASS_SHIFT_Y = 0.05
LASER_GLASS_COLOR = (1.0, 0.9, 0.1, 0.4)

LASER_BASE_WIDTH = LASER_GLASS_RADIUS_X*2 + 0.1
LASER_BASE_LENGTH = 0.1
LASER_BASE_HEIGHT = 0.2
LASER_BASE_SIZE = (LASER_BASE_WIDTH, LASER_BASE_LENGTH, LASER_BASE_HEIGHT)
LASER_BASE_POS = (0, CHASSIS_LENGTH/2 + LASER_BASE_LENGTH/2, CHASSIS_HEIGHT - LASER_BASE_HEIGHT/2 - 0.1)

LASER_GLASS_POS = (LASER_BASE_POS[0], LASER_BASE_POS[1] + LASER_GLASS_SHIFT_Y, LASER_BASE_POS[2])


SENSOR_BASE_COLOR = (0.2, 0.2, 0.2, 1.0)


US_EMITTER_RECEIVER_RADIUS = 0.1
US_EMITTER_RECEIVER_HEIGHT = 0.05
US_EMITTER_RECEIVER_SIZE = (US_EMITTER_RECEIVER_HEIGHT, US_EMITTER_RECEIVER_RADIUS, US_EMITTER_RECEIVER_RADIUS)
US_COMPONENT_SEPARATION = 0.1
US_BASE_WIDTH = 0.1
US_BASE_LENGTH = 3*US_COMPONENT_SEPARATION + 4*US_EMITTER_RECEIVER_RADIUS
US_BASE_HEIGHT = 2*US_COMPONENT_SEPARATION + 2*US_EMITTER_RECEIVER_RADIUS
US_BASE_SIZE = (US_BASE_WIDTH, US_BASE_LENGTH, US_BASE_HEIGHT)
US_RIGHT_BASE_POS = (CHASSIS_WIDTH/2 + US_BASE_WIDTH/2, 0, CHASSIS_HEIGHT/2)
US_LEFT_BASE_POS = (-US_RIGHT_BASE_POS[0], US_RIGHT_BASE_POS[1], US_RIGHT_BASE_POS[2])
US_RIGHT_EMITTER_POS = (US_RIGHT_BASE_POS[0] + US_BASE_WIDTH/2 + US_EMITTER_RECEIVER_HEIGHT/2, US_RIGHT_BASE_POS[1] + US_COMPONENT_SEPARATION/2 + US_EMITTER_RECEIVER_RADIUS, US_RIGHT_BASE_POS[2])
US_RIGHT_RECEIVER_POS = (US_RIGHT_BASE_POS[0] + US_BASE_WIDTH/2 + US_EMITTER_RECEIVER_HEIGHT/2, US_RIGHT_BASE_POS[1] - US_COMPONENT_SEPARATION/2 - US_EMITTER_RECEIVER_RADIUS, US_RIGHT_BASE_POS[2])
US_LEFT_EMITTER_POS = (-US_RIGHT_EMITTER_POS[0], US_RIGHT_RECEIVER_POS[1], US_RIGHT_EMITTER_POS[2])
US_LEFT_RECEIVER_POS = (-US_RIGHT_RECEIVER_POS[0], US_RIGHT_EMITTER_POS[1], US_RIGHT_RECEIVER_POS[2])
US_EMITTER_COLOR = (0.0, 1.0, 0.0, 1.0)
US_RECEIVER_COLOR = (1.0, 0.0, 0.0, 1.0)
US_SENSOR_SIZE = (US_BASE_SIZE[0] + US_EMITTER_RECEIVER_SIZE[0], US_BASE_SIZE[1], US_BASE_SIZE[2])


CAMERA_BASE_WIDTH = 0.4
CAMERA_BASE_LENGTH = 0.4
CAMERA_BASE_HEIGHT = 0.1
CAMERA_BASE_SIZE = (CAMERA_BASE_WIDTH, CAMERA_BASE_LENGTH, CAMERA_BASE_HEIGHT)
CAMERA_BASE_POS = (0.0, CHASSIS_LENGTH/2 - CAMERA_BASE_LENGTH/2 - 0.1, CHASSIS_HEIGHT)
CAMERA_NECK_RADIUS = 0.1
CAMERA_NECK_HEIGHT = 0.2
CAMERA_NECK_SIZE = (CAMERA_NECK_RADIUS, CAMERA_NECK_RADIUS, CAMERA_NECK_HEIGHT)
CAMERA_NECK_POS = (CAMERA_BASE_POS[0], CAMERA_BASE_POS[1], CAMERA_BASE_POS[2] + CAMERA_NECK_HEIGHT/2 + CAMERA_BASE_HEIGHT/2)
CAMERA_BODY_WIDTH = 0.3
CAMERA_BODY_LENGTH = 0.6
CAMERA_BODY_HEIGHT = 0.3
CAMERA_BODY_SIZE = (CAMERA_BODY_WIDTH, CAMERA_BODY_LENGTH, CAMERA_BODY_HEIGHT)
CAMERA_BODY_Y_SHIFT = 0.1
CAMERA_BODY_POS = (CAMERA_NECK_POS[0], CAMERA_NECK_POS[1] + CAMERA_BODY_Y_SHIFT, CAMERA_NECK_POS[2] + CAMERA_NECK_HEIGHT/2 + CAMERA_BODY_HEIGHT/2)
CAMERA_LENS_WIDTH = 0.12
CAMERA_LENS_LENGTH = 0.05
CAMERA_LENS_HEIGHT = 0.12
CAMERA_LENS_SIZE = (CAMERA_LENS_WIDTH, CAMERA_LENS_LENGTH, CAMERA_LENS_HEIGHT)
CAMERA_LENS_POS = (CAMERA_BODY_POS[0], CAMERA_BODY_POS[1] + CAMERA_BODY_LENGTH/2, CAMERA_BODY_POS[2])
CAMERA_LENS_COLOR = (0.0, 0.3, 0.5, 0.6)


PI = pi #from math.pi

def create_axis(obj_pos, obj_name):
    #right outer part of the wheel:
    Objeto.crearCilindro('cilindro_exterior_derecho')
    Seleccionado.rotarY(PI/2.0)
    Seleccionado.escalar((WHEEL_OUTER_PART_WIDTH, WHEEL_OUTER_PART_RADIUS, WHEEL_OUTER_PART_RADIUS))
    Seleccionado.mover((WHEEL_OUTER_PART_WIDTH/2 + WHEEL_INNER_PART_WIDTH/2, 0, 0))
    
    #left outer part of the wheel:
    Seleccionado.duplicar((-WHEEL_OUTER_PART_WIDTH - WHEEL_INNER_PART_WIDTH, 0, 0), 'cilindro_exterior_izquierdo')
    
    #inner part of the wheel:
    Objeto.crearCilindro('cilindro_interior')
    Seleccionado.rotarY(PI/2.0)
    Seleccionado.escalar((WHEEL_INNER_PART_WIDTH, WHEEL_INNER_PART_RADIUS, WHEEL_INNER_PART_RADIUS))
    
    #joinning the different parts of the wheel:
    seleccionarObjetos(['cilindro_exterior_derecho', 'cilindro_exterior_izquierdo', 'cilindro_interior'])
    Seleccionado.unir('rueda_derecha')
    Seleccionado.añadirMaterial(WHEEL_COLOR, 'WHEEL')
    
    #duplicating and translating the wheels:
    Seleccionado.mover((WHEEL_AXIAL_DISTANCE/2, 0, 0))
    Seleccionado.duplicar((-WHEEL_AXIAL_DISTANCE, 0, 0), 'rueda_izquierda')
    
    #creating the axis:
    Objeto.crearCilindro('eje')
    Seleccionado.rotarY(PI/2.0)
    Seleccionado.escalar((WHEEL_AXIS_LENGTH, WHEEL_AXIS_RADIUS, WHEEL_AXIS_RADIUS))
    Seleccionado.añadirMaterial(WHEEL_AXIS_COLOR, 'AXIS')
    
    #joinning the axis with the wheels: 
    seleccionarObjetos(['rueda_derecha', 'rueda_izquierda', 'eje'])
    Seleccionado.unir(obj_name)
    Seleccionado.mover(obj_pos)

def create_body(obj_pos, obj_name):
    #creating the central part of the chsassis:
    Objeto.crearCubo('chasis_parte_central')
    Seleccionado.escalar(CHASSIS_SIZE)
    Seleccionado.mover((0, 0, CHASSIS_HEIGHT/2))
    
    #creating the bannet:
    Objeto.crearCubo('capo')
    Seleccionado.escalar(BONNET_SIZE)
    Seleccionado.mover((0, CHASSIS_LENGTH/2 + BONNET_LENGTH/2, BONNET_HEIGHT/2))
    
    #creating the parts of the trunk:
    Objeto.crearCubo('maletero_parte_izquierda')
    Seleccionado.escalar((TRUNK_BORDER_WIDTH, TRUNK_LENGTH, TRUNK_HEIGHT))
    Seleccionado.mover((-TRUNK_WIDTH/2 + TRUNK_BORDER_WIDTH/2, -CHASSIS_LENGTH/2 - TRUNK_LENGTH/2, TRUNK_HEIGHT/2))

    Seleccionado.duplicar((TRUNK_WIDTH - TRUNK_BORDER_WIDTH, 0, 0), 'maletero_parte_derecha')

    Objeto.crearCubo('maletero_parte_inferior')
    Seleccionado.escalar((TRUNK_WIDTH - TRUNK_BORDER_WIDTH*2, TRUNK_LENGTH, TRUNK_BORDER_WIDTH))
    Seleccionado.mover((0, -CHASSIS_LENGTH/2 - TRUNK_LENGTH/2, TRUNK_BORDER_WIDTH/2))
    
    Objeto.crearCubo('maletero_parte_posterior')
    Seleccionado.escalar((TRUNK_WIDTH - TRUNK_BORDER_WIDTH*2, TRUNK_BORDER_WIDTH, TRUNK_HEIGHT))
    Seleccionado.mover((0, -CHASSIS_LENGTH/2 - TRUNK_LENGTH + TRUNK_BORDER_WIDTH/2, TRUNK_HEIGHT/2))

    #joinning the parts of the trunk together:
    seleccionarObjetos(['maletero_parte_inferior', 'maletero_parte_derecha', 'maletero_parte_izquierda', 'maletero_parte_posterior'])
    Seleccionado.unir('maletero')
    
    #joinning the chassis, the bannet and the trunk as the robot body:
    seleccionarObjetos(['capo', 'chasis_parte_central', 'maletero'])
    Seleccionado.unir(obj_name)
    Seleccionado.añadirMaterial(BODY_COLOR, 'BODY')
    Seleccionado.mover(obj_pos)

def create_aerial(obj_pos, obj_name):
    #making the aerial:
    Objeto.crearCilindro('base_antena')
    Seleccionado.rotarZ(PI/2.0)
    Seleccionado.escalar(AERIAL_BASE_SIZE)
    Seleccionado.mover((0, 0, AERIAL_BASE_HEIGHT/2))
    
    Objeto.crearCono('vara_antena')
    Seleccionado.escalar((AERIAL_STICK_RADIUS, AERIAL_STICK_RADIUS, AERIAL_STICK_HEIGHT/2))
    Seleccionado.mover((0, 0, AERIAL_BASE_HEIGHT + AERIAL_STICK_HEIGHT/2)) #for some reason the cone creates itself with the double of the height specified, so it has to be divided by 2.
    
    Objeto.crearEsfera('bola_antena')
    Seleccionado.escalar((AERIAL_TIP_RADIUS, AERIAL_TIP_RADIUS, AERIAL_TIP_RADIUS))
    Seleccionado.mover((0, 0, AERIAL_BASE_HEIGHT + AERIAL_STICK_HEIGHT))
    
    #joinning the parts of the aerial together:    
    seleccionarObjetos(['base_antena', 'vara_antena', 'bola_antena'])
    Seleccionado.unir(obj_name)
    Seleccionado.añadirMaterial(AERIAL_COLOR, 'AERIAL')
    Seleccionado.mover(obj_pos)
    
    
def create_laser(obj_pos, obj_name):
    Objeto.crearCubo('base_laser')
    Seleccionado.escalar(LASER_BASE_SIZE)
    Seleccionado.añadirMaterial(SENSOR_BASE_COLOR, 'LASER_BASE')
    
    Objeto.crearCilindro('cristal_laser')
    Seleccionado.rotarZ(PI/2.0)
    Seleccionado.escalar(LASER_GLASS_SIZE)
    Seleccionado.mover((0, LASER_GLASS_SHIFT_Y, 0))
    Seleccionado.añadirMaterial(LASER_GLASS_COLOR, 'LASER_GLASS')
    
    seleccionarObjetos(['base_laser', 'cristal_laser'])
    Seleccionado.unir(obj_name)
    Seleccionado.mover(obj_pos)

def create_us_sensor(obj_pos, obj_name):
    Objeto.crearCubo('base_sensor')
    Seleccionado.escalar(US_BASE_SIZE)
    Seleccionado.añadirMaterial(SENSOR_BASE_COLOR, 'US_BASE')
    
    Objeto.crearCilindro('emisor')
    Seleccionado.rotarY(PI/2.0)
    Seleccionado.escalar(US_EMITTER_RECEIVER_SIZE)
    Seleccionado.mover((US_BASE_WIDTH/2 + US_EMITTER_RECEIVER_HEIGHT/2, US_EMITTER_RECEIVER_RADIUS + US_COMPONENT_SEPARATION/2, 0))
    Seleccionado.añadirMaterial(US_EMITTER_COLOR, 'US_EMITTER')
    
    Objeto.crearCilindro('receptor')
    Seleccionado.rotarY(PI/2.0)
    Seleccionado.escalar(US_EMITTER_RECEIVER_SIZE)
    Seleccionado.mover((US_BASE_WIDTH/2 + US_EMITTER_RECEIVER_HEIGHT/2, -US_EMITTER_RECEIVER_RADIUS - US_COMPONENT_SEPARATION/2, 0))
    Seleccionado.añadirMaterial(US_RECEIVER_COLOR, 'US_RECEIVER')
    
    seleccionarObjetos(['base_sensor', 'emisor', 'receptor'])
    Seleccionado.unir(obj_name)
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME', center='MEDIAN')
    Seleccionado.mover(obj_pos)

def create_camera(obj_pos, obj_name):
    Objeto.crearCubo('base_camara')
    Seleccionado.escalar(CAMERA_BASE_SIZE)
    Seleccionado.mover((0, 0, CAMERA_NECK_HEIGHT/2))
    
    Objeto.crearCilindro('cuello_camara')
    Seleccionado.escalar(CAMERA_NECK_SIZE)
    Seleccionado.mover((0, 0, CAMERA_NECK_HEIGHT + CAMERA_BASE_HEIGHT/2))
    
    Objeto.crearCubo('cuerpo_camara')
    Seleccionado.escalar(CAMERA_BODY_SIZE)
    Seleccionado.mover((0, CAMERA_BODY_Y_SHIFT, CAMERA_NECK_HEIGHT + CAMERA_BASE_HEIGHT + CAMERA_BODY_HEIGHT/2))
    
    seleccionarObjetos(['base_camara', 'cuello_camara', 'cuerpo_camara'])
    Seleccionado.unir('camara_sin_lente')
    Seleccionado.añadirMaterial(SENSOR_BASE_COLOR, 'CAMERA_WITHOUT_LENS')
    
    Objeto.crearEsfera('lente_camara')
    Seleccionado.escalar(CAMERA_LENS_SIZE)
    Seleccionado.mover((0, CAMERA_BODY_Y_SHIFT + CAMERA_BODY_LENGTH/2, CAMERA_NECK_HEIGHT + CAMERA_BASE_HEIGHT + CAMERA_BODY_HEIGHT/2))
    Seleccionado.añadirMaterial(CAMERA_LENS_COLOR, 'CAMERA_LENS')
    
    seleccionarObjetos(['lente_camara', 'camara_sin_lente'])
    Seleccionado.unir(obj_name)
    Seleccionado.mover(obj_pos)
    
if __name__ == "__main__":
    #Deleting all the objects to reset the scene:
    borrarObjetos()
    borrarMateriales()
    borrarLuces()
    borrarMallas()
    
    #Creating the axes:
    create_axis((0, -AXIS_SEPARATION_DISTANCE/2, 0), 'eje_y_ruedas_posteriores')
    create_axis((0, AXIS_SEPARATION_DISTANCE/2, 0), 'eje_y_ruedas_anteriores')
    
    #Creating the body of the robot:
    create_body((0, 0, 0), 'cuerpo_robot')
    
    #Creating the sensors and details:
    create_aerial((-CHASSIS_WIDTH/2 + AERIAL_BASE_RADIUS + 0.1, -CHASSIS_LENGTH/2 + AERIAL_BASE_RADIUS + 0.1, CHASSIS_HEIGHT), 'antena')
    
    create_laser((0, CHASSIS_LENGTH/2 + LASER_BASE_LENGTH/2, CHASSIS_HEIGHT - LASER_BASE_HEIGHT/2 - 0.1), 'laser')
    
    create_us_sensor((CHASSIS_WIDTH/2 + US_EMITTER_RECEIVER_HEIGHT/2 + US_BASE_WIDTH/2, 0, CHASSIS_HEIGHT/2), 'us_derecha')
    
    create_us_sensor((-CHASSIS_WIDTH/2 - US_EMITTER_RECEIVER_HEIGHT/2 - US_BASE_WIDTH/2, 0, CHASSIS_HEIGHT/2), 'us_izquierda')
    Seleccionado.escalar((-1, -1, 1))
    
    create_camera((0, CHASSIS_LENGTH/2 - CAMERA_BASE_LENGTH/2 - 0.1, CHASSIS_HEIGHT - CAMERA_BASE_HEIGHT/2), 'camara_robot')
    



    #lights and camera:
    bpy.ops.object.light_add(type='SUN', radius=1, location=(0.0, 0.0, 5.0))
    bpy.ops.object.light_add(type='POINT', location=(4.5, 1.5, 3.7))
    bpy.ops.object.camera_add(align='VIEW',\
                              location=(10.0, -10.0, 8.5),\
                              rotation=(1.06, 0.00771012, 0.765167))

