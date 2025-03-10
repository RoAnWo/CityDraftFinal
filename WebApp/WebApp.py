# Import javascript modules
from js import THREE, window, document, Object, console, Math
import js
# Import pyscript / pyodide modules
from pyodide.ffi import create_proxy, to_js #type:ignore
from shapely.geometry.polygon import LinearRing
#Import python module
import math
#import shapely

# Import NumPy as np
import numpy as np
from random import choices,choice, randint
import random
from time import time
from shapely import geometry
from collections import OrderedDict

import json


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# USE THIS FUNCTION TO WRITE THE MAIN PROGRAM
def main():
    # VISUAL SETUP
    # Declare the variables

    global renderer, scene, camera, controls,composer, light2, light

    #Set up the renderer

    renderer = THREE.WebGLRenderer.new()
    renderer.setPixelRatio( window.devicePixelRatio )
    renderer.setSize(window.innerWidth, window.innerHeight)
    document.body.appendChild(renderer.domElement)

 # Set up the scene

    scene = THREE.Scene.new()
    back_color = THREE.Color.new(200,200,200)
    scene.background = back_color
    camera = THREE.PerspectiveCamera.new(30, window.innerWidth/window.innerHeight,0.1, 10000)
    camera.position.y = -1000
    camera.position.x = 100
    camera.position.z = 200
    camera.up = THREE.Vector3.new( 0, 0, 1 )
    scene.add(camera)

    light2 = THREE.AmbientLight.new()
    light = THREE.PointLight.new(THREE.Color.new(255,255,233), 0.001,10000,20)
    light.position.set(-50, -50, 200)
    
    light.castShadow = True
    light.shadow.mapSize.width = 512
    light.shadow.mapSize.height = 512
    light.shadow.camera.near = 5
    light.shadow.camera.far = 500
    renderer.shadowMap.enabled = True
    renderer.shadowMap.type = THREE.PCFSoftShadowMap
    
    scene.add(light, light2)
    # axesHelper
    # axesHelper = THREE.AxesHelper.new(100)
    # scene.add(axesHelper)
    
    # Graphic Post Processing
    global composer
    post_process()

    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    global objects, control_points, transform_control, spheres, Boundary_status, Mouse1Bool, controls,Close_Bool, preview_Sphere, spheres_road,all_spheres,all_curve_object_road,Saved,Hover_over_Save,object_clicked, output_lists,clicked_sphere, geometrie, Input_Road_Coords_py,Boundary_Coords_py, curve_material
    global sphere_geom, sphere_material,preview_Sphere,prev_sphere_geom, Reset_Mesh, Save_Mesh, raycaster, mouse, plane_Raycaster, plane_map,texture_Plane_Mesh_Mat,OUTPUT_Mainstreet
    OUTPUT_Mainstreet =[]
    Input_Road_Coords_py=[]
    Boundary_Coords_py=[]
    input_param_map =  True
    clicked_sphere = None
    object_clicked=False
    Hover_over_Save = False
    Saved = False
    Close_Bool = False
    Mouse1Bool = False
    Boundary_status = "open"
    all_spheres = []
    spheres = []
    spheres_road = []
    objects = []
    control_points = []
    all_curve_object_road =[]

    sphere_geom = THREE.SphereGeometry.new( 3, 20, 20 )
    sphere_material = THREE.MeshPhongMaterial.new()
    sphere_material.color = THREE.Color.new( "rgb(255,0,0)" )


    prev_sphere_geom = THREE.SphereGeometry.new( 6, 20, 20 )
    prev_sphere_material = THREE.MeshPhongMaterial.new()
    prev_sphere_material.color = THREE.Color.new( "rgb(255,0,0)" )
    prev_sphere_material.transparent = True
    prev_sphere_material.opacity = 0.5
    preview_Sphere = THREE.Mesh.new( prev_sphere_geom, prev_sphere_material )
    preview_Sphere.visible= False
    scene.add( preview_Sphere )

    Reset_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Reset = THREE.TextureLoader.new().load("./maps\ResetBoundary.png")
    Reset_Mesh_Mat.map = texture_Reset

    Save_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Save = THREE.TextureLoader.new().load("./maps\SaveBoundary.png")
    Save_Mesh_Mat.map = texture_Save

    Button_Geo = THREE.BoxGeometry.new( 78, 34, 1 )

    Reset_Mesh = THREE.Mesh.new( Button_Geo, Reset_Mesh_Mat )
    Reset_Mesh.translateX(289)
    Reset_Mesh.translateY(236)
    Reset_Mesh.translateZ(-3)
    scene.add( Reset_Mesh )
    
    Save_Mesh = THREE.Mesh.new( Button_Geo, Save_Mesh_Mat )
    Save_Mesh.translateX(289)
    Save_Mesh.translateY(202)
    Save_Mesh.translateZ(-3)
    scene.add( Save_Mesh )
    
    raycaster = THREE.Raycaster.new()

    mouse = THREE.Vector2.new()

    geometrie = THREE.PlaneGeometry.new( 500, 500 )
    geometrie.rotateX( - Math.PI / 2 )

     
    plane_Raycaster = THREE.Mesh.new( geometrie, THREE.MeshPhongMaterial.new())
    geometrie.rotateX(math.radians(90))
    plane_Raycaster.visible = False
    plane_Raycaster.material.transparent=True
    plane_Raycaster.material.opacity = 0.5
    scene.add( plane_Raycaster )
    objects.append(plane_Raycaster)

    color_plane_map = THREE.Color.new ("rgb(200, 200, 200)")
    Plane_Mesh_Mat = THREE.MeshPhongMaterial.new( )
    Plane_Mesh_Mat.color = color_plane_map
    #texture_Plane_Mesh_Mat = THREE.TextureLoader.new().load("./maps\Berlin.png")
    #Plane_Mesh_Mat.map = texture_Plane_Mesh_Mat
    plane_map = THREE.Mesh.new( geometrie,Plane_Mesh_Mat)
    
    plane_map.translateZ(-3)
    scene.add( plane_map )

    curve_material = THREE.LineBasicMaterial.new()
    curve_material.color = THREE.Color.new("rgb(255,0,0)")
    # Set up responsive window

    # Set up responsive window

    transform_control = THREE.TransformControls.new(camera, renderer.domElement)
    transform_drag_proxy = create_proxy(transform_drag)
    transform_control.addEventListener('dragging-changed', transform_drag_proxy)
    
    
    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    
    resize_proxy = create_proxy(on_window_resize)
    window.addEventListener('resize', resize_proxy)

    mouse_move_proxy = create_proxy(on_mouse_move)
    document.addEventListener('mousemove', mouse_move_proxy)

    mouse_down_proxy = create_proxy(on_mouse_down)
    document.addEventListener('mousedown', mouse_down_proxy)

    mouse_up_proxy = create_proxy(on_mouse_up)
    document.addEventListener('mouseup', mouse_up_proxy)

    dbl_click_proxy = create_proxy(on_dbl_click)
    document.addEventListener('dblclick', dbl_click_proxy)

    controls = THREE.OrbitControls.new(camera, renderer.domElement)
    global input_param   

    input_param = {  
                   
    "Map1" : Map1,
    "Map2" : Map2,
    "Map3" : Map3,
    "removeMap" : NoMap,
           
    "MainStreets" : False, 
    "SecondaryStreets":False,
    "AssignUsage" :False,
    "GenerateCity" : False,
    "Generate" : Generate,
    "Regenerate" : regenerateAll,
    
    "population" : 1,
    "iputOld" : 1,
    "density" : 1,
    "populationold_density" : 1,
    
    #Industrial storagespace
    "height"   : 5,
    "oldheight" : 5,
    "distancestreetI" : 5, 
    "OlddistancestreetI" : 5,
    
    #0ffice
    "heightperfloorO"   :4,
    "oldheightperfloorO" : 4,
    "distancetostreetO"   : 3,
    "olddistancetostreetO" : 3,
    
    "LivingIndustrial" : 55,
    "workplaces": 1, 
    "workingpeopleold": 1,
    "floors" : 1, 
    "offsetR": 4, 
    "offsetB" : 3, 
    "offsetH" : 2, 
    "heightperfloorR": 4, 
    "heightperfloorB": 3.5, 
    "heightperfloorH": 4, 
    
    }
    input_param = Object.fromEntries(to_js(input_param))
    #-----------------------------------------------------------------------
     #GUI
    global gui, workingpeople
    gui = window.lil.GUI.new()
    
    map_folder = gui.addFolder('choose map')
    map_folder.add(input_param, 'Map1')
    map_folder.add(input_param, 'Map2')
    map_folder.add(input_param, 'Map3')
    map_folder.add(input_param, 'removeMap')
    
    map_folder.close()
    gen_folder = gui.addFolder('generate streetnetwork')
    gen_folder.add(input_param, 'MainStreets')
    gen_folder.add(input_param, 'SecondaryStreets')
    gen_folder.add(input_param, 'AssignUsage')
    gen_folder.add(input_param, 'LivingIndustrial', 10,100,1)
    
    gen_folder.add(input_param, 'GenerateCity')
    
    gen_folder.add(input_param, 'Generate')
    gen_folder.add(input_param, 'Regenerate')
    
    gen_folder.open()
    
    param_folder = gui.addFolder('demographic settings')
    param_folder.add(input_param, 'population', 0,1,0.1)
    param_folder.add(input_param, 'density', 0,5,0.1)

    
    I_folder = gui.addFolder('industrial storage')
    I_folder.add(input_param, 'height', 0,15,1)

    I_folder.open()
     
    I_folder = gui.addFolder('offices')
    I_folder.add(input_param, 'workplaces', 0,1,0.1)
    I_folder.open()

    
    global linesIfinal, meshesIfinal

    global count_Mainstreet,count_Substreet,count_Usage
    count_Mainstreet = 0
    count_Substreet = 0
    count_Usage = 0
    
    global curve_object
    curve_object = None

     #initiate empty curve2
    global curve_object_road
    curve_object_road = None


    #-----------------------------------------------------------------------

    # RENDER + UPDATE THE SCENE AND GEOMETRIES
    #Space for potential GUI- might be added later (still WIP)!
    
    render()

def Info_Table():
    
    global maxpopulation, areaLiving, workingpeople, areaIndustrials, Greenareaperperson, areaGreenAll, areaOffices, areaEducationAll, volumeoffice, volumIndustrial, volumeLiving
    
    if areaGreenAll == None:
        areaGreenAll = 0
    areaGreenAll = round(areaGreenAll)

    if Greenareaperperson == None:
        Greenareaperperson = 0
    Greenareaperperson = round(Greenareaperperson)
    
    if volumeLiving == None:
        volumeLiving = 0
    volumeLiving = round(volumeLiving)    
    
    if workingpeople == None:
        workingpeople = 0
    workingpeople = round(workingpeople)
    
    # if 'volumeoffice'  in globals():
    if volumeoffice == None:
        volumeoffice = 0
    volumeoffice = round(volumeoffice)
    
    if volumIndustrial == None:
        volumIndustrial = 0
    volumIndustrial = round(volumIndustrial)
    
    population = maxpopulation*input_param.population
    population = round(population)
    LivingSpacepp = 30
   
    
    
    body = js.document.getElementsByTagName('body')[0]
    
    existing_popul = js.document.getElementsByClassName("info-table-container")
    for i in existing_popul:
        body.removeChild(i)

    ################################################

    Popul = js.document.createElement('p')
    Popul_span = js.document.createElement('span')
    Popul_span.textContent = str(population)
    Popul_span.className = "Popul-span"
    Popul.appendChild(js.document.createTextNode("Popoulation: "))
    Popul.appendChild(Popul_span)
    Popul.className = "value-Popul-container"
    ####################################
    WorkPl = js.document.createElement('p')
    WorkPl_span = js.document.createElement('span')
    WorkPl_span.textContent = str(workingpeople)
    WorkPl_span.className = "WorkPl-span"
    WorkPl.appendChild(js.document.createTextNode("Number of workplaces: "))
    WorkPl.appendChild(WorkPl_span)
    WorkPl.className = "value-WorkPl-container"
    ####################################
    Green = js.document.createElement('p')
    Green_span_pp = js.document.createElement('span')
    Green_span_pp.textContent = str(Greenareaperperson)+" m² p/P"
    Green_span_pp.className = "Greenpp-span"
    Green_span_oa = js.document.createElement('span')
    Green_span_oa.textContent = str(areaGreenAll)+" m²"
    Green_span_oa.className = "Greenoa-span"

    Green.appendChild(js.document.createTextNode("Green Space: "))
    Green.appendChild(Green_span_pp)
    Green.appendChild(Green_span_oa)
    Green.className = "value-Green-container"

    ####################################
    Living = js.document.createElement('p')
    Living_span_pp = js.document.createElement('span')
    Living_span_pp.textContent = str(LivingSpacepp)+" m² p/P"
    Living_span_pp.className = "Livingpp-span"
    Living_span_oa = js.document.createElement('span')
    Living_span_oa.textContent = str(areaLiving)+" m²"
    Living_span_oa.className = "Livingoa-span"

    Living.appendChild(js.document.createTextNode("Living Space: "))
    Living.appendChild(Living_span_pp)
    Living.appendChild(Living_span_oa)
    Living.className = "value-Living-container"
    ####       ######         ########    #####        ######

    Living_vol = js.document.createElement('p')
    Living_vol_span = js.document.createElement('span')
    Living_vol_span.textContent = str(volumeLiving)+" m³"
    Living_vol_span.className = "Living_vol-span"
    Living_vol.appendChild(js.document.createTextNode("Built Living Volume: "))
    Living_vol.appendChild(Living_vol_span)
    Living_vol.className = "value-LivingVol-container"
    #####################################################

    Indus = js.document.createElement('p')
    Indus_span = js.document.createElement('span')
    Indus_span.textContent = str(areaIndustrials)+" m²"
    Indus_span.className = "Indus-span"
    Indus.appendChild(js.document.createTextNode("Built Industrial Space: "))
    Indus.appendChild(Indus_span)
    Indus.className = "value-Indus-container"

    ######### #######    ########         ########  ###

    Indus_Vol = js.document.createElement('p')
    Indus_Vol_span = js.document.createElement('span')
    Indus_Vol_span.textContent = str(volumIndustrial)+" m³"
    Indus_Vol_span.className = "IndusVol-span"
    Indus_Vol.appendChild(js.document.createTextNode("Built Industrial Volume: "))
    Indus_Vol.appendChild(Indus_Vol_span)
    Indus_Vol.className = "value-IndusVol-container"


    #############################
    Offi = js.document.createElement('p')
    Offi_span = js.document.createElement('span')
    Offi_span.textContent = str(areaOffices)+" m²"
    Offi_span.className = "Offi-span"
    Offi.appendChild(js.document.createTextNode("Built Office Space: "))
    Offi.appendChild(Offi_span)
    Offi.className = "value-Offi-container"

    ######### #######    ########         ########  ###

    Offi_Vol = js.document.createElement('p')
    Offi_Vol_span = js.document.createElement('span')
    Offi_Vol_span.textContent = str(volumeoffice)+" m³"
    Offi_Vol_span.className = "OffiVol-span"
    Offi_Vol.appendChild(js.document.createTextNode("Built Office Volume: "))
    Offi_Vol.appendChild(Offi_Vol_span)
    Offi_Vol.className = "value-OffiVol-container"

    ######################################
    Edu = js.document.createElement('p')
    Edu_span = js.document.createElement('span')
    Edu_span.textContent = str(areaEducationAll)+" m²"
    Edu_span.className = "Edu-span"
    Edu.appendChild(js.document.createTextNode("Built Education Space: "))
    Edu.appendChild(Edu_span)
    Edu.className = "value-Edu-container"


    #######################################

    container = js.document.createElement('div')
    container.className = "info-table-container"

    container.appendChild(Popul)
    container.appendChild(WorkPl)
    container.appendChild(Living)
    container.appendChild(Living_vol)
    container.appendChild(Indus)
    container.appendChild(Indus_Vol)
    container.appendChild(Green)
    container.appendChild(Offi)
    container.appendChild(Offi_Vol)
    container.appendChild(Edu)

    body.appendChild(container)

def Map1():
    global plane_map, geometrie,texture_Plane_Mesh_Mat 
    
    scene.remove(plane_map) 
    Plane_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Plane_Mesh_Mat = THREE.TextureLoader.new().load("./maps\StuttgartBerg.png")
    Plane_Mesh_Mat.map = texture_Plane_Mesh_Mat
    plane_map = THREE.Mesh.new( geometrie,Plane_Mesh_Mat)
    plane_map.translateZ(-3)
    scene.add( plane_map )

def Map2():
    global plane_map, geometrie,texture_Plane_Mesh_Mat 
    
    scene.remove(plane_map) 
    Plane_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Plane_Mesh_Mat = THREE.TextureLoader.new().load("./maps\Berlin.png")
    Plane_Mesh_Mat.map = texture_Plane_Mesh_Mat
    plane_map = THREE.Mesh.new( geometrie,Plane_Mesh_Mat)
    plane_map.translateZ(-3)
    scene.add( plane_map )
    
def Map3():
    global plane_map, geometry,texture_Plane_Mesh_Mat 
    
    scene.remove(plane_map) 
    Plane_Mesh_Mat = THREE.MeshPhongMaterial.new()
    texture_Plane_Mesh_Mat = THREE.TextureLoader.new().load("./maps\Frankfurt.png")
    Plane_Mesh_Mat.map = texture_Plane_Mesh_Mat
    plane_map = THREE.Mesh.new( geometrie,Plane_Mesh_Mat)
    plane_map.translateZ(-3)
    scene.add( plane_map )

def NoMap():
    global plane_map
    
    scene.remove(plane_map) 
    color_plane_map = THREE.Color.new ("rgb(200, 200, 200)")
    Plane_Mesh_Mat = THREE.MeshPhongMaterial.new( )
    Plane_Mesh_Mat.color = color_plane_map
    plane_map = THREE.Mesh.new( geometrie,Plane_Mesh_Mat)
    plane_map.translateZ(-3)
    scene.add(plane_map)

def Generate():
    global light2, light, count_Mainstreet,count_Substreet,count_Usage, Input_Road_Coords_py,Boundary_Coords_py
    scene.clear()
    scene.add(light2, light)
    scene.add(Reset_Mesh)
    scene.add(Save_Mesh)
    scene.add(light)
    scene.add(light2)
    scene.add(preview_Sphere)
    scene.add( plane_map )

####Generate Mainstreet
    if input_param.MainStreets == True or count_Mainstreet < 1 and input_param.GenerateCity == True or count_Mainstreet < 1 and input_param.SecondaryStreets == True or count_Mainstreet < 1 and input_param.AssignUsage == True:
        inputForSecondaryStreets = generateMainStreets(Boundary_Coords_py, Input_Road_Coords_py)
        count_Mainstreet += 1
####Generate Substreet
    if input_param.SecondaryStreets == True or count_Substreet < 1 and input_param.GenerateCity == True or count_Substreet < 1 and input_param.SecondaryStreets == True or count_Substreet < 1 and input_param.AssignUsage == True:
        untranslatedSubplotsAsList, translatedAndAllignedSubPlots = generateSecondaryStreets(inputForSecondaryStreets)
        count_Substreet += 1
####Assign Usage
    if input_param.AssignUsage == True or count_Usage < 1 and input_param.GenerateCity == True:
        generatePlotsAndAssign(untranslatedSubplotsAsList, translatedAndAllignedSubPlots)
        count_Usage += 1
### Generate City    
    if input_param.GenerateCity == True:
        global meshesfinal_listL, linesfinal_listL
        generateL ()
        global meshfinal_list2, linefinal_list2, meshplaneI
        generateI()
        global meshO_list2, lineO_list2
        generateO()
        generateG()
        generateE()
        Info_Table()
    
