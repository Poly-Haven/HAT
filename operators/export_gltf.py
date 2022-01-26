import bmesh
import bpy
import json
import mathutils
import os
from shutil import rmtree
from ..utils.filename_utils import get_map_name


def export_model(cls, context, slug, gltf_file):
    try:
        collection = bpy.data.collections[slug]
    except KeyError:
        cls.report({'ERROR'}, "No collection named " + slug)
        return {'CANCELLED'}

    for o in bpy.data.objects:
        o.select_set(o in list(collection.objects))

    if context.scene.hat_props.asset_type == 'model':
        bpy.ops.export_scene.gltf(
            export_format='GLTF_SEPARATE',
            export_texture_dir='textures_TEMP',
            use_selection=True,
            export_apply=True,
            filepath=gltf_file,
        )

    try:
        rmtree(os.path.join(os.path.dirname(
            bpy.data.filepath), 'textures_TEMP'))
    except FileNotFoundError:
        cls.report({'WARNING'}, "No textures exported")


def export_texture(cls, context, slug, gltf_file):

    def find_disp(images):
        disp_options = ['disp', 'displacement', 'height']
        for img in images:
            if not img.filepath:
                continue
            map_name = get_map_name(img.filepath)
            if map_name in disp_options:
                return img
        return None

    try:
        plane = bpy.data.objects['Plane']
    except KeyError:
        cls.report({'ERROR'}, "No 'Plane' object found")
        return {'CANCELLED'}

    D = bpy.data
    bm = bmesh.new()

    Filepath = bpy.data.filepath
    Directory = os.path.dirname(Filepath)
    DirectoryTextures = Directory + '\\textures\\'
    DirectoryTexturesTemp = Directory + '\\textures_TEMP\\'

    # REFERENCE SIZE OF PLANE
    WorldSize = plane.dimensions.x

    # CREATE SPHERE
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=256, ring_count=128, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    obj = context.object
    obj.name = 'sphere_gltf'
    context.object.dimensions = (WorldSize, WorldSize, WorldSize)
    bpy.ops.object.shade_smooth()
    bpy.ops.object.modifier_add(type='REMESH')
    obj.modifiers["Remesh"].use_smooth_shade = True
    obj.modifiers["Remesh"].voxel_size = 0.01
    bpy.ops.object.modifier_apply(modifier="Remesh")

    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.sphere_project(direction='VIEW_ON_EQUATOR', align='POLAR_ZX',
                              correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False)

    obj = context.active_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    S = mathutils.Vector((2, 1))
    uv_layer = bm.loops.layers.uv.verify()
    # scale UVs by S
    for f in bm.faces:
        for l in f.loops:
            l[uv_layer].uv *= S

    bpy.ops.object.editmode_toggle()

    context.object.rotation_euler = (1.5707, 0, 0)
    bpy.ops.object.transform_apply(location=False, scale=True, rotation=True)

    # Assign Material AND GET DISPLACEMENT ATTRIBUTES
    mat = D.materials[slug]
    context.active_object.data.materials.append(mat)
    DispMat_Mid = D.materials[slug].node_tree.nodes["Displacement"].inputs[1].default_value
    DispMat_Scale = D.materials[slug].node_tree.nodes["Displacement"].inputs[2].default_value

    # CREATE TEXTURE DATA BLOCK
    ImgData = find_disp(D.images)

    if ImgData == None:
        cls.report({'ERROR'}, "Could not find displacement data block")
        return {'CANCELLED'}

    DispTexture = D.textures.new('Displacement', 'IMAGE')
    DispTexture.image = ImgData

    # CREATE DISPLACEMENT MODIFIER
    DispMod = obj.modifiers.new('DisplacementMod', 'DISPLACE')
    DispMod.texture = DispTexture
    DispMod.texture_coords = 'UV'
    DispMod.strength = DispMat_Scale
    DispMod.mid_level = DispMat_Mid
    UVScaleX = D.materials[slug].node_tree.nodes["Mapping"].inputs[3].default_value[0]
    UVScaleY = D.materials[slug].node_tree.nodes["Mapping"].inputs[3].default_value[1]
    UVScaleZ = D.materials[slug].node_tree.nodes["Mapping"].inputs[3].default_value[2]
    D.textures['Displacement'].repeat_x = UVScaleX
    D.textures['Displacement'].repeat_y = UVScaleY

    # CREATE DECIMATE MODIFIER
    DecimateMod = obj.modifiers.new('DecimateMod', 'DECIMATE')
    DecimateMod.ratio = 0.285

    # Correct Smoothing
    context.object.data.use_auto_smooth = True
    context.object.data.auto_smooth_angle = 180
    DecimateMod = obj.modifiers.new('WeightedNormal', 'WEIGHTED_NORMAL')

    # EXPORT GLTF
    bpy.ops.export_scene.gltf(
        export_format='GLTF_SEPARATE',
        export_texture_dir='textures_TEMP',
        export_selected=True,
        use_selection=True,
        export_apply=True,
        filepath=gltf_file,
    )

    with open(gltf_file, 'r') as json_file:
        gltf_data = json.load(json_file)

    PackedMap = '-' + slug + '_rough.png'
    NoPackedMap = slug + '_rough.png'
    FoundPackedMap = False
    OldPackedMapSlug = 'none'

    for p in gltf_data['images']:
        uri = p['uri']
        if p['uri'].endswith(PackedMap):
            FoundPackedMap = True
            OldPackedMapSlug = p['uri']
            p['uri'] = 'textures/' + slug + '_arm.png'
            break
        elif p['uri'].endswith(NoPackedMap):
            p['uri'] = 'textures/' + slug + '_rough.png'
            break
        elif p['uri'].endswith('textures/' + slug + '_arm.png'):
            break
        uri = uri.replace('textures_TEMP', 'textures')
        p['uri'] = uri

    with open(gltf_file, 'w') as jsonfile:
        json.dump(gltf_data, jsonfile, indent=4)

    # RENAME PACKED FILE
    OldPackedMapSlug = OldPackedMapSlug.replace(
        'textures_TEMP/', '').replace('textures_TEMP\\', '')
    OldPackedMap = DirectoryTexturesTemp + OldPackedMapSlug
    NewPackedMap = DirectoryTextures + slug + '_arm.png'
    if FoundPackedMap:
        os.rename(OldPackedMap, NewPackedMap)