def regenerateAll():
    global light2, light
    scene.clear()
    scene.add(light2, light)
    scene.add(Reset_Mesh)
    scene.add(Save_Mesh)
    scene.add(light)
    scene.add(light2)
    scene.add(preview_Sphere)
    scene.add( plane_map )
    inputForSecondaryStreets = generateMainStreets(Boundary_Coords_py, Input_Road_Coords_py)
    untranslatedSubplotsAsList, translatedAndAllignedSubPlots = generateSecondaryStreets(inputForSecondaryStreets)
    generatePlotsAndAssign(untranslatedSubplotsAsList, translatedAndAllignedSubPlots)
    
    global meshesfinal_listL, linesfinal_listL
    generateL ()
    global meshfinal_list2, linefinal_list2, meshplaneI
    generateI()
    global meshO_list2, lineO_list2
    generateO()
    generateG() 
    generateE()
    
    Info_Table()
    

    
    planeGeometry = THREE.PlaneGeometry.new( 2000, 2000, 32, 32 )
    color = THREE.Color.new("rgb(200,200,200)")
    planeMaterial = THREE.ShadowMaterial.new()
    planeMaterial.color = color
    
    plane = THREE.Mesh.new( planeGeometry, planeMaterial )
    
    plane.translateZ(-2)
    plane.transparent = True 
    plane.opacity = 0
    plane.receiveShadow = True
    
    scene.add(plane) 

def generateMainStreets(BaseShapePoints,InputLineLines):     #Function that handles Main Street generation
        
       
        BaseShapeLines= generateLinesNum(BaseShapePoints)
        
        
        randomInputLines = InputLineLines.copy()
        random.shuffle(randomInputLines)        #Shuffles order of inputlines so that generated streets have potential to be different every time

        mainStreetNetwork = mainStreetGenerator(BaseShapeLines,randomInputLines)
    
        for i in BaseShapeLines:                            #Append BaseShapeLines to list of generated Streets
            mainStreetNetwork.append(i)
    
        splitMainStreetNetwork = splitMultipleLines(mainStreetNetwork)   #Split List of Streets and Baseshape into lines useable by loopfinder

        splitMainStreetNetworkAsList = []
        splitMainStreetNetworkAsListRounded = []
        for i in splitMainStreetNetwork:
            tempList = [i[0].tolist(),i[1].tolist()]
            splitMainStreetNetworkAsList.append(tempList)
            tempList = []

        for i in splitMainStreetNetworkAsList:  #Round all Points in Line-Network to 8 digits after comma so small rounding errors of the linesplitter get mitigated
            for j in i:
                temptemplist = [round(j[0],8),round(j[1],8)]
                tempList.append(temptemplist)
            splitMainStreetNetworkAsListRounded.append(tempList)
            tempList = []
    
        inputForSecondaryStreets = loop_finder(splitMainStreetNetworkAsListRounded)    #Find the Loops (Plots) out of the generated street-network
        return inputForSecondaryStreets

def generateSecondaryStreets(inputForSecondaryStreets):     #Function that handles Secondary street generation

    subPlotsAsNP = []
    for i in inputForSecondaryStreets:
        tempSubPlot = []
        for j in i:
            tempSubPlot.append(np.array([j[0],j[1]]))       #Transforms Plotslist back to numpy-arrays
        subPlotsAsNP.append(tempSubPlot)
   

    offsettedSubplotsAsNP = []
    for i in subPlotsAsNP:
        currentOffset = offsetNpPoly(i,4)       #Offset of main streets, the number in brackets is half the extra distance of the main streets!
        offsettedSubplotsAsNP.append(currentOffset)

    oldSubPlots = []
    for i in offsettedSubplotsAsNP:
        oldSubPlots.append(polygonDivider(i,600,3000,1,True, i))   #The actual "Secondary Street Generator"
    


    subPlots = addEveryPointToEveryPoly(oldSubPlots)



    untranslatedSubplots = []
    for i in range(len(oldSubPlots)):
        for k in oldSubPlots[i]:
            untranslatedSubplots.append(k)         #DO NOT USE, BUGGY, IDK WHY

    untranslatedSubplotsAsList = []

    for h in untranslatedSubplots:
        currentPoly = []
        for o in h:
            currentPoly.append(o.tolist())
        untranslatedSubplotsAsList.append(currentPoly) #USE THIS INSTEAD! TRANSLATE BACK FROM LIST IF NESSESARY!
           
    
    translatedAndAllignedSubPlots = translatePointsOnOffset(subPlotsAsNP,offsettedSubplotsAsNP,subPlots)     #Translate points of offsetted polygons and insert points of other polygons for neighborfinder
    
    translatedAndAllignedSubPlotsAsList = []
    for h in translatedAndAllignedSubPlots:
        currentPoly = []
        for o in h:
            currentPoly.append(o.tolist())
        translatedAndAllignedSubPlotsAsList.append(currentPoly)

    visualizeNormalPlots(untranslatedSubplotsAsList)

    return untranslatedSubplotsAsList, translatedAndAllignedSubPlotsAsList

def sortPointsByDistance(points, start_point):
    distances = [np.linalg.norm(point - start_point) for point in points]
    points_and_distances = list(zip(points, distances))
    sorted_points_and_distances = sorted(points_and_distances, key=lambda x: x[1])
    return [point for point, distance in sorted_points_and_distances]

def translatePointsOfPoly(oldPolyAsPoints,offsetPolyAsPoints,listOfPolysInoffsettedAsPtsOld):
    oldPolyAsLinesUE = []
    offsetPolyAsLinesUE = []

    def angle_between(v1, v2):
        v1_u = v1 / np.linalg.norm(v1)
        v2_u = v2 / np.linalg.norm(v2)
        return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))).round(1)

    def kickWrongLineFromPoly(newPolyLinesUE,oldPolyLinesUE):
        oldPolyLines = oldPolyLinesUE.copy()
        newPolyLines = newPolyLinesUE.copy()
        for i in range(len(oldPolyLines)):
            if i > len(newPolyLines)-1:
                oldPolyAsLines.pop(i)
                break
            oldVec = oldPolyLines[i][1]-oldPolyLines[i][0]
            newVec = newPolyLines[i][1]-newPolyLines[i][0]
            if angle_between(oldVec,newVec) != 0:
                oldPolyLines.pop(i)
                break
        if len(oldPolyLines) > len(newPolyLines):
            return kickWrongLineFromPoly(newPolyLines,oldPolyLines)
            
        return newPolyLines, oldPolyLines

    
    for i in range(len(oldPolyAsPoints)):      #Make Old poly as points to lines
        if i < len(oldPolyAsPoints)-1:
            CurrentLine = [oldPolyAsPoints[i], oldPolyAsPoints[i+1]]
            oldPolyAsLinesUE.append(CurrentLine)
        else:
            CurrentLine = [oldPolyAsPoints[i], oldPolyAsPoints[i-(len(oldPolyAsPoints)-1)]]
            oldPolyAsLinesUE.append(CurrentLine)

    for i in range(len(offsetPolyAsPoints)):    #Make offsetted poly as points to lines
        if i < len(offsetPolyAsPoints)-1:
            CurrentLine = [offsetPolyAsPoints[i], offsetPolyAsPoints[i+1]]
            offsetPolyAsLinesUE.append(CurrentLine)
        else:
            CurrentLine = [offsetPolyAsPoints[i], offsetPolyAsPoints[i-(len(offsetPolyAsPoints)-1)]]
            offsetPolyAsLinesUE.append(CurrentLine)

    if len(oldPolyAsPoints) > len(offsetPolyAsPoints):
        offsetPolyAsLines, oldPolyAsLines = kickWrongLineFromPoly(offsetPolyAsLinesUE,oldPolyAsLinesUE)
    else:
        offsetPolyAsLines = offsetPolyAsLinesUE.copy()
        oldPolyAsLines = oldPolyAsLinesUE.copy()


    listOfPolysInoffsettedAsPts = []
    for i in  listOfPolysInoffsettedAsPtsOld:
        listOfPolysInoffsettedAsPts.append(i)
   
    allPolyPoints = []
    for i in listOfPolysInoffsettedAsPts:
        for j in i:
           
            if any(np.array_equal(j.round(6), allPolyPoints[o].round(6)) for o in range(len(allPolyPoints))):
                continue
            else:
                allPolyPoints.append(j)

    
    pointsOnNewPoly = []
    pointsOnOldPoly = []
    for i in range(len(oldPolyAsLines)):
        vecOld = (oldPolyAsLines[i][1]-oldPolyAsLines[i][0])
        lenNew= np.linalg.norm(offsetPolyAsLines[i][1]-offsetPolyAsLines[i][0])
        for j in allPolyPoints:
            if np.all(j.round(6) == offsetPolyAsLines[i][0].round(6)): #If startpoint is same, just continue, otherwise point is gonna be doubled in the final list
                continue
            elif pointOnLineSegment(j,offsetPolyAsLines[i]):
                pointsOnNewPoly.append(j)
                lenCurrentLine = np.linalg.norm(j-offsetPolyAsLines[i][0])
                relationshipOnOffset = lenCurrentLine/lenNew
                newPt = oldPolyAsLines[i][0] + vecOld*relationshipOnOffset.round(6)
                pointsOnOldPoly.append(newPt)
                
    if len(pointsOnOldPoly) >= 1:
        for k in range(len(pointsOnNewPoly)):
            for j in range(len(listOfPolysInoffsettedAsPts)):
                if any(np.array_equal(pointsOnNewPoly[k].round(6), listOfPolysInoffsettedAsPts[j][o].round(6)) for o in range(len(listOfPolysInoffsettedAsPts[j]))):
                    index = arrayIndex(listOfPolysInoffsettedAsPts[j],pointsOnNewPoly[k])
                    del listOfPolysInoffsettedAsPts[j][index]
                    
                    listOfPolysInoffsettedAsPts[j].insert(index, pointsOnOldPoly[k])
                    
    return listOfPolysInoffsettedAsPts

def translatePointsOnOffset(oldPolygonsAsPoints,offsetPolygonsAsPoints,subPlotsInOffsettedPolygonsAsPoints):
    translatedSubplots = []
    
    
    for i in range(len(offsetPolygonsAsPoints)):
        currentTranslatedSubplots = translatePointsOfPoly(oldPolygonsAsPoints[i],offsetPolygonsAsPoints[i],subPlotsInOffsettedPolygonsAsPoints[i])
        for j in currentTranslatedSubplots:
            translatedSubplots.append(j)
        
    

    
    allSubplotPoints = []       #List of unique points present in translated subplots
    for i in translatedSubplots:
        for j in i:
           
            if any(np.array_equal(j.round(6), allSubplotPoints[o].round(6)) for o in range(len(allSubplotPoints))):
                continue
            else:
                allSubplotPoints.append(j)

    allNewSubplots = []
    for k in translatedSubplots:
        currentNewSubplot = []
        for i in range(len(k)):      #Test for every single line
            if i < len(k)-1:
                currentSubplotLine = [k[i], k[i+1]] 
            else:
                currentSubplotLine = [k[i], k[i-(len(k)-1)]]
            currentNewSubplot.append(k[i])      #append first point of currently viewed line to new plot
            pointsOnCurrentLine = []
            for j in allSubplotPoints:
                if (j[0] <= max(currentSubplotLine[0][0], currentSubplotLine[1][0]) + 1e-3 and j[0] >= min(currentSubplotLine[0][0], currentSubplotLine[1][0]) - 1e-3 and j[1] <= max(currentSubplotLine[0][1], currentSubplotLine[1][1]) + 1e-3 and j[1] >= min(currentSubplotLine[0][1], currentSubplotLine[1][1]) - 1e-3):
                    if np.all(j.round(6) == currentSubplotLine[0].round(6)) == False and np.all(j.round(6) == currentSubplotLine[1].round(6)) == False:
                        if pointOnLineSegment(j,currentSubplotLine):
                            pointsOnCurrentLine.append(j)
            if len(pointsOnCurrentLine) == 0:
                continue
            elif len(pointsOnCurrentLine) == 1:
                if any(np.array_equal(pointsOnCurrentLine[0].round(6), currentNewSubplot[o].round(6)) for o in range(len(currentNewSubplot))):
                    continue
                else:
                    currentNewSubplot.append(pointsOnCurrentLine[0])
                    continue
            else:
                sortedPointsOnLine = sortPointsByDistance(pointsOnCurrentLine,k[i])
                for h in sortedPointsOnLine:
                    if any(np.array_equal(h, currentNewSubplot[o].round(6)) for o in range(len(currentNewSubplot))):
                        continue
                    else:
                        currentNewSubplot.append(h)

        allNewSubplots.append(currentNewSubplot)
    
   
    
        
    return allNewSubplots

def addEveryPointToEveryPoly(polygons):
    allSubplotPoints = []       #List of unique points present in translated subplots
    for i in polygons:
        for j in i:
            for t in j:
                if any(np.array_equal(t.round(6), allSubplotPoints[o].round(6)) for o in range(len(allSubplotPoints))):
                    continue
                else:
                    allSubplotPoints.append(t)

    allNewSubplots = []
    for k in polygons:
        currentBigSubplot = []
        for p in k:
            currentNewSubplot = []
            for i in range(len(p)):      #Test for every single line
                if i < len(p)-1:
                    currentSubplotLine = [p[i], p[i+1]] 
                else:
                    currentSubplotLine = [p[i], p[i-(len(p)-1)]]
                currentNewSubplot.append(p[i])      #append first point of currently viewed line to new plot
                pointsOnCurrentLine = []
                for j in allSubplotPoints:
                    
                    if (j[0] <= max(currentSubplotLine[0][0], currentSubplotLine[1][0]) + 1e-3 and j[0] >= min(currentSubplotLine[0][0], currentSubplotLine[1][0]) - 1e-3 and j[1] <= max(currentSubplotLine[0][1], currentSubplotLine[1][1]) + 1e-3 and j[1] >= min(currentSubplotLine[0][1], currentSubplotLine[1][1]) - 1e-3):
                        if np.all(j.round(6) == currentSubplotLine[0].round(6)) == False and np.all(j.round(6) == currentSubplotLine[1].round(6)) == False:
                            if pointOnLineSegment(j,currentSubplotLine):
                                pointsOnCurrentLine.append(j)
                if len(pointsOnCurrentLine) == 0:
                    continue
                elif len(pointsOnCurrentLine) == 1:
                    if any(np.array_equal(pointsOnCurrentLine[0].round(6), currentNewSubplot[o].round(6)) for o in range(len(currentNewSubplot))):
                        continue
                    else:
                        currentNewSubplot.append(pointsOnCurrentLine[0])
                        continue
                else:
                    sortedPointsOnLine = sortPointsByDistance(pointsOnCurrentLine,p[i])
                    for h in sortedPointsOnLine:
                        if any(np.array_equal(h, currentNewSubplot[o].round(6)) for o in range(len(currentNewSubplot))):
                            continue
                        else:
                            currentNewSubplot.append(h)

            currentBigSubplot.append(currentNewSubplot)
        allNewSubplots.append(currentBigSubplot)
    return allNewSubplots

def visualizeNormalPlots(plotsaslist):

    dividedplotsaslines = []
    for x in plotsaslist:
        tempplotasline = []
        for i in range(len(x)):
            if i < len(x)-1:
                CurrentLine = [x[i], x[i+1]]
                tempplotasline.append(CurrentLine)
            else:
                CurrentLine = [x[i], x[i-(len(x)-1)]]
                tempplotasline.append(CurrentLine)
        dividedplotsaslines.append(tempplotasline)
    
    ThreeLinesStreet = []
    ThreeCurrentLine = []
    for x in dividedplotsaslines:
            singlePlot = []
            for i in x:
                for j in i:
                
                    ThreeVec1 = THREE.Vector2.new(j[0],j[1])
                    ThreeCurrentLine.append(ThreeVec1)
                singlePlot.append(ThreeCurrentLine)
                ThreeCurrentLine = []
            ThreeLinesStreet.append (singlePlot)
            singlePlot = []

    draw_system_streets(ThreeLinesStreet) 

def generatePlotsAndAssign(normalplots, translatedplots):
    global INPUT_LINES, PLOTS, toplots, NEIGHBOURS
    #INPUT_LINES = [[(int(point[0]), int(point[1])) for point in line] for line in lines]
    ##########################################################################################
    
    PLOTS= normalplots
    
    NEIGHBOURPLOTS = translatedplots
   
  
    ##########################################################################################
    toplots = [[tuple(x) for x in sublist] for sublist in NEIGHBOURPLOTS]#Convert in Tuples
    NEIGHBOURS = find_overlapping_plots(toplots)
    
    ##########################################################################################
    global DICTIONARY
    DICTIONARY = convert_data(NEIGHBOURS)
    
    DISTRIBUTION=find_solution(DICTIONARY)
    # POSSIBLE_CHANGES=random_distribution(DICTIONARY)
    
    colorPlots()
    # print ("Distribution",DISTRIBUTION)
    # print("Dictionary", DICTIONARY)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CLASS AND GENERATE MAIN DICTIONARY
global plotInformation

class plotInformation:
    def __init__(self, name, outerboundary, plotarea, neighbour, floors, areatype):
        self.name = name
        self.outerboundary = outerboundary
        self.newouterboundary = 0
        self.offsetvalue = 0
        self.plotarea = plotarea
        self.neighbour = neighbour
        self.floors = floors
        self.areatype = areatype
        self.areatyppopul = 0
        self.currentAreaPopul = 0
        self.currentArea = 0
        self.maxbuiltarea = 0
        
    
    def get_area(self):
        return self.plotarea
    
    def get_max_builtarea(self):
        self.maxbuiltarea = self.plotarea * input_param.density
        return self.maxbuiltarea
    
    def get_outerboundary(self):
        return self.outerboundary
    
    def set_floors(self, floors):
        self.floors = floors
    
    def reset(self):
        self.currentArea = 0
    


    def get_current_areaPopul(self):
        return self.currentAreaPopul
    
    
    def get_current_area(self):
        return self.currentArea
    
    def get_area_typePopul(self):
        return self.areatyppopul
    
    def get_area_type(self):
        return self.areatype
    def set_AreaTyppopuls(self,typus):
        self.areatyppopul = typus

    def set_Typus(self,typus):
        self.areatype = typus

    def calcCurrentAreaOfType(self):
        self.currentArea = self.calcIn(self.areatype)
        return self.currentArea

    def calcCurrentAreaPopulOfType(self):
        self.currentAreaPopul = self.calcIn(self.areatyppopul)
        return self.currentAreaPopul  
    #get_currentarea_oftype 
    def calcIn(self,typus):
        calculatedArea = 0
        
        if typus == 1:
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcH(self.outerboundary, 6)
            calculatedArea =  calculatedArea
        elif typus == 2: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcH(self.outerboundary, 6)
            calculatedArea = calculatedArea *2
        elif typus == 3: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcB(self.outerboundary)
            calculatedArea = calculatedArea *3
        elif typus == 4: 
            calculatedArea,  self.newouterboundary, self.offsetvalue = calcB(self.outerboundary)
            calculatedArea = calculatedArea *4
        elif typus == 5: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  =  calcB(self.outerboundary)
            calculatedArea = calculatedArea *5 
        elif typus == 6: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcB(self.outerboundary)
            calculatedArea = calculatedArea *6
        elif typus == 7: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcH(self.outerboundary, 10)
            calculatedArea = calculatedArea *7
        elif typus == 8: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcH(self.outerboundary, 10)
            calculatedArea = calculatedArea *8
        elif typus == 9: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcH(self.outerboundary, 10)
            calculatedArea = calculatedArea *9
        elif typus == 10: 
            calculatedArea,  self.newouterboundary, self.offsetvalue  = calcH(self.outerboundary, 10)
            calculatedArea = calculatedArea *10

        return calculatedArea
  
    
    def calc_max_area(self):
        maxarea,  newouterboundary, offsetvalue  = calcH(self.outerboundary,10)
        maxarea = self.plotarea *10
        return maxarea
            
def sortedDictPlotAreas (Dict_R, Plotsnumpyn):
    
    plotinfo = {} 
    for i in Dict_R.keys():
        if Dict_R[i]['value'] == "L":
            
            Boundary = Plotsnumpyn[i]
            
            #return offsetet area of each plot and original boundaries 
            
            calc_area = calc_plotArea(Boundary)
             

            #generate new dictionary with all the informations with the right value 
            plot = plotInformation(i, Boundary, calc_area, Dict_R[i]['neighbours'], 0, 0)
            plotinfo[i] = {'Plotobject': plot}
    

    #sort dictionary 
    dict_sort = {}
    dict_sort = sort_dict(plotinfo)
    
    return dict_sort

def colorPlots():
    global PLOTS
    PlotsNumpy = generateNumpyArray (PLOTS)
    for i in DICTIONARY.keys():
        if DICTIONARY[i]['value'] == "I":
            
            Boundary = PlotsNumpy[i]
            G(Boundary, THREE.Color.new("rgb(150,150,150)") )
    

        if DICTIONARY[i]['value'] == "E":
            
            Boundary = PlotsNumpy[i]
            G(Boundary, THREE.Color.new("rgb(202,176,140)") )
        
        if DICTIONARY[i]['value'] == "L":
            
            Boundary = PlotsNumpy[i]
            G(Boundary, THREE.Color.new("rgb(174,155,148)") )
        
        if DICTIONARY[i]['value'] == "O":
            
            Boundary = PlotsNumpy[i]
            G(Boundary, THREE.Color.new("rgb(161,173,173)") )
        
        if DICTIONARY[i]['value'] == "G":
            
            Boundary = PlotsNumpy[i]
            G(Boundary, THREE.Color.new("rgb(138,158,134)") )

def generateL ():
    global PlotsNumpy, dict_sorted, DICTIONARY, PLOTS
    PlotsNumpy = generateNumpyArray (PLOTS)
    dict_sorted = sortedDictPlotAreas (DICTIONARY, PlotsNumpy )
    
    global meshesfinal_listL, linesfinal_listL, groundsfinal, greenPG
    meshesfinal_listL, linesfinal_listL, groundsfinal, greenPG = generateTypeL(dict_sorted, input_param.offsetR, input_param.offsetH, input_param.heightperfloorR, input_param.heightperfloorB, input_param.heightperfloorH, input_param.population, input_param.density)

def generateI():
    global meshfinal_list2, linefinal_list2, meshplaneI, areaIndustrials, volumIndustrial
    meshfinal_list2 = []
    linefinal_list2 = []
    meshplaneI = []
    
    volumIndustrial = 0
    areaIndustrials = 0
    for i in DICTIONARY.keys():
        if DICTIONARY[i]['value'] == "I":
            #loop_check_angle(PLOTS)
        
            Boundary = PlotsNumpy[i]
            #print("Boundary", Boundary)
            linesI, meshesI, planeI, areaplot = offsetAndGenerateShapeI(Boundary,input_param.distancestreetI, THREE.Color.new("rgb(180,180,180)"), THREE.Color.new("rgb(150,150,150)"),  THREE.Color.new("rgb(150,150,150)"),1, input_param.height)
            
            areaIndustrials += areaplot
            volumperplot = areaplot*input_param.height
            volumIndustrial += volumperplot
            
            linefinal_list2.append(linesI)
            meshfinal_list2.append(meshesI)
            meshplaneI.append(planeI)
    
    return areaIndustrials, volumIndustrial

def generateO():
    global meshO_list2, lineO_list2, workingpeople, areaOffices, volumeoffice
    meshO_list2 = []
    lineO_list2 = []
    
    volumeoffice = 0
    workingpeople = 0
    areaOffices = 0
    for i in DICTIONARY.keys():
        if DICTIONARY[i]['value'] == "O":
            #loop_check_angle(PLOTS)
        
            Boundary = PlotsNumpy[i]
            linesO, meshesO, PeoplePerPlot, AreaperPlot = offsetAndGenerateShapeO(Boundary,THREE.Color.new("rgb(218,235,235)"), THREE.Color.new("rgb(161,173,173)"),  THREE.Color.new("rgb(161,173,173)"), input_param.heightperfloorO)
            
           
            workingpeople += PeoplePerPlot
            areaOffices += AreaperPlot
            lineO_list2.append(linesO)
            meshO_list2.append(meshesO)
            # meshplaneO.append(planeO)
    volumeoffice = areaOffices*input_param.heightperfloorO
   
    return workingpeople, AreaperPlot, areaOffices

def generateG():
    global areaGreenAll, maxpopulation, Greenareaperperson
    areaGreenAll = 0
    for i in DICTIONARY.keys():
        if DICTIONARY[i]['value'] == "G":
            
            Boundary = PlotsNumpy[i]
            
            G(Boundary, THREE.Color.new("rgb(138,158,134)") )
            areagreenplot = Area(Boundary)
            areaGreenAll += areagreenplot
    
    if  maxpopulation > 0:
        Greenareaperperson = areaGreenAll/maxpopulation
    else:
        Greenareaperperson = 0
    
    return areaGreenAll, Greenareaperperson

def generateE():
    global areaEducationAll
    areaEducationAll = 0 
    for i in DICTIONARY.keys():
        if DICTIONARY[i]['value'] == "E":
 
            Boundary = PlotsNumpy[i]
            E(Boundary, THREE.Color.new("rgb(245,223,191)"), THREE.Color.new("rgb(202,176,140)"),  THREE.Color.new("rgb(202,176,140)"), 1, 4)
            
            areaEducation = Area(Boundary)
            areaEducationAll += areaEducation
            
    return areaEducationAll

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# UPDATE FUNCTIONS 
def updateI():
    
    global meshfinal_list2, linefinal_list2, meshplaneI, DICTIONARY, PlotsNumpy, scene
  
   
    if input_param.oldheight != input_param.height:
     
        for sub_list in linefinal_list2:
            for line in sub_list:
                scene.remove(line)    
        
        for sublist2 in meshfinal_list2:
            for mesh in sublist2:
                scene.remove(mesh)
        
        for mesh in meshplaneI:
            scene.remove(mesh)
    
     
        linefinal_list2 = []
        meshfinal_list2 = []
        meshplaneI = []

        
        generateI()
        Info_Table()
   
            
    input_param.oldheight = input_param.height
 
def updateO():
    global meshO_list2, lineO_list2, DICTIONARY, PlotsNumpy, scene
    if input_param.workingpeopleold != input_param.workplaces:
        # input_param.distancetostreetO != input_param.olddistancetostreetO
        
        for sub_list in lineO_list2:
            for line in sub_list:
                scene.remove(line)    
        
        for sublist2 in meshO_list2:
            for mesh in sublist2:
                scene.remove(mesh)
        
        # for mesh in meshplaneO:
        #     scene.remove(mesh)
    
     
        meshO_list2 = []
        lineO_list2 = []
        # meshplaneO = []
        
        
        generateO()
        Info_Table()
            
    input_param.workingpeopleold = input_param.workplaces

def updateL ():
  
    global meshesfinal_listL, linesfinal_listL, greenPG,  groundsfinal, DICTIONARY, PlotsNumpy, scene
    if input_param.populationold_density != input_param.density or input_param.iputOld != input_param.population:
        
        
        for sub_list in linesfinal_listL:
            for line in sub_list:
                scene.remove(line)    
        
        for sublist2 in meshesfinal_listL:
            for mesh in sublist2:
                scene.remove(mesh)
        
        for i in range(len(groundsfinal)):
            scene.remove(groundsfinal[i])
        
        for mesh in greenPG:
            scene.remove(mesh)
            
        
     
        meshesfinal_listL = []
        linesfinal_listL = []
        groundsfinal = []
        greenPG = []
        
        
        generateL ()
        Info_Table()
            
    input_param.iputOld = input_param.population
    input_param.populationold_density = input_param.density


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CALCULATE FUNCTIONS
def Area(corners):#DONT TOUCH

    n = len(corners) # of corners
    area = 0

    for i in range(n):
        j = (i + 1) % n
        area += (corners[i][0] * corners[j][1])
        area -= (corners[j][0] * corners[i][1])
    area = abs(area)//2.0

    return area

def calc_plotArea(arraypoints):#DONT TOUCH
    
    areaOuterBoundary = Area(arraypoints)
    return areaOuterBoundary

def calcmaxpeople(dict_sorted):#DONT TOUCH
    
    choose_type = 0
    
    area_all = 0 
    while choose_type < 10:
        for i in dict_sorted.keys():
            currentArea = 0
            
            if dict_sorted[i]['Plotobject'].get_area_typePopul() != 0:
                currentArea = dict_sorted[i]['Plotobject'].get_current_areaPopul()
            
            max_built_area = dict_sorted[i]['Plotobject'].get_max_builtarea() 
            
            if currentArea >= max_built_area:
                
                population_possible_max = area_all//30
                return population_possible_max

            dict_sorted[i]['Plotobject'].set_AreaTyppopuls(choose_type)
            builtarea_per_plot = dict_sorted[i]['Plotobject'].calcCurrentAreaPopulOfType()
            
            area_all = area_all - currentArea
            area_all = area_all + builtarea_per_plot

            
        choose_type += 1
        
        population_possible_max = area_all//30
        
    return   population_possible_max

def calculatetype(dict_sorted, density ,population, maxpopul):#DONT TOUCH
    
    choose_type = 0
    
    area_all = 0 
    while choose_type < 10:
        for i in dict_sorted.keys():
            currentArea = 0
            
            if dict_sorted[i]['Plotobject'].get_area_type() != 0:
                currentArea = dict_sorted[i]['Plotobject'].get_current_area()
            
            max_built_area = dict_sorted[i]['Plotobject'].get_max_builtarea() 
            
            if currentArea >= max_built_area:
                return area_all
           
            dict_sorted[i]['Plotobject'].set_Typus(choose_type)
            builtarea_per_plot = dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()
            
            area_all = area_all - currentArea
            area_all = area_all + builtarea_per_plot
            population_possible = area_all//30
            if population_possible >= maxpopul*input_param.population:
                #print("choose_type return 1", choose_type)
                return area_all
        
        choose_type += 1

    return area_all      

def calcB (arraypoints):#PUT YOUR HANDS HERE calculates Living with Hole  (Blockrandbebauung)

    Xcoordinatesb, Ycoordinatesb = generatexy (arraypoints)
    offsetpolyB = offsetNpPoly(arraypoints, 4)
    Xcoordinates5, Ycoordinates5 = generatexy(offsetpolyB)
    points_check = convert_into_Points(Xcoordinates5, Ycoordinates5)
   
    if determine_loop_direction(points_check) == "Counterclockwise":
       
        offsetvalueouter = 0
        offsetpolyB = arraypoints
        # Xcoordinates5 = Xcoordinatesb
        # Ycoordinates5 = Ycoordinatesb
    
    

    offsetpolyBB = offsetNpPoly(offsetpolyB, 2)
    OffsetX, OffsetY = generatexy(offsetpolyBB)
    points_check2 = convert_into_Points(OffsetX, OffsetY)
    
    if determine_loop_direction(points_check2) == "Counterclockwise":
       
        offsetvalueouter = 0

        
        OffsetX = Xcoordinates5
        OffsetY = Ycoordinates5
    
    newOuterboundary = convert_result_check_W(OffsetX, OffsetY)
    areaOuterBoundary = Area(newOuterboundary)
    boundarylengths = lengthBoundary(OffsetX, OffsetY)

    
    
    
    offsetvalue = 2.5
    while min(boundarylengths) > 15 or offsetvalue <=4 :###########################CHANGES ROBERT
        
        Oldoffset = offsetvalue
        

        offsetvalue += 0.5
        
        offsetPolyBBB = offsetNpPoly(newOuterboundary, offsetvalue)
        Offset2X, Offset2Y = generatexy(offsetPolyBBB)
        boundarylengths = lengthBoundary(Offset2X, Offset2Y)
        Points_2_check = convert_into_Points(Offset2X, Offset2Y)
    
        if min(Offset2X) == min(OffsetX) or determine_loop_direction(Points_2_check) == "Counterclockwise":
           
            offsetPolyBBB = offsetNpPoly(newOuterboundary, Oldoffset)
            
            areaInnerBoundary = Area(offsetPolyBBB)
            final_area = areaOuterBoundary - areaInnerBoundary
            
            return (final_area, newOuterboundary,Oldoffset)

        else: 
            # convertInnerBoundary = convert_result_check_W(Offset2X, Offset2Y)
            areaInnerBoundary = Area(offsetPolyBBB)
            final_area = areaOuterBoundary - areaInnerBoundary

    
    final_area = areaOuterBoundary
    return (final_area, newOuterboundary,offsetvalue)

def calcH(arraypoints, minlengthbl):#PUT YOUR HANDS HERE calculates Living without Hole
    
    
    outerboundArray = []
    offsetvpoly = offsetNpPoly(arraypoints, 4)

    Xcoordinates5, Ycoordinates5 = generatexy(arraypoints)
    points_check = convert_into_Points(Xcoordinates5, Ycoordinates5)
    
    if determine_loop_direction(points_check) == "Counterclockwise":
        OffsetListdividedPoly = [0]
        
        oldAreaOuterBoundary = Area(arraypoints)
        outerboundArray.append(arraypoints)
        
        return oldAreaOuterBoundary, outerboundArray, OffsetListdividedPoly
    
    
    else:
        
        dividedPoly = polygonDivider(offsetvpoly,100, 25000, 1, True,offsetvpoly)
        
        
        
        OffsetListdividedPoly = []
        areaPlotfinal = []
        
        finalArea = 0
        for i in dividedPoly:
            
            offsetvalue = 0
            areaPlotvalidR = Area(i)
            Xcoordinatesb, Ycoordinatesb = generatexy (i)
            #check distance of intersectes points and offsets plot if possible
            boundarylengths = lengthBoundary(Xcoordinatesb, Ycoordinatesb)

            while min(boundarylengths) > minlengthbl:  
                
                Oldoffset = offsetvalue
                    
                offsetvalue += 1
                
                offsetpoly = offsetNpPoly(i,offsetvalue)
                OffsetX, OffsetY = generatexy(offsetpoly)
                boundarylengths = lengthBoundary(OffsetX, OffsetY)
               
                
                Points_2_check = convert_into_Points(OffsetX, OffsetY)
                
                if min(OffsetX) == min(Xcoordinatesb) or determine_loop_direction(Points_2_check) == "Counterclockwise":
                    
                    oldoffsetpoly = offsetNpPoly(i, Oldoffset)
                    
                    areaPlotvalidR = Area(oldoffsetpoly)
                    
                    offsetvalue = Oldoffset
                    break 
            

                else: 
                    
                    areaPlotvalidR = Area(offsetpoly)

            areaPlotfinal.append(areaPlotvalidR)
            OffsetListdividedPoly.append(offsetvalue)

        areaR = 0
        for area in areaPlotfinal:
            areaR += area
        
       
        return areaR, dividedPoly, OffsetListdividedPoly
    
def calc(arraypoints, minboundarylength):#PUT YOUR HANDS HERE calcutes for Industrial and Offices###min BOUNDARY TURNED OFF
    
    offsetvalue = 0
    Xcoordinatesb, Ycoordinatesb = generatexy (arraypoints)
    #check distance of intersectes points and offsets plot if possible
    boundarylengths = lengthBoundary(Xcoordinatesb, Ycoordinatesb)
    
    while offsetvalue < 8 : #################### MIN BUNDARY
        #print("boundarylengths",min(boundarylengths))
        
        Oldoffset = offsetvalue
        
            
        offsetvalue += 0.5
        
        offsetpolyC = offsetNpPoly(arraypoints,offsetvalue)
        OffsetX, OffsetY= generatexy(offsetpolyC)
        boundarylengths = lengthBoundary(OffsetX, OffsetY)

        
        Points_2_check = convert_into_Points(OffsetX, OffsetY)
        
        if min(OffsetX) == min(Xcoordinatesb) or determine_loop_direction(Points_2_check) == "Counterclockwise":
            
            
            return Oldoffset
   
    return offsetvalue


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROZESS AND CALLDRAWFUNTION
def G(arraypoints, colorp):#Generate Meshes on the Ground
    
    newboundary = offsetallplots5(arraypoints)
    #convert x and y lists 
    OffsetX, OffsetY = generatexy(newboundary)
    xCoordAr, yCoordAr = makeFloatfromPoint(OffsetX, OffsetY)
    pleneGGG = plane(xCoordAr,yCoordAr,colorp)
    
    return pleneGGG

def R(arraypoints, floors, heightperfloor):#Build Residentials

    meshesRfinal = []
    linesRfinal = []
 
    
    area, dividedboundary, dividedoffset = calcH(arraypoints,6)
    
    

    length = len(dividedboundary)
    
    for i in range(0, length):
    
        offsetpolyR = offsetNpPoly(dividedboundary[i], dividedoffset[i])
        xCoordsf, yCoordsf = generatexy(offsetpolyR)
        xCoordAr,yCoordAr = makeFloatfromPoint(xCoordsf, yCoordsf) 
  
        
        meshesR, linesR = generateShape(xCoordAr,yCoordAr,THREE.Color.new("rgb(204,185,178)"), THREE.Color.new("rgb(174,155,148)"),floors, heightperfloor)
        
        for j in range(len(meshesR)):
            meshesRfinal.append(meshesR[j])
        
        for k in range(len(linesR)):
            linesRfinal.append(linesR[k])
    
  
    SB=2
    

    offsetpoly = offsetallplots_Highrise(arraypoints,SB)
    Xcoordinates, Ycoordinates = generatexy(offsetpoly)
    xCoordB, yCoordB = makeFloatfromPoint( Xcoordinates, Ycoordinates)
    
    planeR = plane(xCoordB,yCoordB,THREE.Color.new("rgb(174,155,148)"))
    
    return meshesRfinal, linesRfinal, planeR

def B(arraypoints, colorm, colorl, colorp, floors, heightperfloor):#Build Blocks #### if Bug not in somewhere in calcB its prly here

   
    area, boundary, Offsetv  = calcB(arraypoints) 
    
    xCoordB, yCoordB = generatexy (boundary)
    length = lengthBoundary( xCoordB, yCoordB)
    xCoordBF, yCoordBF = makeFloatfromPoint(xCoordB, yCoordB) 
    
    if  min (length)< 8:

        plane1 = plane(xCoordBF, yCoordBF,colorp)
        meshes_listB, lines_listB = generateShape(xCoordBF,yCoordBF,colorm,colorl, floors, heightperfloor )
    
    else:
        
        offsetpolyB = offsetNpPoly(boundary, Offsetv)
        OffsetX, OffsetY = generatexy(offsetpolyB)
        xCoordAr, yCoordAr = makeFloatfromPoint(OffsetX, OffsetY) 
        
        BlockPermiterLines = ListPoint2Lines(xCoordAr, yCoordAr)
        BlockPermiterLines = numLinesToVec(BlockPermiterLines)
        
        plane1 = plane(xCoordBF, yCoordBF,colorp)
        meshes_listB, lines_listB = generateShapeblock(xCoordBF,yCoordBF,colorm,colorl,xCoordAr, yCoordAr, BlockPermiterLines,floors, heightperfloor)

    return meshes_listB, lines_listB, plane1