class HAT_OT_export_gltf(bpy.types.Operator):
    bl_idname = "hat.export_gltf"
    bl_label = "Export GLTF"
    bl_description = "Export this asset as a GLTF file as standard for uploading to polyhaven.com"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved and context.scene.hat_props.asset_type == 'model'

    def execute(cls, context):
        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        gltf_file = os.path.join(os.path.dirname(
            bpy.data.filepath), slug + '.gltf')

        if context.scene.hat_props.asset_type == 'model':
            export_model(cls, context, slug, gltf_file)
        else:
            export_texture(cls, context, slug, gltf_file)

        with open(gltf_file, 'r') as json_file:
            data = json.load(json_file)

        errors = []
        for p in data['images']:
            uri = p['uri']
            uri = uri.replace('textures_TEMP', 'textures')
            if uri.endswith("_png.png"):
                uri = uri.replace("_png.png", ".png")
            if uri.endswith("_rough.png"):
                uri = uri.replace("_rough.png", "_arm.png")

            fp = os.path.join(os.path.dirname(bpy.data.filepath), uri)
            if not os.path.exists(fp):
                errors.append(uri)

            p['uri'] = uri

        if errors:
            cls.report({'ERROR'}, "Image not found:\n" + '\n'.join(errors))

        with open(gltf_file, 'w') as f:
            json.dump(data, f, indent=4)

        return {'FINISHED'}