def H(arraypoints, floors, heightperfloor):#Build Highrise #hardcoded offset floor number
    
    meshesRfinal = []
    linesRfinal = []
    
    area, dividedboundary, dividedoffset = calcH(arraypoints, 10)
    length = len(dividedboundary)
    
    for i in range(0, length):
        
        offsetpolyH = offsetNpPoly(dividedboundary[i], dividedoffset[i])
        xCoordsf, yCoordsf = generatexy (offsetpolyH)
        xCoordAr,yCoordAr = makeFloatfromPoint(xCoordsf, yCoordsf) 
    
    #generate list of lines
        # IntersectionLines = ListPoint2Lines(xCoordsf, yCoordsf)
        # IntersectionLines = numLinesToVec(IntersectionLines)
        # draw_system(IntersectionLines)
        
        meshesR, linesR = generateShape(xCoordAr,yCoordAr,THREE.Color.new("rgb(204,185,178)"), THREE.Color.new("rgb(174,155,148)"),4, heightperfloor)
        
        for j in range(len(meshesR)):
            meshesRfinal.append(meshesR[j])
        
        for k in range(len(linesR)):
            linesRfinal.append(linesR[k])

        boundaryoffsett = convert_result_check_W(xCoordsf, yCoordsf)
        offsetValTop = calc(boundaryoffsett, 8)
        
        offsetpollyHTop = offsetNpPoly(offsetpolyH,2)
        
        Offset2X, Offset2Y = generatexy(offsetpollyHTop)
        xCoordAr2, yCoordAr2 = makeFloatfromPoint(Offset2X, Offset2Y)

        meshesTop, linesTop = generateShapeTop(xCoordAr2, yCoordAr2,THREE.Color.new("rgb(204,185,178)"), THREE.Color.new("rgb(174,155,148)"),round((floors//4)), heightperfloor)
        for j in range(len(meshesTop)):
            meshesRfinal.append(meshesTop[j])
        
        for k in range(len(linesTop)):
            linesRfinal.append(linesTop[k])
    
    
    SB=2
    offsetpoly = offsetallplots_Highrise(arraypoints,SB)
    Xcoordinates, Ycoordinates = generatexy(offsetpoly)
    xCoordB, yCoordB = makeFloatfromPoint( Xcoordinates, Ycoordinates)
    planeH = plane(xCoordB,yCoordB,THREE.Color.new("rgb(174,155,148)"))
    
    return meshesRfinal, linesRfinal, planeH

def E(arraypoints, colorm, colorp, colorl, floors, heightperfloor):#build e

    newOuterboundary = offsetallplots5(arraypoints)
    
    Xcoordinates, Ycoordinates = generatexy(newOuterboundary)

    xCoordB, yCoordB = makeFloatfromPoint( Xcoordinates, Ycoordinates)
    
    offsetvalue = calc(newOuterboundary, 10)
    
    offsetpoly = offsetNpPoly(newOuterboundary, offsetvalue)

    OffsetX, OffsetY = generatexy(offsetpoly)
    xCoordAr, yCoordAr = makeFloatfromPoint(OffsetX, OffsetY)

    

    plane1 = plane(xCoordB, yCoordB,colorp)
    meshesI, linesI = generateShape(xCoordAr,yCoordAr,colorm, colorl,floors, heightperfloor)
    
    return meshesI, linesI, plane1

def generateTypeL (dict_sorted, offsetR, offsetH, heightperfloorR, heightperfloorB, heightperfloorH, population, density):##dont TouchChooses which type will be built
    global maxpopulation, areaLiving, volumeLiving
    
    maxpopulation = calcmaxpeople(dict_sorted)
   
    areaLiving = calculatetype(dict_sorted, density, population, maxpopulation)
    
    colorm = THREE.Color.new("rgb(203,182,168)")
    colorm = THREE.Color.new("rgb(238,214,206)")
    colorm = THREE.Color.new("rgb(204,185,178)")
    
    colorl = THREE.Color.new("rgb(189,136,110)")
    colorp = THREE.Color.new("rgb(174,155,148)")
    
    volumeLiving = 0
    meshes_listL = []
    lines_listL = []
    meshes_list = []
    lines_list = []
    ground = []
    groundes = []
    green = []
    greenP = []
    
    for i in dict_sorted.keys():
            #print("typus", dict_sorted[i]['Plotobject']. get_area_type())
            
            if dict_sorted[i]['Plotobject']. get_area_type() == 0:
                greenP = G(dict_sorted[i]['Plotobject'].get_outerboundary(), THREE.Color.new("rgb(138,158,134)"))
            
            if dict_sorted[i]['Plotobject']. get_area_type() == 1:
                meshes_list, lines_list, ground = R(dict_sorted[i]['Plotobject'].get_outerboundary(), 1, heightperfloorR)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorR
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 2:
                meshes_list, lines_list, ground = R(dict_sorted[i]['Plotobject'].get_outerboundary(), 2, heightperfloorR)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorR
                
            elif dict_sorted[i]['Plotobject']. get_area_type() == 3:
                meshes_list, lines_list, ground = B(dict_sorted[i]['Plotobject'].get_outerboundary(),colorm, colorl, colorp, 3, heightperfloorB)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorB
                
            elif dict_sorted[i]['Plotobject']. get_area_type() == 4:
                meshes_list, lines_list, ground = B(dict_sorted[i]['Plotobject'].get_outerboundary(), colorm,colorl, colorp, 4, heightperfloorB)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorB
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 5:
                meshes_list, lines_list, ground = B(dict_sorted[i]['Plotobject'].get_outerboundary(), colorm, colorl, colorp,5, heightperfloorB)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorB
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 6:
                meshes_list, lines_list, ground = B(dict_sorted[i]['Plotobject'].get_outerboundary(), colorm,colorl, colorp, 6, heightperfloorB)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorB
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 7:
                meshes_list, lines_list, ground = H(dict_sorted[i]['Plotobject'].get_outerboundary(), 7, heightperfloorH)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorH
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 8:
                meshes_list, lines_list, ground = H(dict_sorted[i]['Plotobject'].get_outerboundary(),  8, heightperfloorH)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorH
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 9:
                meshes_list, lines_list, ground = H(dict_sorted[i]['Plotobject'].get_outerboundary(),  9, heightperfloorH)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorH
            
            elif dict_sorted[i]['Plotobject']. get_area_type() == 10:
                meshes_list, lines_list, ground = H(dict_sorted[i]['Plotobject'].get_outerboundary(), 10, heightperfloorH)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorH
            elif dict_sorted[i]['Plotobject']. get_area_type() == 11:
                meshes_list, lines_list, ground = H(dict_sorted[i]['Plotobject'].get_outerboundary(), 11, heightperfloorH)
                volumeLiving += dict_sorted[i]['Plotobject'].calcCurrentAreaOfType()*heightperfloorH
            
            meshes_listL.append(meshes_list)
        
            lines_listL.append(lines_list)
            groundes.append (ground)
            green.append(greenP)
        
            
    return meshes_listL, lines_listL, groundes, green

def offsetAndGenerateShapeO(arraypoints, colorm, colorl, colorp , heightperfloor):#Prly everything Fine, DONT TOUCH if ur not 100% its this funtion thats bugging
    global scene 
        
    newOuterboundary = offsetallplots5(arraypoints)
    Xcoordinates, Ycoordinates = generatexy(newOuterboundary)
    xCoordB, yCoordB = makeFloatfromPoint( Xcoordinates, Ycoordinates)
    
    offsetvalue = calc(newOuterboundary, 15)
    
    floor = (offsetvalue*2)/heightperfloor
    floors = round(floor) 
   
    offsetpolyg = Offset_Shapely(newOuterboundary, offsetvalue,-1)
    
    arePerPlot = Area(offsetpolyg)
    
    peoploperplot = (arePerPlot*floors)//10
    
    peoploperplot = input_param.workplaces * peoploperplot
    floor = (peoploperplot * 10 )//arePerPlot
    if floor != None:
        floors = round(floor)
        if floors == 0:
            peoploperplot = 0
    else: 
        floors == 0
        peoploperplot = 0



    OffsetX, OffsetY = generatexy(offsetpolyg)
    xCoordAr, yCoordAr = makeFloatfromPoint(OffsetX, OffsetY)

   
    plane1 = plane(xCoordB, yCoordB,colorp)
    meshesI, linesI = generateShape(xCoordAr,yCoordAr,colorm, colorl,floors, heightperfloor)
    
    return meshesI, linesI, peoploperplot, arePerPlot
    
def offsetAndGenerateShapeI(arraypoints, offsetvalue, colorm, colorl, colorp , floors, heightperfloor): #prly no mistakes here
   
    newOuterboundary = offsetallplots5(arraypoints)
    Xcoordinates, Ycoordinates = generatexy(newOuterboundary)
    xCoordB, yCoordB = makeFloatfromPoint( Xcoordinates, Ycoordinates)
    plane1 = plane(xCoordB, yCoordB,colorp)
    
   
    
    dividedPoly = polygonDivider(newOuterboundary,50, 25000, 1, True,newOuterboundary, False,False,False,0.2,[],78)
   
      
    if dividedPoly == None:
        dividedPoly = []
        dividedPoly.append(arraypoints)
    
    
    areadividedplots = []
    for i in dividedPoly:
        area_per_plot =  Area(i)
        areadividedplots.append(area_per_plot)

    j = areadividedplots.index(max(areadividedplots))
    
    # xcoordj, ycoordj = generatexy(dividedPoly[j])
    maxoffset= calc(dividedPoly[j],5)
    
    if maxoffset == 0:
        maxheightperfloor = 3
        offsetvalue = 0 
    
    else:
        maxheightperfloor = maxoffset*2
        offsetvalue = heightperfloor//2
        
    if offsetvalue < maxoffset and heightperfloor < maxheightperfloor:
        
        offsetmaxpoly = offsetNpPoly(dividedPoly[j], offsetvalue)
        OffsetX, OffsetY = generatexy(offsetmaxpoly)
        xCoordAr, yCoordAr = makeFloatfromPoint(OffsetX, OffsetY)
        
        arePerPlot = Area(offsetmaxpoly)

        meshesI, linesI = generateShape(xCoordAr,yCoordAr,colorm, colorl,floors, heightperfloor)
        return meshesI, linesI, plane1, arePerPlot

    else: 
        
        offsetmaxpoly = offsetNpPoly(dividedPoly[j], maxoffset)
        OffsetX, OffsetY = generatexy(offsetmaxpoly)
        xCoordAr, yCoordAr = makeFloatfromPoint(OffsetX, OffsetY)
        
        arePerPlot = Area(offsetmaxpoly)

        
        meshesI, linesI = generateShape(xCoordAr,yCoordAr,colorm, colorl,floors, maxheightperfloor)
    
        return meshesI, linesI, plane1, arePerPlot
        

def offsetallplots5(arraypoints):#Offset all Boundarys to generate sub streets

    
    offsetpoints = offsetNpPoly(arraypoints, 4)

    if determine_loop_direction(offsetpoints) == "Counterclockwise":
    
        return arraypoints
    
    return offsetpoints
def offsetallplots_Highrise(arraypoints,setbackdistance):#Offset all Boundarys to generate sub streets

    
    offsetpoints = offsetNpPoly(arraypoints, setbackdistance)

    if determine_loop_direction(offsetpoints) == "Counterclockwise":
    
        return arraypoints
    
    return offsetpoints

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DRAW FUNKTIONS THREEJS 
#draw lines 
def draw_system(lines):

    for points in lines:
        line_geom = THREE.BufferGeometry.new()

        points = to_js(points)
        line_geom.setFromPoints( points )
        material = THREE.LineBasicMaterial.new( THREE.Color.new(0x0000ff))
        vis_line = THREE.Line.new( line_geom, material )

        global scene
        scene.add(vis_line)
#draw plane surface        
def plane(xCordsArray,yCordsArray,color):

    shape_Green = THREE.Shape.new()

    for i in range(len(xCordsArray)):
        if i == 0 :
            #("moveTo",xCordsArray[i], yCordsArray[i])
            shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
        else: 
            shape_Green.lineTo(xCordsArray[i], yCordsArray[i])     
    geometryplane = THREE.ShapeGeometry.new(shape_Green)
    
    #colorgreen = 
    meshgreen_material = THREE.MeshPhongMaterial.new(color)
    meshgreen_material.color = color
    meshgreen = THREE.Mesh.new(geometryplane, meshgreen_material)
    meshgreen.receiveShadow = True
    
    # colorS = THREE.Color.new("rgb(180,180,180)")
    # planeMaterial = THREE.ShadowMaterial.new(colorS)
    # planeMaterial.color = colorS
    # plane = THREE.Mesh.new( geometryplane, planeMaterial )
    # plane.receiveShadow = True
    # plane.transparent = True 
    # plane.opacity = 0.5
    
    scene.add(meshgreen)
    # scene.add(plane)
    
    return meshgreen

 
#generate shapes to extrude and cap 

global generateShape
def generateShape(xCordsArray,yCordsArray, color, colorl, floors, heightperfloor,):#all geometries except Blockrand
    
    global scene
   
    extrudeSettings = {"steps" : 20,"depth" : 3.5,"bevelEnabled": False, "bevelSize": 0 }
    extrudeSettings["depth"] = heightperfloor
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings ))
    
    mesh_list1 = []
    line_list1 = []
    
    for k in range(floors):
        shape_Green = THREE.Shape.new()
    
        for i in range(len(xCordsArray)):
            if i == 0 :
                shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
            else: 
                shape_Green.lineTo(xCordsArray[i], yCordsArray[i])  

        geometry = THREE.ExtrudeGeometry.new(shape_Green,extrudeSettings)
        geometry.translate(0, 0, extrudeSettings.depth*k)
        mesh_material = THREE.MeshPhongMaterial.new(color)
       
        
        mesh_material.color = color
        mesh = THREE.Mesh.new(geometry, mesh_material)
        mesh_list1.append(mesh)
        
        mesh.castShadow = True
        mesh.receiveShadow = False  
        scene.add(mesh)
        
        edgesout = THREE.EdgesGeometry.new( geometry )
        linematerial = THREE.LineBasicMaterial.new( colorl )
        
        linematerial.color = colorl
        line = THREE.LineSegments.new( edgesout, linematerial )
        line_list1.append(line)
   
        scene.add(line)
        
        
    return mesh_list1, line_list1  

def generateShapeTop(xCordsArray,yCordsArray, color, colorl, floors, heightperfloor):#setback on highrises


    extrudeSettings = {"steps" : 20,"depth" : 3.5,"bevelEnabled": False, "bevelSize": 0 }
    extrudeSettings["depth"] = heightperfloor
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings ))
    
    linesTop = []
    meshesTop = []
    
    for k in range(floors):
        shape_Green = THREE.Shape.new()
    
        for i in range(len(xCordsArray)):
            if i == 0 :
                shape_Green.moveTo (xCordsArray[i], yCordsArray[i])
            else: 
                shape_Green.lineTo(xCordsArray[i], yCordsArray[i])  

        geometry = THREE.ExtrudeGeometry.new(shape_Green,extrudeSettings)
        geometry.translate(0, 0, extrudeSettings.depth*(k+4))
        mesh_material = THREE.MeshPhongMaterial.new(color)
        mesh_material.color = color
        mesh = THREE.Mesh.new(geometry, mesh_material)
        mesh.castShadow = True
        mesh.receiveShadow = False  
        meshesTop.append(mesh)
        linematerial = THREE.LineBasicMaterial.new( colorl )
        linematerial.color = colorl
        
        edgesout = THREE.EdgesGeometry.new( geometry )
        line = THREE.LineSegments.new( edgesout, linematerial )
        linesTop.append(line)
        
        global scene
        scene.add(line)
        scene.add(mesh)
    
    return meshesTop,linesTop

def generateShapeblock(xCordsArray,yCordsArray, color, colorl, xCordsHoles, yCordsHoles, array, floors, heightperfloor):##blockrandgeometry

    global scene
    
    extrudeSettings = {"steps" : 20,"depth" : 3.5,"bevelEnabled": False, "bevelSize": 0 }
    extrudeSettings["depth"] = heightperfloor
    extrudeSettings = Object.fromEntries(to_js(extrudeSettings ))
    
    
    linesB = []
    meshesB = []
    
    for k in range(floors):
        
        shape_permit = THREE.Shape.new()
    
        for i in range(len(xCordsArray)):
            if i == 0 :
                shape_permit.moveTo (xCordsArray[i], yCordsArray[i])
            else: 
                shape_permit.lineTo(xCordsArray[i], yCordsArray[i])  
        
        shape_hole = THREE.Shape.new()
        for i in range(len(xCordsHoles)):
            if i == 0 :
                shape_hole.moveTo (xCordsHoles[i], yCordsHoles[i])
            else: 
                shape_hole.lineTo(xCordsHoles[i], yCordsHoles[i])  
        
        shape_permit.holes.push(shape_hole)
        geometry = THREE.ExtrudeGeometry.new(shape_permit,extrudeSettings)
        geometry.translate(0, 0, extrudeSettings.depth*k)
        mesh_material = THREE.MeshPhongMaterial.new(color)
        mesh_material.color = color
        mesh = THREE.Mesh.new(geometry, mesh_material)
        meshesB.append(mesh)
        mesh.castShadow = True
        mesh.receiveShadow = False  
        
        edgesout = THREE.EdgesGeometry.new( geometry )
        linematerial = THREE.LineBasicMaterial.new( colorl )
        linematerial.color = colorl

        line = THREE.LineSegments.new( edgesout, linematerial )
        linesB.append(line)
        
        global scene
        scene.add(line)
        scene.add(mesh)
    
    
        for points in array:

            points = to_js(points)
        
            shape = THREE.Shape.new(points) 
        
            geometry2 = THREE.ExtrudeGeometry.new(shape,extrudeSettings)
            geometry2.translate(0, 0, extrudeSettings.depth*k)
            mesh_material = THREE.MeshPhongMaterial.new(color)
            mesh_material.lightMap
            # mesh_material.transparent = True
            # mesh_material.opacity = 0.8
            mesh_material.color = color
            mesh2 = THREE.Mesh.new(geometry2, mesh_material)
            meshesB.append(mesh2)
            mesh.castShadow = True
            mesh.receiveShadow = False  
            
            edges = THREE.EdgesGeometry.new( geometry2 )
            
            linematerial = THREE.LineBasicMaterial.new( colorl )
            linematerial.color = colorl

            line = THREE.LineSegments.new( edges, linematerial )
            
            linesB.append(line)
            
            scene.add( line )
            scene.add(mesh2)

    return meshesB, linesB


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#HELPER FUNCTIONS #Dont Touch, only if 100% sure mistake stems from here
def generateLinesNum(listpoints):
        listLines = []
        
        for i in range(len(listpoints)):
            if i < len(listpoints)-1:
                CurrentLine = [listpoints[i], listpoints[i+1]]
                listLines.append(CurrentLine)

            else:
                CurrentLine = [listpoints[i], listpoints[i-(len(listpoints)-1)]]
                listLines.append(CurrentLine)
        return listLines

def generateNumpyArray (plotboundaries):
    temp_list=[]
    Point_list=[]
    for i in plotboundaries:
        for k in i:

            temp_list.append(np.array(k))
        Point_list.append(temp_list)
        temp_list=[]
      
    SUB_SUB_NUMPY = [[np.array(k) for k in i] for i in plotboundaries]
    # print("biggerscale", SUB_SUB_NUMPY)
    
    return SUB_SUB_NUMPY

def generatexy (arraypoints):
    
    Xcoordinates = []
    Ycoordinates = []

    for m in range(len(arraypoints)):
        Xcoordinates.append(arraypoints[m][0])
        Ycoordinates.append(arraypoints[m][1])
    
    return Xcoordinates, Ycoordinates
     
def makeFloatfromPoint(xlist,ylist):
    fXlist = []
    fyList = []
    for fx in xlist:
        fXlist.append(float(fx))
    for fy in ylist:
        fyList.append(float(fy))
    return fXlist,fyList

def convert_result_check_W(x,y):
    BlockPermiter = []
    for k in range(len(x)): 
        BlockPermiter.append(np.array([x[k], y[k]]))
    return BlockPermiter

def convert_into_Points(x,y):
    BlockPermiter = []
    for k in range(len(x)): 
        BlockPermiter.append([x[k], y[k]])
    return BlockPermiter

def ListPoint2Lines(x,y):

    BlockPermiter = []
    for k in range(len(x)): 
        BlockPermiter.append(np.array([x[k], y[k]]))
        
    lines = []
    for h in range(len(BlockPermiter)):
        if h < len(BlockPermiter)-1:
            CurrentLine = [BlockPermiter[h], BlockPermiter[h+1]]
            lines.append(CurrentLine)

        else:
            CurrentLine = [BlockPermiter[h], BlockPermiter[h-(len(BlockPermiter)-1)]]
            lines.append(CurrentLine)
    return lines

def sort_dict(d, reverse = False):
  return dict(sorted(d.items(), key = lambda x: x[1]['Plotobject'].get_area(), reverse = reverse)) 

def numLinesToVec(ListStartEndpoint): 

        Currentoffset = []
        ListStartEndVec = []

    #offset Shape

        for i in ListStartEndpoint:
            for j in i:
                TempArrayToList = j.tolist()
                ThreeVec1 = THREE.Vector2.new(TempArrayToList[0],TempArrayToList[1])
                Currentoffset.append(ThreeVec1)
            ListStartEndVec.append (Currentoffset)
            Currentoffset = []
        return ListStartEndVec
        
def normalizeVec(x,y):

    distance = np.sqrt(x*x+y*y)
    return x/distance, y/distance

def isIntersectingWithoutEndpoints(intersectLinesAsNPList):
    if (np.all(intersectLinesAsNPList[0][0] == intersectLinesAsNPList[1][0]) or np.all(intersectLinesAsNPList[0][0] == intersectLinesAsNPList[1][1]) or 
    np.all(intersectLinesAsNPList[0][1] == intersectLinesAsNPList[1][0]) or np.all(intersectLinesAsNPList[0][1] == intersectLinesAsNPList[1][1])):
        return False
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y


    # Given three collinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    def onSegment(p, q, r):
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False

    def orientation(p, q, r):
    #Find point orientation
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):
            
            # Clockwise orientation
            return 1
        elif (val < 0):
            
            # Counterclockwise orientation
            return 2
        else:
            
            # Collinear orientation
            return 0

    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def doIntersect(p1,q1,p2,q2):
        
        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True

        # Special Cases

        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and onSegment(p1, p2, q1)):
            return True

        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and onSegment(p1, q2, q1)):
            return True

        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and onSegment(p2, p1, q2)):
            return True

        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and onSegment(p2, q1, q2)):
            return True

        # If none of the cases
        return False

    TempArrayToList = []
    tempArray1 = []
    for i in intersectLinesAsNPList:
        for j in i:
            tempArray1.append(j.tolist())
        TempArrayToList.append(tempArray1)
        tempArray1 = []

    
    p1 = Point(TempArrayToList[0][0][0],TempArrayToList[0][0][1])
    q1 = Point(TempArrayToList[0][1][0],TempArrayToList[0][1][1])
    p2 = Point(TempArrayToList[1][0][0],TempArrayToList[1][0][1])
    q2 = Point(TempArrayToList[1][1][0],TempArrayToList[1][1][1])
    
    if doIntersect(p1, q1, p2, q2):
        return True
    else:
        return False

def isSelfIntersect(polyVerticesAsNP):
    polyLines = []
    for i in range(len(polyVerticesAsNP)):  #Make the list of polygon vertices into a list of all polygon lines
        if i < len(polyVerticesAsNP)-1:
            CurrentLine = [polyVerticesAsNP[i], polyVerticesAsNP[i+1]]
            polyLines.append(CurrentLine)
        else:
            CurrentLine = [polyVerticesAsNP[i], polyVerticesAsNP[i-(len(polyVerticesAsNP)-1)]]
            polyLines.append(CurrentLine)
    for i in polyLines:
        for j in polyLines: #test if inputline runs through base shape (for every boundary line of base shape) despite endpoints beeing outside
            if all(np.array_equal(i[o], j[o]) for o in range(len(i))):
                continue
            testLines = [i,j]
            if isIntersectingWithoutEndpoints(testLines) == True:
                return True
    return False
             
def lengthBoundary(xcoord, ycoord):
    #print("xcoordoffset", xcoord)

    global LengthList
    LengthList = []

    for i in range(len(xcoord)-1):
        length = np.sqrt((xcoord[i]-xcoord[i+1])**2 + ((ycoord[i]-ycoord[i+1])**2))
        LengthList.append(length)
    
    return LengthList

def loop_check_angle(arraypoints):
    arraylines = generateLinesNum(arraypoints)
    
    
    for current_line in arraylines: 
        
        
        startline = current_line[0]
       
        next_line = current_line[1]
        
        angle = calculate_angle(startline, next_line)
    
        
        if math.degrees(angle) > 90:
            arraylines.pop(current_line[0])  
            # arraylines.remove(next_line) 
               
    
    #print ("arraylines", arraylines)
    return arraylines


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MOUS AND CLICKABILITY 
def transform_drag(event):
    event.preventDefault()

    if not event.value:
        update_Boundary()      

def update_Boundary(): 
    global len_coords, curve_object, Close_Bool,curve_material
    coords=[]
    for i in spheres:
        coords.append(i.position)
    len_coords = len(coords)
    #console.log("CHECK_IF WORKING:", coords)

    if Close_Bool == False:
        js_coords = to_js(coords)
        geometry = THREE.BufferGeometry.new()
        geometry.setFromPoints( js_coords )

        curve_object = THREE.Line.new( geometry, curve_material )

        scene.remove(curve_object)
        scene.add(curve_object)
        
    if Close_Bool == True:
        if len_coords == 2:
            js_coords = to_js(coords)
            geometry = THREE.BufferGeometry.new()
            geometry.setFromPoints( js_coords )
            curve_object = THREE.Line.new( geometry, curve_material )
            scene.remove(curve_object)
            scene.add(curve_object)
            Close_Bool = False
            


        elif len_coords>2:
            scene.remove(curve_object)

            js_coords = to_js(coords)
            geometry = THREE.BufferGeometry.new()
            geometry.setFromPoints( js_coords )

            curve_object = THREE.LineLoop.new( geometry, curve_material )
            
            scene.add(curve_object)
            global Boundary_status
            Boundary_status = "closed"

def update_road():
    global len_coords_road, curve_object_road,all_curve_object_road,curve_material, output_lists
    coords_road=[]
    output_lists= []
    for i in spheres_road:
        coords_road.append(i.position)
    len_coords_road = len(coords_road)

    if len_coords_road >= 2:
    
        output_lists = [coords_road[i:i+2] for i in range(0, len(coords_road), 2)]
        scene.remove(curve_object_road)
        for i in output_lists:
            js_coords = to_js(i)
            geometry = THREE.BufferGeometry.new()
            geometry.setFromPoints( js_coords )

            curve_object_road = THREE.Line.new( geometry, curve_material )
            all_curve_object_road.append(curve_object_road)
            scene.add(curve_object_road)

def toggle_Boundary_status():
    global Boundary_status, Close_Bool
    Boundary_status = "open"
    Close_Bool = False

def on_mouse_move(event):

    event.preventDefault()

    global raycaster, mouse, objects, preview_Sphere,clicked_sphere,object_clicked,Hover_over_Save


    mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( mouse, camera )

    js_objects = to_js(objects)
    intersects = raycaster.intersectObjects( js_objects, True )

    if intersects.length > 0 :
        if object_clicked == True:
            
            preview_Sphere.visible= True
            intersect = intersects[ 0 ]
            preview_Sphere.position.copy( intersect.point ).add( intersect.face.normal )
            
    mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )
    raycaster.setFromCamera( mouse, camera ) 
    js_objects = to_js(all_spheres)
    intersects = raycaster.intersectObjects( js_objects, True )
    if Saved== False:
        if intersects.length > 0 :
            intersect = intersects[ 0 ]
            Object = intersect.object
            
            
            Object_material = THREE.MeshPhongMaterial.new()
            Object_material.color = THREE.Color.new( "rgb(255,0,0)" )
            Object_material.transparent = True
            Object_material.opacity = 0.5
            Object.geometry = prev_sphere_geom
            Object.material = Object_material
            
                
            
            global Hover_over_Sphere
            Hover_over_Sphere=True
        

        else:
            for ball in all_spheres:
                ball.material = sphere_material
                ball.geometry = sphere_geom
            Hover_over_Sphere=False
        
    raycaster.setFromCamera( mouse, camera )
    intersects = raycaster.intersectObject(Save_Mesh , True )
    
    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        Hover_over_Save=True
    else:
        Hover_over_Save=False

def on_mouse_down(event):

    event.preventDefault()

    global raycaster, mouse, objects,clicked_sphere,object_clicked
    
    if object_clicked== False:
        mouse.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1)
        raycaster.setFromCamera(mouse, camera)
        js_objects = to_js(all_spheres)
        intersects = raycaster.intersectObjects(js_objects, True)
        if intersects.length > 0:
            if Saved== False:
                intersect = intersects[0]
                clicked_sphere = intersect.object
                object_clicked = True
                controls.enabled = False
    elif object_clicked==True:
        mouse.set((event.clientX / window.innerWidth) * 2 - 1, -(event.clientY / window.innerHeight) * 2 + 1)
        raycaster.setFromCamera(mouse, camera)
        intersects = raycaster.intersectObject(plane_Raycaster, True)
        if intersects.length > 0 and clicked_sphere is not None:
            intersect = intersects[0]
            clicked_sphere.position.copy(intersect.point).add(intersect.face.normal)
            clicked_sphere = None
            controls.enabled = True
            preview_Sphere.visible= False
            object_clicked = False
        
    scene.remove(curve_object)
    for x in all_curve_object_road:
        scene.remove(x)

    update_Boundary()
    update_road()

def on_mouse_up(event):
    pass

def on_dbl_click(event):
    event.preventDefault()
    global raycaster, mouse, objects, sphere_geom, sphere_material,Close_Bool, spheres,spheres_road,all_spheres, Saved, Hover_over_Save, output_lists,Input_Road_Coords_py,Boundary_Coords_py,count_Mainstreet,count_Substreet,count_Usage
    

    mouse.set( ( event.clientX / window.innerWidth ) * 2 - 1, - ( event.clientY / window.innerHeight ) * 2 + 1 )

    raycaster.setFromCamera( mouse, camera )

    intersects = raycaster.intersectObject( plane_Raycaster, True )
    
    if intersects.length > 0 :
        intersect = intersects[ 0 ]
        ball = THREE.Mesh.new( sphere_geom, sphere_material )
        ball.position.copy( intersect.point ).add( intersect.face.normal )
        ball2 = THREE.Mesh.new( sphere_geom, sphere_material )
        ball2.position.copy( intersect.point ).add( intersect.face.normal )
        if Hover_over_Save == False:
            if Hover_over_Sphere==False and Boundary_status == "open" and Saved == False:
                spheres.append(ball)
                scene.add(ball)
            
                objects.append(ball)
            if Hover_over_Sphere==True:
                Close_Bool = True
            if Hover_over_Sphere==False and Close_Bool == True and Saved == False:
                scene.add(ball2)
                spheres_road.append(ball2)
                update_road()
            

    all_spheres = spheres + spheres_road
    raycaster.setFromCamera( mouse, camera )

    intersects = raycaster.intersectObject(Reset_Mesh , True )
    ###RESET
    if intersects.length > 0 :
        sphere_material.color = THREE.Color.new( "rgb(255,0,0)" )
        curve_material.color = THREE.Color.new("rgb(255,0,0)")
        count_Mainstreet = 0
        count_Substreet = 0
        count_Usage = 0
        Saved=False
        scene.clear()
        spheres = []
        spheres_road =[]
        objects =[]
        objects.append(plane_Raycaster)
        #scene.add(grid_helper)
        scene.add(Reset_Mesh)
        scene.add(Save_Mesh)
        scene.add(light)
        scene.add(light2)
        scene.add(preview_Sphere)
        scene.add( plane_map )
        toggle_Boundary_status()
        Boundary_Coords = []
        Boundary_Coords_py = []

        Input_Road_Coords = []
        Input_Road_Coords_py = []
    #save the current state and lock "editor"
    raycaster.setFromCamera( mouse, camera )
    intersects = raycaster.intersectObject(Save_Mesh , True )
    
    if intersects.length > 0 :
        Saved=True
        Boundary_Coords = []
        Boundary_Coords_py = []
        Input_Road_Coords = []
        Input_Road_Coords_py = []
        Input_Road_Coords_js = []


        #Transform Js Vectors to coords for Boundary
        for i in spheres:
            Js_prox = to_js(i.position)
            Boundary_Coords.append(Js_prox)
        for k in Boundary_Coords:
            
            X_val =k.getComponent(0)
            X_val=round(X_val, 2)
            Y_val =k.getComponent(1)
            Y_val=round(Y_val, 2)
            temp_array=np.array([X_val,Y_val])
            
            #Z_val = k.getComponent(2)
            # Z_val=round(Z_val, 7)
            # temp_list.append(Z_val)
            Boundary_Coords_py.append(temp_array)
    
        for l in output_lists: 
            Input_Road_Coords_temp =[]
 
            for m in l:
                
                X_val =m.getComponent(0)
                X_val=round(X_val, 2)
                Y_val =m.getComponent(1)
                Y_val=round(Y_val, 2)
                temp_array=np.array([X_val,Y_val])
                
                # Z_val = m.getComponent(2)
                # Z_val=round(Z_val, 7)
                # temp_list.append(Z_val)
                Input_Road_Coords_temp.append(temp_array)
            Input_Road_Coords_py.append(Input_Road_Coords_temp)
        for sphere in spheres:
            scene.remove(sphere)
        for sphere_road in spheres_road:
            scene.remove(sphere_road)
        sphere_material.color = THREE.Color.new( "rgb(80,80,80)" )
        curve_material.color = THREE.Color.new("rgb(100,100,100)")
       
        console.log("Boundary_COORDS", Boundary_Coords_py)
      
        console.log("Road_COORDS", Input_Road_Coords_py)
      
    scene.remove(curve_object)
    scene.remove(curve_object_road)
    update_Boundary()
    update_road()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#FIND PLOTS AND ASSIGN
def determine_loop_direction(points):
    n = len(points)
    x = [p[0] for p in points]
    y = [p[1] for p in points]
    a = sum(x[i]*y[(i+1)%n] - x[(i+1)%n]*y[i] for i in range(n))
    return "Counterclockwise" if a > 0 else "Clockwise"
##########################################################################################
def calculate_angle(line1, line2):
    x1, y1 = line1[1][0] - line1[0][0], line1[1][1] - line1[0][1]
    x2, y2 = line2[1][0] - line2[0][0], line2[1][1] - line2[0][1]
    return math.atan2(x1*y2 - y1*x2, x1*x2 + y1*y2)
##########################################################################################
def sharpest_right_turn(angles):
    
    angles_in_radians = [math.radians(angle) for angle in angles]
    right_turn_angles = []
    for i in range(len(angles_in_radians)):
        right_turn_angles.append(angles_in_radians[i])
    max_turn_index = right_turn_angles.index(min(right_turn_angles))
    return max_turn_index
##########################################################################################
def loop_finder(INPUT_LINES):

    """
    Given a list of lines represented as pairs of points, this function finds all loops in the lines.
    A loop is defined as a series of lines where the endpoint of one line is the startpoint of the next line, and the endpoint of the last line is the startpoint of the first line.
    The function returns a list of loops, with each loop represented as a list of points in the order they are encountered in the loop.
    :param INPUT_LINES: list of lines represented as pairs of points
    :return: list of loops, each represented as a list of points
    """
    Loops=[]
    
    for current_line in INPUT_LINES: 
        Loop=[]
        Loop.append(current_line[0])
        Loop.append(current_line[1])

        connecting_lines=[]
        flipped_connector=[]
        # line is  a connecting line, but not itself
        
        for line in INPUT_LINES:
            if line [0] == current_line[1] and line != current_line:
                connecting_lines.append(line)
            if line [1] == current_line[1] and line != current_line:
                flipped_connector=[]
                flipped_connector.append(line[1])
                flipped_connector.append(line[0])
                connecting_lines.append(flipped_connector)
            
        

        if len(connecting_lines) >=1:
            connecting_angles = []
            for neigbhor in connecting_lines:
                angle = calculate_angle(current_line, neigbhor)           
                connecting_angles.append(math.degrees(angle))
            next_line_index= sharpest_right_turn(connecting_angles)
            next_line = connecting_lines[next_line_index]
            Loop.append(next_line[1])
        
        while Loop[-1] != Loop[0]:
            
            Next_connecting_lines=[]
            for line in INPUT_LINES:  
                if line == next_line or line[1] == next_line[0] and line[0] == next_line[1]:
                    pass
                else:
                    if line [0] == Loop[-1] :
                            Next_connecting_lines.append(line)
                    
                    if line [1] == Loop[-1] :
                            flipped_connector=[]
                            flipped_connector.append(line[1])
                            flipped_connector.append(line[0])
                            Next_connecting_lines.append(flipped_connector)

            
            if len(Next_connecting_lines) >=1:
                next_connecting_angles =[]
                for next_neigbhor in Next_connecting_lines:
                    angle = calculate_angle(next_line, next_neigbhor)           
                    next_connecting_angles.append(math.degrees(angle))
                next_line_index= sharpest_right_turn(next_connecting_angles)
                next_line = Next_connecting_lines[next_line_index]
                Loop.append(next_line[1])
                if Loop.count(next_line[1]) == 2:
                    break
            else:
                Loop=[]
                break
        if len(Loop) >=1:    
            Loop.pop(-1)   #delete double coordinate

        direction = determine_loop_direction(Loop)
        if direction== "Clockwise":
            if len(Loop) >=1:  
                Loops.append(Loop)
        if direction== "Counterclockwise":
            Loop=[]
            FlippedStart=[]
            FlippedStart.append(current_line[1])
            FlippedStart.append(current_line[0])
            INPUT_LINES.append(FlippedStart)
            
    new_loops = []
    for sublist in Loops:
        is_duplicate = False
        for other_sublist in new_loops:
            if set(map(tuple,sublist)) <= set(map(tuple,other_sublist)):
                is_duplicate = True
                break
        if not is_duplicate:
            new_loops.append(sublist)
    Loops = new_loops              #Loops is now the cleaned up version of itself




    return Loops
##########################################################################################
def find_overlapping_plots(plots):
    # Create a dictionary to store the mapping from plot number to overlapping plots
    plot_overlaps = {}
    # Iterate over each plot
    for i, plot in enumerate(plots):
        # Initialize an empty list to store the overlapping plots for this plot
        overlaps = []
        # Iterate over the other plots
        for j, other_plot in enumerate(plots):
            # Skip the current plot
            if i == j:
                continue
            # Check if the current plot has 2 or more coordinates in common with the other plot
            common_coords = set(plot).intersection(set(other_plot))
            if len(common_coords) >= 2:
                overlaps.append(j)
        # Add the mapping from plot number to overlapping plots to the dictionary
        plot_overlaps[i] = overlaps
    # Create a list of tuples (plot number, overlapping plots) from the dictionary
    result = [(plot, overlaps) for plot, overlaps in plot_overlaps.items()]
    return result
##########################################################################################
def convert_data(list_neighbours: list[list[int, list[int]]]) -> dict:
    """
    Converts the data from a list to a dictionary.
    """
    # Initialize the dictionary
    dictionary = {}

    # Loop through the plots
    for plot, neighbours in list_neighbours:

        # Add the plot to the dictionary
        dictionary[plot] = {'value': None, 'neighbours': neighbours}
    return dictionary
##########################################################################################
def random_distribution(dictionary: dict) -> dict:
    global PLOTS
    """
    Randomly assign a value to each plot and checks if the rules are
    respected.
    """
    # Declare the possible values
    weights=[]
    modified_val_l = 110-input_param.LivingIndustrial
    weights.append(modified_val_l)
    modified_val_i = input_param.LivingIndustrial
    weights.append(modified_val_i)
    modified_val_g = (110-input_param.LivingIndustrial+55)/2
    weights.append(modified_val_g)
    modified_val_o = (input_param.LivingIndustrial+55)/2
    if modified_val_o<55:
        modified_val_o=modified_val_o/2 
    weights.append(modified_val_o)
    modified_val_e = 100
    weights.append(modified_val_e)
    
    values = ['L', 'I', 'G', 'O', 'E']
    #weights = [20, 20, 20, 20, 20]
    L_Count=0
    I_Count=0
    G_Count=0
    O_Count=0
    E_Count=0
    
    # Get the first plot in the dictionary
    first_plot = list(dictionary.keys())[0]

    # Choose a random value from the list of possible values
    value = choice(['L', 'I', 'G', 'O', 'E'])
    VALID_VALUES=[]
    # Assign the random value to the first plot and change possible Neighbor Values accordingly
    dictionary[first_plot]['value'] = value
    combined_plots = {}
    for neighbor in dictionary[first_plot]['neighbours']:
        if dictionary[first_plot]['value'] == 'L':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
        elif dictionary[first_plot]['value'] == 'I':
            while "L" in values:
                index= values.index("L")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
            while "E" in values:
                index= values.index("E")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        #elif dictionary[first_plot]['value'] == 'G':
            # while "G" in values:
            #     index= values.index("G")
            #     if index < len(values):
            #         values.pop(index)
            #         weights.pop(index)
        if L_Count >= 4:
            while "L" in values:
                index= values.index("L")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if I_Count >= 4:
            while "I" in values:
                index= values.index("I")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if G_Count >= 4:
            while "G" in values:
                index= values.index("G")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if O_Count >= 4:
            while "O" in values:
                index= values.index("O")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)
        if E_Count >= input_param.population//3000:
            while "E" in values:
                index= values.index("E")
                if index < len(values):
                    values.pop(index)
                    weights.pop(index)

        
        
        valid_vals= ([neighbor],values,weights)
        VALID_VALUES.append(valid_vals)
    VALID_VALUES_NO_DOUBLES = []
        
            
    visited=[0]

    if value=="L":
        L_Count=L_Count+1                    
        
    elif value=="I":
        I_Count=I_Count+1
        
    elif value=="G":
        G_Count=G_Count+1
        
    elif value=="O":
        O_Count=O_Count+1
        
    elif value=="E":
        E_Count=E_Count+1
    
    
    for i in VALID_VALUES:
                if i not in VALID_VALUES_NO_DOUBLES:
                    VALID_VALUES_NO_DOUBLES.append(i)
    for plot in VALID_VALUES_NO_DOUBLES:
            plot_num, possible_values, weights = plot
            plot_num = plot_num[0]
            indices = range(len(possible_values))
            if plot_num in combined_plots:
                current_values, current_weights= combined_plots[plot_num]
                combined_values = set(current_values) & set(possible_values)
                combined_indices = [i for i in indices if possible_values[i] in combined_values]
                combined_weights = [weights[i] for i in combined_indices]
                combined_plots[plot_num] = (list(combined_values), combined_weights)
            else:
                combined_plots[plot_num] = (possible_values, weights)
    combined_plots = {key: value for key, value in combined_plots.items() if key not in visited}
    sorted_dict = dict(sorted(combined_plots.items(), key=lambda x: len(x[1][0])))
    
    # Assign the value to the plot
    # dictionary[neighbor]['value'] = value

    values = ['L', 'I', 'G', 'O', 'E']
    # Declare the possible values
    weights=[]
    modified_val_l = 110-input_param.LivingIndustrial
    weights.append(modified_val_l)
    modified_val_i = input_param.LivingIndustrial
    weights.append(modified_val_i)
    modified_val_g = (110-input_param.LivingIndustrial+55)/2
    weights.append(modified_val_g)
    modified_val_o = (input_param.LivingIndustrial+55)/2
    if modified_val_o<55:
        modified_val_o=modified_val_o/2 
    weights.append(modified_val_o)
    modified_val_e = 100
    weights.append(modified_val_e)
    #weights = [20, 20, 20, 20, 20]
        
    

    # Loop through the plots
    while combined_plots != {}:
        for plot in sorted_dict:
            if plot>0:
                visited.append(plot)
                
                # Check the values of the neighbors
                for neighbor in dictionary[plot]['neighbours']:
                    # if dictionary[neighbor]['value'] == 'G':
                    #     while "G" in values:
                    #         index= values.index("G")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    # elif dictionary[neighbor]['value'] == 'C':
                    #     while "I" in values:
                    #         index= values.index("I")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    if dictionary[neighbor]['value'] == 'L':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    elif dictionary[neighbor]['value'] == 'I':
                        while "L" in values:
                            index= values.index("L")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                        # while "C" in values:
                        #     index= values.index("C")
                        #     if index < len(values):
                        #         values.pop(index)
                        #         weights.pop(index)
                        # while "P" in values:
                        #     index= values.index("P")
                        #     if index < len(values):
                        #         values.pop(index)
                        #         weights.pop(index)
                    elif dictionary[neighbor]['value'] == 'E':
                        while "I" in values:
                            index= values.index("I")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                    # if L_Count >= 4:
                    #     while "L" in values:
                    #         index= values.index("L")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    # if I_Count >= 4:
                    #     while "C" in values:
                    #         index= values.index("I")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    # if G_Count >= 4:
                    #     while "G" in values:
                    #         index= values.index("G")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    # if O_Count >= 4:
                    #     while "O" in values:
                    #         index= values.index("O")
                    #         if index < len(values):
                    #             values.pop(index)
                    #             weights.pop(index)
                    if E_Count >= len(PLOTS)//30:
                        while "E" in values:
                            index= values.index("E")
                            if index < len(values):
                                values.pop(index)
                                weights.pop(index)
                
                    
                    valid_vals= ([neighbor],values,weights)
                    VALID_VALUES.append(valid_vals)

            # Assign a value to the plot, using weighted probability
            if(len(values))>=1:
                value = choices(values, weights=weights, k=1)[0]
                
                # Assign the value to the plot
                dictionary[plot]['value'] = value
                

            else:
                for plot in dictionary.keys():
                    # Set the value to None
                    
                    dictionary[plot]['value'] = None
                return False 
            
            for i in VALID_VALUES: ###################################################### List operations for combining different possibilities when checking from a different neigbor
                    if i not in VALID_VALUES_NO_DOUBLES:
                        VALID_VALUES_NO_DOUBLES.append(i)
            for plot in VALID_VALUES_NO_DOUBLES:
                    plot_num, possible_values, weights = plot
                    plot_num = plot_num[0]
                    indices = range(len(possible_values))
                    if plot_num in combined_plots:
                        current_values, current_weights= combined_plots[plot_num]
                        combined_values = set(current_values) & set(possible_values)
                        combined_indices = [i for i in indices if possible_values[i] in combined_values]
                        combined_weights = [weights[i] for i in combined_indices]
                        combined_plots[plot_num] = (list(combined_values), combined_weights)
                    else:
                        combined_plots[plot_num] = (possible_values, weights)
            values = ['L', 'I', 'G', 'O', 'E']    ##############################reset weights and Values
            # Declare the possible values
            weights=[]
            modified_val_l = 110-input_param.LivingIndustrial
            weights.append(modified_val_l)
            modified_val_i = input_param.LivingIndustrial
            weights.append(modified_val_i)
            modified_val_g = (110-input_param.LivingIndustrial+55)/2
            weights.append(modified_val_g)
            modified_val_o = (input_param.LivingIndustrial+55)/2
            if modified_val_o<55:
                modified_val_o=modified_val_o/2    
            weights.append(modified_val_o)
            modified_val_e = 100
            weights.append(modified_val_e)
                    
            #weights = [20, 20, 20, 20, 20]
                    
            combined_plots_all = {key: value for key, value in combined_plots.items()}################################# A list with all possible values for all Plots
            sorted_dict_all = dict(sorted(combined_plots_all.items(), key=lambda x: len(x[1][0])))
            #print("Options_if_changes_neccessary:",sorted_dict_all)       
            
            combined_plots = {key: value for key, value in combined_plots.items() if key not in visited}############### A list with all possible values for all Plots that havnt been assigned yet
            sorted_dict = dict(sorted(combined_plots.items(), key=lambda x: len(x[1][0])))
            
            ############### Count the assignment Values
            if value=="L":  
                L_Count=L_Count+1                    
                
            elif value=="I":
                I_Count=I_Count+1
                
            elif value=="G":
                G_Count=G_Count+1
                
            elif value=="O":
                O_Count=O_Count+1
                
            elif value=="E":
                E_Count=E_Count+1
   
    # print("LCount",L_Count)
    # print("ICount",I_Count)  
    # print("GCount",G_Count)  
    # print("OCount",O_Count)  
    # print("ECount",E_Count)
    return dictionary
##########################################################################################
def find_solution(dictionary: dict,
                max_time: float = 30) -> dict:
    """
    Generates solutions until a valid one is found or the time limit.
    is reached.
    """
    # Initialize the answer and the time
    answer, start = {}, time()

    # Set the stopping condition
    while answer == {} and (time() - start) < max_time:

        # Get a potential solution
        answer = random_distribution(dictionary)

    if answer == False:
        find_solution(dictionary,5)
    else:
        return answer

##########################################################################################
def polygonDivider(inputPolygonsAsNp,minSize = 0, maxSize = 250000, H_or_V = 1, mustHaveStreetConnection = False,streetToConnectToAsNPVertices = [], randomizeH_V = False, force_H = False, force_V = False,min_compactness = 0.2, finishedPolygons = [],percentageOfCut = 50, count = 0, turnCount = 0):
    #Explanation of polygon input:
    #InputPolygonsAsNp: The Polygon you want to subdivide. Geometry should be displayed as a list with the vertices of the polygon in it in the form of np-vectors
    #minSize: The minimal size a generated plot is allowed to have
    #maxSize: the maximal size a generated plot is allowed to have (not guaranteed to always be smaller than this)
    #H_or_V: You can, but don't have to, decide wether to start by slicing horizontally or Vertically, 0: Slizes Vertical, 1: Slizes horizontal
    #MustHaveStreetConnection: True or False, decides wether all newly generated plots have to share a side with the initial polygon
    #streetToConnectToAsNPVertices: MANDATORY to include if MustHaveStreetConnection is = True! The Initial Polygon that all newly created polygons are supposed to share an edge with
    #randomizeH_V: Put True to let the function randomize with each iteration if the polygons are slized vertically or horizontally
    #Force_H/Force_V: Forces the desired direction, no other direction will be used for the split
    #min_compactness: number between 0-1 that defines the required compactness of the generated Plots. NOT IMPLEMENTED YET
    

    if len(inputPolygonsAsNp) == 0:
        return finishedPolygons
    if type(inputPolygonsAsNp[0]) != list:      #Unify data-structure
        inputPolygonsAsNp = [inputPolygonsAsNp.copy()]
    H_or_V += 1

    if force_V == True:     #Create Possibility to force algorhythm to only cut in one direction
        cutDir = "V"
    elif force_H == True:
        cutDir = "H"
    elif randomizeH_V == True:
        numb = random.randint(0,1)
        if numb == 0:
            cutDir = "V"
        else:
            cutDir = "H"
    elif H_or_V % 2:
        cutDir = "V"
    else:
        cutDir = "H"

    if count > 10:       #if algorythm tries too often it stops automatically
        return inputPolygonsAsNp

    currentFinishedPolys = []
    for i in finishedPolygons:
        currentFinishedPolys.append(i)
    
    currentPoly = []
    for i in inputPolygonsAsNp:
        currentPoly.append(i)

    
    for i in range(len(currentPoly)):   #   For every "open" polygon that still needs processing
        
        
        splitPoly = polygonSplit(currentPoly[i],cutDir,percentageOfCut)
        newLeftPolys = splitPoly[0]
        newRightPolys = splitPoly[1]
        leftArea = []
        rightArea = []
        for j in newLeftPolys:
            area = Area(j)
            if area > maxSize:
                leftArea.append("Too Big")
                continue
            elif area < minSize:
                leftArea.append("Too Small")
                continue
            else:
                leftArea.append("Right")

        for j in newRightPolys:
            area = Area(j)
            if area > maxSize:
                rightArea.append("Too Big")
                continue
            elif area < minSize:
                rightArea.append( "Too Small")
                continue
            else:
                rightArea.append("Right")
        leftCompactness = []
        rightCompactness = []
        for k in newLeftPolys:
            perimeter = 0
            polygonLines = []
            for c in range(len(k)):   #Convert Polygon to lines
                if c < len(k)-1:
                    CurrentLine = [k[c], k[c+1]]
                    polygonLines.append(CurrentLine)
                else:
                    CurrentLine = [k[c], k[c-(len(k)-1)]]
                    polygonLines.append(CurrentLine)
            for s in polygonLines:
                perimeter += np.linalg.norm(s[1]-s[0])
            compactness = 4 * np.pi * Area(k) / perimeter ** 2
            if compactness >= min_compactness:
                leftCompactness.append(True)
            else:
                leftCompactness.append(False)

        for k in newRightPolys:
            perimeter = 0
            polygonLines = []
            for c in range(len(k)):   #Convert Polygon to lines
                if c < len(k)-1:
                    CurrentLine = [k[c], k[c+1]]
                    polygonLines.append(CurrentLine)
                else:
                    CurrentLine = [k[c], k[c-(len(k)-1)]]
                    polygonLines.append(CurrentLine)
            for s in polygonLines:
                perimeter += np.linalg.norm(s[1]-s[0])
            compactness = 4 * np.pi * Area(k) / perimeter ** 2
            if compactness >= min_compactness:
                rightCompactness.append(True)
            else:
                rightCompactness.append(False)

        if any(leftCompactness) == False or any(rightCompactness) == False:
            if turnCount == 0 or turnCount % 2 == 0:
                if cutDir == "H":
                    turnCount += 1  
                    return polygonDivider(currentPoly, minSize, maxSize, 1, mustHaveStreetConnection ,streetToConnectToAsNPVertices , False , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                else:
                    turnCount += 1  
                    return polygonDivider(currentPoly, minSize, maxSize, 2, mustHaveStreetConnection ,streetToConnectToAsNPVertices , False , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
            

        if mustHaveStreetConnection == True:        #If required checks if new polygons connect to streets

            if any(y == "Too Small" for y in leftArea) and any(y == "Too Small" for y in rightArea): #Dividing the Polygon return areas too small, mark undivided polygon as finished
                turnCount = 0
                count = 0
                currentFinishedPolys.append(currentPoly[i])
                currentPoly.pop(i)
                return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)

            connectStreetLines = []
            for c in range(len(streetToConnectToAsNPVertices)):   #Convert Polygon to lines
                if c < len(streetToConnectToAsNPVertices)-1:
                    CurrentLine = [streetToConnectToAsNPVertices[c], streetToConnectToAsNPVertices[c+1]]
                    connectStreetLines.append(CurrentLine)
                else:
                    CurrentLine = [streetToConnectToAsNPVertices[c], streetToConnectToAsNPVertices[c-(len(streetToConnectToAsNPVertices)-1)]]
                    connectStreetLines.append(CurrentLine)
            streetConLeft = []
            streetConRight = []

            for k in newLeftPolys:  #check if Left Polygon(s) connect to street
                tempOnline = 0
                for y in k:
                    if pointOnPolygon(y,connectStreetLines) == True:
                        tempOnline += 1
                if tempOnline >= 2:
                    streetConLeft.append(True)
                else:
                    streetConLeft.append(False)
 
            for k in newRightPolys:     #check if Right Polygon(s) connect to street
                tempOnline = 0
                for y in k:
                    if pointOnPolygon(y,connectStreetLines) == True:
                        tempOnline += 1
                if tempOnline >= 2:
                    streetConRight.append(True)
                else:
                    streetConRight.append(False)
            
            if all(streetConLeft) == False and all(streetConRight) == False:        #Further divison of current polygon not possible, mark undivided polygon as finished
                turnCount = 0
                count = 0
                currentFinishedPolys.append(currentPoly[i])
                currentPoly.pop(i)
                return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)

            elif any(streetConLeft) == False or any(streetConRight) == False:
                if count <=5:
                    count += 1
                    if turnCount == 0 or turnCount % 2 == 0:
                        if cutDir == "H":
                            turnCount += 1  
                            return polygonDivider(currentPoly, minSize, maxSize, 1, mustHaveStreetConnection ,streetToConnectToAsNPVertices , False , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                        else:
                            turnCount += 1  
                            return polygonDivider(currentPoly, minSize, maxSize, 2, mustHaveStreetConnection ,streetToConnectToAsNPVertices , False , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                        
                    else:
                        turnCount = 0
                        count = 0
                        currentFinishedPolys.append(currentPoly[i])
                        currentPoly.pop(i)
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                else:
                    turnCount = 0
                    count = 0
                    currentFinishedPolys.append(currentPoly[i])
                    currentPoly.pop(i)
                    return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                
            elif all(streetConLeft) == True and all(streetConRight) == True:        #Condition met: All New Polygons have street-access
                if all(y == "Right" for y in leftArea) and all(y == "Right" for y in rightArea):    #Perfectly finishes: Area is correct and Plots connect to streets
                    for x in newLeftPolys:
                       
                        currentFinishedPolys.append(x)
                    for x in newRightPolys:
                       
                        currentFinishedPolys.append(x)
                    count = 0
                    turnCount = 0
                    currentPoly.pop(i)
                    return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                elif  all(y == "Too Big" for y in leftArea) and all(y == "Too Big" for y in rightArea):       #Both sides Valid, but have to be divided further
                    if count <= 5:
                        currentPoly.pop(i)
                        for x in newRightPolys:
                            currentPoly.insert(0, x)
                        for x in newLeftPolys:
                            currentPoly.insert(0, x)
                        count += 1
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                    else:
                        turnCount = 0
                        count = 0
                        currentFinishedPolys.append(currentPoly[i])
                        currentPoly.pop(i)
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)

                elif all(y == "Too Small" for y in leftArea) == False and any(y == "Too Small" for y in rightArea) == False:  #Two sides are not all perfect, but none is too small
                    if count <= 5:
                        for z in range(len(newLeftPolys)):
                            if leftArea[z] == "Right":
                                currentFinishedPolys.append(newLeftPolys[z])
                                del newLeftPolys[z]
                        for z in range(len(newRightPolys)):
                            if rightArea[z] == "Right":
                                currentFinishedPolys.append(newRightPolys[z])
                                del newRightPolys[z]
                        currentPoly.pop(i)
                        for x in newRightPolys:
                            currentPoly.insert(0, x)
                        for x in newLeftPolys:
                            currentPoly.insert(0, x)
                        count += 1
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)
                    else:
                        turnCount = 0
                        count = 0
                        currentFinishedPolys.append(currentPoly[i])
                        currentPoly.pop(i)
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)

                elif  any(y == "Too Small" for y in leftArea) == False and any(y == "Too Small" for y in rightArea):
                    
                    if count <= 5:
                        count += 1
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut-(percentageOfCut/2) , count , turnCount)
                    else:
                        turnCount = 0
                        count = 0
                        currentFinishedPolys.append(currentPoly[i])
                        currentPoly.pop(i)
                        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)

                elif  any(y == "Too Small" for y in leftArea) and any(y == "Too Small" for y in rightArea) == False:
                    try:
                        if count <= 5:
                            count += 1
                            return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut + ((100-percentageOfCut) / 2) , count , turnCount)
                        else:
                            turnCount = 0
                            count = 0
                            currentFinishedPolys.append(currentPoly[i])
                            currentPoly.pop(i)
                            return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut, count , turnCount)
                    except:
                        pass
                        


        count += 1
        return polygonDivider(currentPoly, minSize, maxSize, H_or_V, mustHaveStreetConnection ,streetToConnectToAsNPVertices , randomizeH_V , force_H , force_V ,min_compactness , currentFinishedPolys,percentageOfCut , count , turnCount)

def NumpyArea(verticesAsNP):

    n = len(verticesAsNP) # of verticesAsNP
    area = 0

    for i in range(n):
        j = (i + 1) % n
        area += (verticesAsNP[i][0] * verticesAsNP[j][1])
        area -= (verticesAsNP[j][0] * verticesAsNP[i][1])
    area = abs(area)/2.0

    return area

def arrayIndex(arrayList,searchedArray):
    for i in range(len(arrayList)):
        if np.all(searchedArray == arrayList[i]):
            return i

def minimalBoundingBox(pointsOfPolyAsNP): #Find the minimum bounding box for an polygon, Output is always clockwise! (at least never encountered different)
    
    pointsOfPoly = []
    for i in pointsOfPolyAsNP:
        TempArrayToList = i.tolist()
        pointsOfPoly.append (TempArrayToList)
    
    min_bounding_box_geom = geometry.Polygon(pointsOfPoly).minimum_rotated_rectangle
    min_bounding_box = min_bounding_box_geom.exterior.coords[:-1]
    #Child: "Dad, what rhymes on orange?" 
    # ... 
    #Dad: "No it doesn't"
    min_bounding_boxAsNP = []
    for i in min_bounding_box:
        min_bounding_boxAsNP.append(np.array([i[0],i[1]]))
    return min_bounding_boxAsNP


def Offset_Shapely(points,offset,ccw):
    
    if ccw == -1:
        side_var="right"
    else: side_var="left"
    poly_line = LinearRing(points)
    poly_line_offset = poly_line.parallel_offset(offset, side=side_var, resolution=16, join_style=2, mitre_limit=1)
    poly_line_offset_np = np.array([np.array([c[0], c[1]]) for c in poly_line_offset.coords])
    poly_line_offset_np = [np.array(i) for i in poly_line_offset_np]
  
    return poly_line_offset_np

def offsetNpPoly(points, offset, outer_ccw = 1):
    oldX = []
    oldY = []
    
    pointsrounded = []
    for k in points:
        pointsrounded.append(k.round(7))        
    
    for i in pointsrounded:
        point = i.tolist()
        oldX.append(point[0])
        oldY.append(point[1])
    
    num_points = len(oldX)
    oldNewPoints = []

    for indexpoint in range(num_points):
        prev = (indexpoint + num_points -1 ) % num_points
        next = (indexpoint + 1) % num_points
        vnX =  oldX[next] - oldX[indexpoint]
        vnY =  oldY[next] - oldY[indexpoint]
        vnnX, vnnY = normalizeVec(vnX,vnY)
        nnnX = vnnY
        nnnY = -vnnX
        vpX =  oldX[indexpoint] - oldX[prev]
        vpY =  oldY[indexpoint] - oldY[prev]
        vpnX, vpnY = normalizeVec(vpX,vpY)
        npnX = vpnY * outer_ccw
        npnY = -vpnX * outer_ccw
        bisX = (nnnX + npnX) * outer_ccw
        bisY = (nnnY + npnY) * outer_ccw
        bisnX, bisnY = normalizeVec(bisX,  bisY)
        bislen = offset /  np.sqrt((1 + nnnX*npnX + nnnY*npnY)/2)

        oldNewPoints.append(np.array([oldX[indexpoint] + bislen * bisnX, oldY[indexpoint] + bislen * bisnY]))
            
    def crossingLineKicker(points,lennewPoints):
        newPoints = points.copy()
        for i in range(lennewPoints):
            if lennewPoints < 4:
                return newPoints
            
            
            line1 = [newPoints[i % lennewPoints],newPoints[(i+1) % lennewPoints]]
            line2 = [newPoints[(i+2) % lennewPoints],newPoints[(i+3) % lennewPoints]]
            if isIntersecting([line1,line2]) == True:
                intersectPt = getIntersectPoint([line1,line2])
                if type(intersectPt) is not np.ndarray:   
                    return newPoints
                newPoints.pop((i+2) % lennewPoints)
                lennewPoints = len(newPoints)
                newPoints.pop((i+1) % lennewPoints)
                lennewPoints = len(newPoints)
                newPoints.insert((i+1) % lennewPoints,intersectPt)
                lennewPoints = len(newPoints)
                return crossingLineKicker(newPoints,len(newPoints))
                
        return newPoints
    
    newPoints = points.copy()
    if len(oldNewPoints)>= 4:
        newPoints = crossingLineKicker(oldNewPoints,len(oldNewPoints))         
    return newPoints


def arrangePolygonPieces(listOfPiecesAsNP, counter = 0):
    loops = []
    for i in listOfPiecesAsNP:
        if len(loops) == 0:
            loops.append(i)
            continue
        appended = False
        for k in loops:
            if np.all(i[0] == k[-1]):
                for f in i:
                    k.append(f)
                    appended = True
            if appended == True:
                break
        if appended == False:
            loops.append(i)
    newLoops = []
    if all(np.all(i[0] == i[-1]) for i in loops) or counter > 5:
        for t in loops:
            singleLoop = []
            for j in t:
                if len(singleLoop) == 0:
                    singleLoop.append(j)
                elif any(np.all(j == x) for x in singleLoop) == False:
                    singleLoop.append(j)
            newLoops.append(singleLoop)
        return newLoops
    else:
        counter =+1
        return arrangePolygonPieces(loops, counter)


def polygonSplit(unidirectionalPolygonAsNp,cuttingDir_H_or_V,percentageOfCut):   #Input can be whatever way, function works with counterclockwise polygons though! (returns Clockwise)
    
    if determine_loop_direction(unidirectionalPolygonAsNp) == "Clockwise":
        streetToConnectToAsNPVertices = []
        for i in range(len(unidirectionalPolygonAsNp)):      #Make Polygon Counter-clockwise... there was confusion about which direction we work with, too much work to change now, i'm sorry Zuardin (Or anyone else for that matter)
            streetToConnectToAsNPVertices.append(unidirectionalPolygonAsNp[len(unidirectionalPolygonAsNp)-(i+1)])
    else:
        streetToConnectToAsNPVertices = unidirectionalPolygonAsNp.copy()
    bbo = minimalBoundingBox(streetToConnectToAsNPVertices)
    bb = offsetNpPoly(bbo,0.001,1)#Offset Bounding Box ever so slightly larger outwards to prevent intersecting Bug that sometimes happens otherwise (presumeably because of inaccurately rounded numbers)
    sideA = np.linalg.norm(bb[1]-bb[0])
    sideB = np.linalg.norm(bb[1]-bb[2])
    if cuttingDir_H_or_V == "H":   #Cut polygon Horizontaly through minimal bounding box
        if sideA >= sideB:
            dirVec = bb[1]-bb[0]       
            scaledVec = scaleVec(dirVec,np.linalg.norm(dirVec)*(percentageOfCut/100))
            cutLine = [bb[0]+scaledVec,bb[3]+scaledVec]     #Find cutting line fromBoundingbox
        else:
            dirVec = bb[1]-bb[2]       
            scaledVec = scaleVec(dirVec,np.linalg.norm(dirVec)*(percentageOfCut/100))
            cutLine = [bb[3]+scaledVec,bb[2]+scaledVec]     #Find cutting line fromBoundingboxprint("CutLine",cutLine)

    if cuttingDir_H_or_V == "V":    #Cut polygon Vertically through minimal bounding box
        if sideA <= sideB:
            dirVec = bb[1]-bb[0]       
            scaledVec = scaleVec(dirVec,np.linalg.norm(dirVec)*(percentageOfCut/100))
            cutLine = [bb[0]+scaledVec,bb[3]+scaledVec]     #Find cutting line fromBoundingbox
        else:
            dirVec = bb[1]-bb[2]       
            scaledVec = scaleVec(dirVec,np.linalg.norm(dirVec)*(percentageOfCut/100))
            cutLine = [bb[3]+scaledVec,bb[2]+scaledVec]     #Find cutting line fromBoundingboxprint("CutLine",cutLine)

    connectStreetLines = []
    for i in range(len(streetToConnectToAsNPVertices)):   #Convert Polygon to lines
        if i < len(streetToConnectToAsNPVertices)-1:
            CurrentLine = [streetToConnectToAsNPVertices[i], streetToConnectToAsNPVertices[i+1]]
            connectStreetLines.append(CurrentLine)
        else:
            CurrentLine = [streetToConnectToAsNPVertices[i], streetToConnectToAsNPVertices[i-(len(streetToConnectToAsNPVertices)-1)]]
            connectStreetLines.append(CurrentLine)
    for p in streetToConnectToAsNPVertices:       #Test if cutline runs through vertice of polygon which can lead to problems
        if pointOnLineSegment(p, cutLine) == True:
            if np.all(p != cutLine[0]) and np.all(p != cutLine[1]):
                return "no split possible because cutline runs through vertice of polygon"
    
    intersectPoints = []
    listOfVerticesAfterCut = []
    for j in connectStreetLines: #test for intersections between polygon and cutline
        testLines = [j,cutLine]
        if isIntersecting(testLines) == True:
            tempIntersectPoint = getIntersectPoint(testLines)
            if type(tempIntersectPoint) is not np.ndarray:   # if split line is collinear with polygon-line and runs through it: no split happens at this point.
                intersectPoints = []               
                continue
            elif any(np.array_equal(tempIntersectPoint, x) for x in intersectPoints):     #When cut goes through a vertice the cutpoint should not be appended twice
                continue
            else:
                intersectPoints.append(tempIntersectPoint)
                listOfVerticesAfterCut.append(j[1])
                tempIntersectPoint = []
    if (len(intersectPoints) % 2 ) != 0:    #Remove? Evaluate wether needed!
        return "no split possible due to odd intersection number" 

    allPtsForNewPolys = []
    for i in streetToConnectToAsNPVertices:               #Copying polygonasnp into new list, somehow didnt work with "copy()"
        allPtsForNewPolys.append(i)

    for k in range(len(intersectPoints)):               #Insert cutpoints into their correct place in list of polygon-vertices
        if np.all(intersectPoints[k] == listOfVerticesAfterCut[k]):
            continue                                   
        ind = arrayIndex(allPtsForNewPolys,listOfVerticesAfterCut[k])
        allPtsForNewPolys.insert(ind, intersectPoints[k])
    intersectInds = []
    for i in intersectPoints:      #Find all indexes of all the intersectionpoints inside the list of all indexes of the entire polygon
        intersectInds.append(arrayIndex(allPtsForNewPolys,i))
    intersectInds.sort()
    longIntersectInds = intersectInds.copy()
    longAllPtsForNewPolys = allPtsForNewPolys.copy()
    
    for j in range(2):
        for i in intersectInds:     #Append the entire intersectInds list to itself again to basically loop list
            longIntersectInds.append(i)
        for i in allPtsForNewPolys:     #Append the entire allPtsForNewPoly list to itself again to basically loop list
            longAllPtsForNewPolys.append(i)
    
    if len(intersectPoints) > 2:            #If the polygon has multiple cutting-points, search for cutting-point connection that basically "Jumps back" over other points
        intersectLines = []
        for i in range(len(intersectPoints)):   #Convert Polygon to lines
            if i < len(intersectPoints)-1:
                CurrentLine = [intersectPoints[i], intersectPoints[i+1]]
                intersectLines.append(CurrentLine)
            else:
                CurrentLine = [intersectPoints[i], intersectPoints[i-(len(intersectPoints)-1)]]
                intersectLines.append(CurrentLine)
        intersectLineLengths = []
        for i in intersectLines:
            intersectLineLengths.append(np.linalg.norm(i[1]-i[0]))
        maxInd = intersectLineLengths.index(max(intersectLineLengths))
        forbiddenLine = [[intersectLines[maxInd][0].round(5),intersectLines[maxInd][1].round(5)],[intersectLines[maxInd][1].round(5),intersectLines[maxInd][0].round(5)]]
    
    elif len(intersectPoints) <= 2:     #If the polygon has multiple cutting-points, search for cutting-point connection that basically "Jumps back" over other points
        intersectLines = [[intersectPoints[0].round(5),intersectPoints[1].round(5)],[intersectPoints[1].round(5),intersectPoints[0].round(5)]]
        lengthFromIntersectStart = []
        for i in intersectLines:
            lengthFromIntersectStart.append(np.linalg.norm(i[0]-cutLine[0]))
        if lengthFromIntersectStart[0] <= lengthFromIntersectStart[1]:
            forbiddenLineLeft = [intersectLines[0],intersectLines[0]]
            forbiddenLineRight = [intersectLines[1],intersectLines[1]]
        else:
            forbiddenLineLeft = [intersectLines[1],intersectLines[1]]
            forbiddenLineRight = [intersectLines[0],intersectLines[0]]


    leftLoops = []
    leftLoopParts = []
    rightLoops = []
    rightLoopParts = []

    for i in range(len(intersectInds)):         #Find Loops on left side of Cutline
        firstTP = longAllPtsForNewPolys[longIntersectInds[i]]
        secondTP = longAllPtsForNewPolys[longIntersectInds[i+1]]
        if len(intersectPoints) > 2:    #Make sure that loopfinder doesnt try to jump back over all other loops
            if (all(np.array_equal([firstTP.round(5),secondTP.round(5)][o], forbiddenLine[0][o]) for o in range(len(forbiddenLine[0]))) or 
            all(np.array_equal([secondTP.round(5),firstTP.round(5)][o], forbiddenLine[0][o]) for o in range(len(forbiddenLine[0])))):
                continue
        elif len(intersectPoints) == 2:
            if all(np.array_equal([firstTP.round(5),secondTP.round(5)][o], forbiddenLineLeft[0][o]) for o in range(len(forbiddenLineLeft[0]))):
                continue

        testLoop = [firstTP,secondTP,longAllPtsForNewPolys[longIntersectInds[i+1]+1]]
        currentLoop = []
        if determine_loop_direction(testLoop) == "Counterclockwise":
            currentLoop = [firstTP,secondTP]
            for j in range(len(allPtsForNewPolys)):
                currentLoop.append(longAllPtsForNewPolys[longIntersectInds[i+1]+1+j])
                if any(np.array_equal(longAllPtsForNewPolys[longIntersectInds[i+1]+1+j], x) for x in intersectPoints):
                    break                    
                
                    
        else:
            continue
        
        if np.all(currentLoop[-1] == currentLoop[0]):
            del currentLoop[-1]
            leftLoops.append(currentLoop)
        else:
            leftLoopParts.append(currentLoop)
        
    for i in reversed(range(len(intersectInds))):         #Find Loops on right side of Cutline
        firstTP = longAllPtsForNewPolys[longIntersectInds[i]]
        secondTP = longAllPtsForNewPolys[longIntersectInds[i-1]]

        if len(intersectPoints) > 2:    #Make sure that loopfinder doesnt try to jump back over all other loops
            if (all(np.array_equal([firstTP.round(5),secondTP.round(5)][o], forbiddenLine[0][o]) for o in range(len(forbiddenLine[0]))) or 
            all(np.array_equal([secondTP.round(5),firstTP.round(5)][o], forbiddenLine[0][o]) for o in range(len(forbiddenLine[0])))):
                continue
        elif len(intersectPoints) == 2:
            if all(np.array_equal([firstTP.round(5),secondTP.round(5)][o], forbiddenLineRight[0][o]) for o in range(len(forbiddenLineRight[0]))):
                continue

        testLoop = [firstTP,secondTP,longAllPtsForNewPolys[longIntersectInds[i-1]+1]]
        currentLoop = []
        if determine_loop_direction(testLoop) == "Counterclockwise":
            currentLoop = [firstTP,secondTP]
            for j in range(len(allPtsForNewPolys)):
                currentLoop.append(longAllPtsForNewPolys[longIntersectInds[i-1]+1+j])
                if any(np.array_equal(longAllPtsForNewPolys[longIntersectInds[i-1]+1+j], x) for x in intersectPoints):
                    break                    
                
                    
        else:
            continue
        if np.all(currentLoop[-1] == currentLoop[0]):
            del currentLoop[-1]
            rightLoops.append(currentLoop)
        else:
            rightLoopParts.append(currentLoop)

   
    if len(rightLoopParts) >= 2:
        currentRightLoops = arrangePolygonPieces(rightLoopParts)
        for i in currentRightLoops:
            rightLoops.append(i)

    if len(leftLoopParts) >= 2:
        currentLeftLoops = arrangePolygonPieces(leftLoopParts)
        for i in currentLeftLoops:
            leftLoops.append(i)
            
    turnedLeftLoops = []
    turnedRightLoops = []
    for b in leftLoops:
        tempTurn = []
        for i in range(len(b)):      
            tempTurn.append(b[len(b)-(i+1)])
        turnedLeftLoops.append(tempTurn)
    for b in rightLoops:
        tempTurn = []
        for i in range(len(b)):     
            tempTurn.append(b[len(b)-(i+1)])
        turnedRightLoops.append(tempTurn)
    return [turnedLeftLoops,turnedRightLoops]

def pointInPoly(pointAsNP,polyAsNPLines):
    pointList = pointAsNP.tolist()
    polyNP = []
    poly = []

    for i in polyAsNPLines:
        polyNP.append(i[0])
    for i in polyNP:
        poly.append(i.tolist())

    if len(poly) < 3:  # not a polygon - no areaNp
        return False
    
    total = 0
    i = 0
    x = pointList[0]
    y = pointList[1]
    next = 0
    for i in range(len(poly)):
        next = (i + 1) % len(poly)
        if poly[i][1] <= y < poly[next][1]:
            if x < poly[i][0] + (y - poly[i][1]) * (poly[next][0] - poly[i][0]) / (poly[next][1] - poly[i][1]):
                total += 1
        elif poly[next][1] <= y < poly[i][1]:
            if x < poly[i][0] + (y - poly[i][1]) * (poly[next][0] - poly[i][0]) / (poly[next][1] - poly[i][1]):
                total += 1
    if total % 2 == 0:
        return False
    else:
        return True

def pointOnLine(pointAsNP,lineAsNP):
    # NP to List
    lineList = []
    tempPoint = []
    for i in lineAsNP:
        tempPoint = i.tolist()
        lineList.append (tempPoint)
    pointList = pointAsNP.tolist()
    
    endpoint1 = lineList[0]
    endpoint2 = lineList[1]
    #Exeption for Vertical lines with undefined slope
    if (endpoint2[0] - endpoint1[0]) == 0:
        if pointList[0] == endpoint1[0]:
            #Point Is On Line
            return True
        else:
            #Point is not on line
            return False
    #Calculate Slope
    else:
        slope = (endpoint2[1] - endpoint1[1]) / (endpoint2[0] - endpoint1[0])

    # Calculate the y-intercept of the line segment
    y_intercept = endpoint1[1] - (slope * endpoint1[0])
    # Calculate the y-coordinate of the point on the line segment
    y_on_line = (slope * pointList[0]) + y_intercept

    # Check if the y-coordinate of the point is equal to the y-coordinate of the point passed to the function
    if y_on_line == pointList[1]:
        #Point is on line
        return True
    else:
        #Point is not on line
        return False

def pointOnLineSegment(pointAsNP, lineAsNP, threshold = 1e-3):
    p, q, r = lineAsNP[0], pointAsNP, lineAsNP[1]
    if (q[0] <= max(p[0], r[0]) + threshold and q[0] >= min(p[0], r[0]) - threshold and
        q[1] <= max(p[1], r[1]) + threshold and q[1] >= min(p[1], r[1]) - threshold and
        abs(np.cross(r - p, q - p)) < threshold):
        return True
    else:
        return False

def isIntersecting(intersectLinesAsNPList):
    class Point:
        def __init__(self, x, y):
            self.x = x
            self.y = y


    # Given three collinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    def onSegment(p, q, r):
        if ( (q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False

    def orientation(p, q, r):
    #Find point orientation
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if (val > 0):
            
            # Clockwise orientation
            return 1
        elif (val < 0):
            
            # Counterclockwise orientation
            return 2
        else:
            
            # Collinear orientation
            return 0

    # The main function that returns true if
    # the line segment 'p1q1' and 'p2q2' intersect.
    def doIntersect(p1,q1,p2,q2):
        
        # Find the 4 orientations required for
        # the general and special cases
        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        # General case
        if ((o1 != o2) and (o3 != o4)):
            return True

        # Special Cases

        # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
        if ((o1 == 0) and onSegment(p1, p2, q1)):
            return True

        # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
        if ((o2 == 0) and onSegment(p1, q2, q1)):
            return True

        # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
        if ((o3 == 0) and onSegment(p2, p1, q2)):
            return True

        # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
        if ((o4 == 0) and onSegment(p2, q1, q2)):
            return True

        # If none of the cases
        return False

    TempArrayToList = []
    tempArray1 = []
    for i in intersectLinesAsNPList:
        for j in i:
            tempArray1.append(j.tolist())
        TempArrayToList.append(tempArray1)
        tempArray1 = []

    
    p1 = Point(TempArrayToList[0][0][0],TempArrayToList[0][0][1])
    q1 = Point(TempArrayToList[0][1][0],TempArrayToList[0][1][1])
    p2 = Point(TempArrayToList[1][0][0],TempArrayToList[1][0][1])
    q2 = Point(TempArrayToList[1][1][0],TempArrayToList[1][1][1])
    
    if doIntersect(p1, q1, p2, q2):
        return True
    else:
        return False

def getIntersectPoint(intersectLinesAsNPList):
    
    x1, y1 = intersectLinesAsNPList[0][0]
    x2, y2 = intersectLinesAsNPList[0][1]
    x3, y3 = intersectLinesAsNPList[1][0]
    x4, y4 = intersectLinesAsNPList[1][1]

    if (x1, y1) == (x3, y3) or (x1, y1) == (x4, y4):#Check if Intersection-point is already included in input because x_num and y_num are = 0 otherwise which causes mistakes
        return np.array([x1, y1])
    if (x2, y2) == (x3, y3) or (x2, y2) == (x4, y4):
        return np.array([x2, y2])

    x_num = (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)
    y_num = (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    
    if denom == 0:
        return "Lines are parallel"
    x = x_num / denom
    y = y_num / denom
    return np.array([x, y])

    """a1 = intersectLinesAsNPList[0][0]
    a2 = intersectLinesAsNPList[0][1]
    b1 = intersectLinesAsNPList[1][0]
    b2 = intersectLinesAsNPList[1][1]
    
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return "False"
    return np.array([x/z, y/z])         # returns intersection point as NP-Array"""

def pointOnPolygon(pointAsNP,polygonAsNPLines):
    for i in polygonAsNPLines:
        if pointOnLineSegment(pointAsNP,i) == True:
            return True
    return False

def scaleVec(vecAsNP,newLength):
    distance = np.linalg.norm(vecAsNP)
    scale_factor = newLength / distance
    return vecAsNP * scale_factor

def normalizeNpVec(vec):
    return vec / np.linalg.norm(vec)

def mainStreetGenerator(BaseShape,InputLines): #Edit: Write exception for collinear inputlines! Write exaption for inputline that generates street segment through another inputpoint #Write exception for self-interecting Polygon!!!
    """for i in InputLines:
        for j in InputLines:
            if np.array_equal(i,j):
                continue
            intersect = isIntersecting([i,j])"""
    #Find valid generation starting points
    startPointAndVec = [] 
    generatedStreets = []
    for i in InputLines:
        pc = []
        #Testing both points of the current Inputline for their position
        for j in i:
            if pointOnPolygon(j,BaseShape) == True:
                pc.append("onOutline")
                continue
            elif pointInPoly(j,BaseShape) == True:
                pc.append("inside")
                continue
            else:
                pc.append("outside")
       
        #Generating start-points and vectors for the street generation out of the inputlines and their points' conditions

        if pc[0] == "outside" and pc[1] == "outside": #Both points are outside of baseshape
            intersectPoints = []
            for j in BaseShape: #test if inputline runs through base shape (for every boundary line of base shape) despite endpoints beeing outside
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []               # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            
            if len(intersectPoints) == 2:                 # if the endpoints of the inputline are outside the baseshape, but it intersects the baseshape twice, 
                generatedStreets.append(intersectPoints)  # - the resulting line inside the baseshape is effectivly a valid street
            else:
                continue
            
        if pc[0] == "inside" and pc[1] == "inside": #Both points are contained in baseshape
            intersectPoints = []
            for j in BaseShape: #test if inputline runs through base shape (for every boundary line of base shape) despite endpoints beeing inside
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:        # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []               # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            if len(intersectPoints) == 0:  #When there are no intersections with the outter lines, midpoint of inputline = start, and vectors in both directions as dir_vecs
                tP = []
                for p in i:
                    tP.append(p.tolist())
                midpoint = np.array([(tP[0][0] + tP[1][0])/2, (tP[0][1] + tP[1][1])/2])
                for p in i:
                    dirVec = p - midpoint
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([midpoint,dirVecScaled])
                continue
            elif len(intersectPoints) == 1: #When there is one intersectionpoint with the edges, just take the intersectionpoint as start
                for p in i:
                    dirVec = p - intersectPoints[0]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                continue
            elif len(intersectPoints) == 2:  #When there are two intersectionpoints with the boundary, take the closest to the point as start and calculate dir_vec
                for p in i:
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k-p))
                    if pointDistance[0] < pointDistance[1]:
                        dirVec = p - intersectPoints[0]
                        dirVecScaled = normalizeNpVec(dirVec)
                        startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    elif pointDistance[0] > pointDistance[1]:
                        dirVec = p - intersectPoints[1]
                        dirVecScaled = normalizeNpVec(dirVec)
                        startPointAndVec.append([intersectPoints[1],dirVecScaled])
                    else:
                        continue
            else:
                continue
        
        if pc[0] == "onOutline" and pc[1] == "onOutline": #Both points are on the baseshapes outline DEACTIVATED, MAYBE FIX LATER
            continue #Both points on outline have a high chance to be no ciable street. Could also mean street outside of polygon. MAYBE FIX LATER!
        
        if pc[0] == "inside" and pc[1] == "outside" or pc[0] == "outside" and pc[1] == "inside": #One point inside of baseshape, other outside
            intersectPoints = []
            for j in BaseShape: #test on every boundary line of base shape for intersection and find out intersection point
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []          # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            if len(intersectPoints) == 1: #If the line has one intersection with baseshape, this is starting point for generation, dir_vec towards point in baseshape
                if pc[0] == "inside":
                    dirVec = i[0] - intersectPoints[0]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    dirVec = i[1] - intersectPoints[0]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                else:
                    continue
            
            elif len(intersectPoints) > 1:   #If the line has multiple intersections,closest intersection to the inside-point is takes as start, inside-point for dir_vec
                if pc[0] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[0]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[0] - intersectPoints[minpos]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[1]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[1] - intersectPoints[minpos]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
            else:
                continue

        if pc[0] == "inside" and pc[1] == "onOutline" or pc[0] == "onOutline" and pc[1] == "inside": #One point inside baseshape, other on it's outline
            intersectPoints = []
            for j in BaseShape: #test on every boundary line of base shape for intersection and find out intersection point
                testLines = [i]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []          # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []
            if len(intersectPoints) == 1:  #If the line has one intersection (should be the point which is on the line) take this as start, iside point as dir_vec
                if pc[0] == "inside":
                    dirVec = i[0] - intersectPoints[0]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    dirVec = i[1] - intersectPoints[0]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[0],dirVecScaled])
                    continue
                else:
                    continue
            elif len(intersectPoints) > 1:   #If the line has multiple intersections,closest intersection to the inside-point is takes as start, inside-point for dir_vec
                if pc[0] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[0]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[0] - intersectPoints[minpos]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
                elif pc[1] == "inside":
                    pointDistance = []
                    for k in intersectPoints:
                        pointDistance.append(np.linalg.norm(k - i[1]))
                    minpos = pointDistance.index(min(pointDistance))
                    dirVec = i[1] - intersectPoints[minpos]
                    dirVecScaled = normalizeNpVec(dirVec)
                    startPointAndVec.append([intersectPoints[minpos],dirVecScaled])
                    continue
            else:
                continue

        if pc[0] == "onOutline" and pc[1] == "outside" or pc[0] == "outside" and pc[1] == "onOutline": #One point on Outline, other outside DEACTIVATED, MAYBE FIX LATER
            continue

        else:
            continue
        
    for i in startPointAndVec:

        def generateStreetSegment(startPoint,dirVec,BaseShape,existingStreets,segmentLength):
            
            newDirVec = scaleVec(dirVec,segmentLength)
            currentSegment = [startPoint, startPoint + newDirVec]
            intersectPoints = []
            allLinesToTest = BaseShape + existingStreets
            
            for j in allLinesToTest: #test on every boundary line of base shape for intersection and find out intersection points
                testLines = [currentSegment]
                testLines.append(j)
                if isIntersecting(testLines) == True:
                    tempIntersectPoint = getIntersectPoint(testLines)
                    if type(tempIntersectPoint) is not np.ndarray:   # Exeption if line runs through baseshape but is colinear with boundary line
                        intersectPoints = []          # - of baseshape which could lead to problems
                        break                                  
                    else:
                        intersectPoints.append(tempIntersectPoint)
                        tempIntersectPoint = []

            spList = startPoint.tolist()
            spListRounded = []
            for i in spList:
                spListRounded.append(round(i,3))
            ipList = []
            for b in intersectPoints:
                ipList.append(b.tolist())
            
            ipListRounded = []
            tempIpList = []
            for o in ipList:
                for k in o:
                    tempIpList.append(round(k,3))
                ipListRounded.append(tempIpList)
                tempIpList = []
  
            if spListRounded in ipListRounded:
                ind = ipListRounded.index(spListRounded)
                del intersectPoints[ind]

            if len(intersectPoints) == 0:
                return "noIntersect"
            elif len(intersectPoints) == 1:
                return [startPoint,intersectPoints[0]]
            elif len(intersectPoints) > 1:
                pointDistance = []
                for k in intersectPoints:
                    pointDistance.append(np.linalg.norm(k - startPoint))
                minpos = pointDistance.index(min(pointDistance))
                return [startPoint,intersectPoints[minpos]]
            


        def system(startPoint,dirVec,BaseShape,existingStreets,segmentLength):
            
            segmentLength += 500 
            currentStreetSegment = generateStreetSegment(startPoint,dirVec,BaseShape,existingStreets,segmentLength)
            if currentStreetSegment == "noIntersect" and segmentLength <= 500:
                return system(startPoint,dirVec,BaseShape,existingStreets,segmentLength)
            elif currentStreetSegment == "noIntersect" and segmentLength > 500:
                return "false"
            else:
                return currentStreetSegment

        segmentLength = 0
        
        currentGeneratedStreet = system(i[0],i[1],BaseShape,generatedStreets,segmentLength)
        if currentGeneratedStreet == "false":
            continue
        else:
            generatedStreets.append(currentGeneratedStreet)

    return generatedStreets

def splitLine(lineToSplitAsNP,splittingLineOrPointAsNP):
    if len (lineToSplitAsNP) == 2:
        if type(splittingLineOrPointAsNP) is np.ndarray and len(splittingLineOrPointAsNP) == 2:
            if (splittingLineOrPointAsNP == lineToSplitAsNP[0]).all() or (splittingLineOrPointAsNP == lineToSplitAsNP[1]).all():
                return "Intersecting only in Endpoint of Line"
            isOnLine = pointOnLineSegment(splittingLineOrPointAsNP,lineToSplitAsNP)
            if isOnLine == False:
                return "notIntersecting"
            else:
                return [[lineToSplitAsNP[0],splittingLineOrPointAsNP],[splittingLineOrPointAsNP,lineToSplitAsNP[1]]]

        elif type(splittingLineOrPointAsNP) is list and len(splittingLineOrPointAsNP) == 2:
            for i in lineToSplitAsNP:
                if pointOnLineSegment(i,splittingLineOrPointAsNP) == True:
                    return "Intersecting only in Endpoint of Line to split or Lines are identical"
            if isIntersecting([lineToSplitAsNP,splittingLineOrPointAsNP]) == True:
                intersectPoint = getIntersectPoint([lineToSplitAsNP,splittingLineOrPointAsNP])
                if type(intersectPoint) is not np.ndarray:
                    return "no single splittingpoint"
                else:
                    return [[lineToSplitAsNP[0],intersectPoint],[intersectPoint,lineToSplitAsNP[1]]]
            else:
                return "notIntersecting"
        else:
            return "please only pass a single point or line as splittingLineOrPointAsNP"
    else:
        return "please only provide a single line to split"

def splitMultipleLines(linesToSplitAsNP):
    splitLines = []
    for i in linesToSplitAsNP:
        intersectPoints = []
        for j in linesToSplitAsNP:
            if np.array_equal(i,j):
                continue
            if isIntersecting([i,j]) == True or pointOnLineSegment(j[0],i) or pointOnLineSegment(j[1],i):
                if np.array_equal(i[0],j[0]) or np.array_equal(i[0],j[1]) or np.array_equal(i[1],j[0]) or np.array_equal(i[1],j[1]):
                    continue
                if pointOnLineSegment(i[0],j) or pointOnLineSegment(i[1],j):
                    continue
                else:
                    
                    currentIntersect = getIntersectPoint([i,j])
                    
                    if type(currentIntersect) is not np.ndarray:
                        continue
                    intersectPoints.append(currentIntersect)
            else:
                continue

        if len(intersectPoints) == 1:
            splitLines.append([i[0],intersectPoints[0]])
            splitLines.append([intersectPoints[0],i[1]])
            continue
        else:
            start = i[0]
            end = i[1]
            # Get the vector of the line segment
            lineVec = end - start
            # Create a list to store the ordered points
            orderedPoints = []
            for point in intersectPoints:
                # Get the vector from the start of the line segment to the point
                pointVec = point - start
                # Use the dot product to determine the position of the point on the line segment
                position = np.dot(pointVec, lineVec)
                # Append the point and its position to the list
                orderedPoints.append((point, position))
            # Sort the list of points based on their position on the line segment
            orderedPoints.sort(key=lambda x: x[1])
            # Return only the points
            pointsInOrder = [point for point, position in orderedPoints]
            pointsInOrder.insert(0, i[0])
            pointsInOrder.append(i[1])
            for k in range(len(pointsInOrder)-1):
                splitLines.append([pointsInOrder[k],pointsInOrder[k+1]])
    return splitLines

#Turning the generated point-list into a drawn line
def draw_system_streets(plots):
    for lines in plots:
        for points in lines:
            line_geom = THREE.BufferGeometry.new()
            points = to_js(points)
            
            line_geom.setFromPoints( points )

            material = THREE.LineBasicMaterial.new()
            material.color = THREE.Color.new("rgb(0,0,0)")
            
            vis_line = THREE.Line.new( line_geom, material )
            global scene
            scene.add(vis_line)
############################################
def draw_system_baseshape(lines):
    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        line_geom.setFromPoints( points )

        material = THREE.LineBasicMaterial.new()
        material.color = THREE.Color.new("#58D68D")
        
        vis_line = THREE.Line.new( line_geom, material )
        global scene
        scene.add(vis_line)
############################################
def draw_system_input(lines):
    for points in lines:
        line_geom = THREE.BufferGeometry.new()
        points = to_js(points)
        
        line_geom.setFromPoints( points )

        material = THREE.LineBasicMaterial.new()
        material.color = THREE.Color.new("#FA8072")
                
        vis_line = THREE.Line.new( line_geom, material )
        global scene
        scene.add(vis_line)
##########################################################################################
def draw_system_substreets(plots):
    for lines in plots:
        for points in lines:
            line_geom = THREE.BufferGeometry.new()
            points = to_js(points)
            
            line_geom.setFromPoints( points )
            material = THREE.LineBasicMaterial.new()
            material.color = THREE.Color.new("#FDFEFE")
            
            vis_line = THREE.Line.new( line_geom, material )
            global scene
            scene.add(vis_line)

lines=[
[[0, 0],[ 2, 2]],#Input Lines
[[2, 2], [2, 0]], 
[[2, 0], [0, 0]],
[[6, 0], [4, 1]], 
[[4, 1], [2, 0]], 
[[2, 0], [2, 2]],
[[2, 2], [6, 2]], 
[[6, 2], [6, 0]], 
[[6, 0], [6, 2]], 
[[6, 2], [8, 3]], 
[[8, 3], [9, 1]], 
[[9, 1], [8, 0]], 
[[8, 0], [6, 0]], 
[[6, 4], [6, 5]], 
[[6, 5], [8, 5]], 
[[8, 5], [8, 3]], 
[[8, 3], [6, 2]], 
[[6, 2], [6, 4]], 
[[6, 4], [3, 4]], 
[[3, 4], [2, 2]], 
[[2, 2], [6, 2]], 
[[6, 2], [6, 4]], 
[[0, 0], [0, 3]], 
[[0, 3], [2, 2]], 
[[2, 2], [0, 0]], 
[[0, 3], [2, 2]], 
[[2, 2], [3, 4]], 
[[3, 4], [3, 5]], 
[[3, 5], [0, 5]], 
[[0, 5], [0, 3]], 
[[6, 4], [6, 5]], 
[[6, 5], [3, 5]], 
[[3, 5], [3, 4]], 
[[3, 4], [6, 4]], 
[[6, 5], [3, 5]], 
[[3, 5], [3, 7]], 
[[3, 7], [6, 5]], 
[[0, 7], [0, 5]], 
[[0, 5], [3, 5]], 
[[3, 5], [3, 7]], 
[[3, 7], [0, 7]]
]

# lines = [
# [[70.5, 100.0], [67.38502673796792, 50.160427807486634]], 
# [[67.38502673796792, 50.160427807486634], [64.25, 0.0]], 
# [[37.5, 69.5], [0.0, 77.0]], 
# [[37.5, 69.5], [68.20987654320987, 63.35802469135801]], 
# [[0.0, 22.083333333333332], [50.0, 42.91666666666667]], 
# [[50.0, 42.91666666666667], [67.38502673796792, 50.16042780748664]], 
# [[50.0, 0.0], [50.0, 42.91666666666668]], 
# [[0, 0], [0.0, 22.083333333333332]], 
# [[0.0, 22.083333333333332], [0.0, 77.0]], 
# [[0.0, 77.0], [0, 100]], 
# [[0, 100], [70.5, 100.0]], 
# [[70.5, 100.0], [100, 100]], 
# [[100, 100], [100, 0]], 
# [[100, 0], [64.25, 0.0]], 
# [[64.25, 0.0], [50.0, 0.0]], 
# [[50.0, 0.0], [0, 0]]
# ]



# Simple render and animate

def render(*args):
    global linesIfinal, meshesIfinal,scene
    window.requestAnimationFrame(create_proxy(render))
    updateI()
    updateO ()
    updateL ()
    
  
    controls.update()
    
    composer.render()





def post_process():

    render_pass = THREE.RenderPass.new(scene, camera)
    render_pass.clearColor = THREE.Color.new(0,0,0)
    render_pass.ClearAlpha = 0
    fxaa_pass = THREE.ShaderPass.new(THREE.FXAAShader)
    pixelRatio = window.devicePixelRatio
    fxaa_pass.material.uniforms.resolution.value.x = 1 / ( window.innerWidth * pixelRatio )
    fxaa_pass.material.uniforms.resolution.value.y = 1 / ( window.innerHeight * pixelRatio )

    global composer
    composer = THREE.EffectComposer.new(renderer)
    composer.addPass(render_pass)
    composer.addPass(fxaa_pass)

# Adjust display when window size changes

def on_window_resize(event):
    event.preventDefault()
    global renderer
    global camera
    camera.aspect = window.innerWidth / window.innerHeight
    camera.updateProjectionMatrix()
    renderer.setSize( window.innerWidth, window.innerHeight )

    #postprocessing after resize
    post_process()

#-----------------------------------------------------------------------

#RUN THE MAIN PROGRAM

if __name__=='__main__':
    main()
