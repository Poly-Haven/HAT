import bmesh
import bpy
import json
import logging
import mathutils
import os
from shutil import rmtree
from ..utils.filename_utils import get_map_name, get_slug

log = logging.getLogger(__name__)


def select_objects_in_collection(collection, depth=0):
    """Recursively select all objects in the given collection."""
    if depth == 0:
        # First time, deselect all objects
        for obj in bpy.data.objects:
            try:
                obj.select_set(False)
            except RuntimeError:
                log.error("Failed to deselect object %s. It may not be selectable.", obj.name)
                continue
    elif depth > 100:
        log.error("Too deep recursion in select_objects_in_collection, aborting to prevent infinite loop.")
        return
    log.debug("Selecting objects in collection: %s", collection.name)
    for obj in collection.objects:
        try:
            obj.select_set(True)
        except RuntimeError:
            log.error("Failed to select object %s. It may not be selectable.", obj.name)
            continue
    for child_collection in collection.children:
        select_objects_in_collection(child_collection, depth + 1)


def export_model(cls, context, slug, gltf_file):
    if f"{slug}_LOD0" in bpy.data.collections:
        collection = bpy.data.collections[f"{slug}_LOD0"]
    elif f"{slug}_static" in bpy.data.collections:
        collection = bpy.data.collections[f"{slug}_static"]
    elif slug in bpy.data.collections:
        collection = bpy.data.collections[slug]
    else:
        cls.report({"ERROR"}, "No collection named " + slug)
        return {"CANCELLED"}

    select_objects_in_collection(collection)

    if context.scene.hat_props.asset_type == "model":
        bpy.ops.export_scene.gltf(
            export_format="GLTF_SEPARATE",
            export_texture_dir="textures_TEMP",
            use_selection=True,
            export_apply=True,
            filepath=gltf_file,
        )


def export_texture(cls, context, slug, gltf_file):

    def find_disp(images):
        disp_options = ["disp", "displacement", "height"]
        for img in images:
            if not img.filepath:
                continue
            map_name = get_map_name(img.filepath, slug)
            if map_name in disp_options:
                return img
        return None

    D = bpy.data

    try:
        plane = D.objects["Plane"]
    except KeyError:
        cls.report({"ERROR"}, "No 'Plane' object found")
        return {"CANCELLED"}

    try:
        mat = D.materials[slug]
    except KeyError:
        cls.report({"ERROR"}, "No material with slug name")
        return {"CANCELLED"}

    bm = bmesh.new()

    folder = os.path.dirname(D.filepath)

    # REFERENCE SIZE OF PLANE
    scale = plane.dimensions.x

    # CREATE SPHERE
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=256, ring_count=128, enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
    )
    obj = context.active_object
    obj.name = "sphere_gltf"
    obj.dimensions = (scale, scale, scale)
    bpy.ops.object.shade_smooth()
    bpy.ops.object.modifier_add(type="REMESH")
    obj.modifiers["Remesh"].use_smooth_shade = True
    obj.modifiers["Remesh"].voxel_size = 0.01
    bpy.ops.object.modifier_apply(modifier="Remesh")

    bpy.ops.object.editmode_toggle()

    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.sphere_project(
        direction="VIEW_ON_EQUATOR", align="POLAR_ZX", correct_aspect=True, clip_to_bounds=False, scale_to_bounds=False
    )

    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    mult = mathutils.Vector((2, 1))
    uv_layer = bm.loops.layers.uv.verify()
    # scale UVs by S
    for f in bm.faces:
        for l in f.loops:
            l[uv_layer].uv *= mult

    bpy.ops.object.editmode_toggle()

    obj.rotation_euler = (1.5707, 0, 0)
    bpy.ops.object.transform_apply(location=False, scale=True, rotation=True)

    context.active_object.data.materials.append(mat)  # Assign material

    # CREATE TEXTURE DATA BLOCK
    disp_image = find_disp(D.images)

    if disp_image is None:
        cls.report({"ERROR"}, "Could not find displacement data block")
        return {"CANCELLED"}

    disp_texture = D.textures.new("Displacement", "IMAGE")
    disp_texture.image = disp_image

    # CREATE DISPLACEMENT MODIFIER
    disp_mod = obj.modifiers.new("DisplacementMod", "DISPLACE")
    disp_mod.texture = disp_texture
    disp_mod.texture_coords = "UV"
    disp_node = None
    for n in mat.node_tree.nodes:
        if n.type == "DISPLACEMENT":
            disp_node = n
            break
    if not disp_node:
        cls.report({"ERROR"}, "No displacement node")
        return {"CANCELLED"}
    disp_mod.strength = disp_node.inputs[2].default_value
    disp_mod.mid_level = disp_node.inputs[1].default_value
    mapping_node = mat.node_tree.nodes["Mapping"]
    D.textures["Displacement"].repeat_x = round(mapping_node.inputs[3].default_value[0])
    D.textures["Displacement"].repeat_y = round(mapping_node.inputs[3].default_value[1])

    # CREATE DECIMATE MODIFIER
    decimate_mod = obj.modifiers.new("DecimateMod", "DECIMATE")
    decimate_mod.ratio = 0.285

    # Ensure Smoothing
    for f in obj.data.polygons:
        f.use_smooth = True

    # Remove any Anisotropic textures
    for n in mat.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            for i in n.inputs:
                if i.name.startswith("Anisotropic"):
                    for link in i.links:
                        if link.from_node.type == "TEX_IMAGE":
                            mat.node_tree.nodes.remove(link.from_node)

    # EXPORT GLTF
    bpy.ops.export_scene.gltf(
        export_format="GLTF_SEPARATE",
        export_texture_dir="textures_TEMP",
        use_selection=True,
        export_apply=True,
        filepath=gltf_file,
    )

    # Delete new sphere
    bpy.data.objects.remove(obj, do_unlink=True)

    with open(gltf_file, "r") as json_file:
        gltf_data = json.load(json_file)

    old_arm_fn = None
    for p in gltf_data["images"]:
        if p["uri"].endswith("-" + slug + "_rough.png"):
            # Found Packed texture, Renamed to _arm
            old_arm_fn = os.path.basename(p["uri"])
            p["uri"] = "textures/" + slug + "_arm.png"
            break
        elif p["uri"].endswith(slug + "_rough.png"):
            # No packed texture found. Defaulted to using only roughness.
            p["uri"] = "textures/" + slug + "_rough.png"
            break

    with open(gltf_file, "w") as jsonfile:
        json.dump(gltf_data, jsonfile, indent=4)

    # RENAME PACKED FILE
    if old_arm_fn:
        old_arm = os.path.join(folder, "textures_TEMP", old_arm_fn)
        new_arm = os.path.join(folder, "textures", slug + "_arm.png")
        if not os.path.exists(new_arm):
            os.rename(old_arm, new_arm)


class HAT_OT_export_gltf(bpy.types.Operator):
    bl_idname = "hat.export_gltf"
    bl_label = "Export GLTF"
    bl_description = "Export this asset as a GLTF file as standard for uploading to polyhaven.com"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved

    def execute(cls, context):
        slug = get_slug()

        gltf_file = os.path.join(os.path.dirname(bpy.data.filepath), slug + ".gltf")

        if context.scene.hat_props.asset_type == "model":
            export_model(cls, context, slug, gltf_file)
        else:
            export_texture(cls, context, slug, gltf_file)

        try:
            rmtree(os.path.join(os.path.dirname(bpy.data.filepath), "textures_TEMP"))
        except FileNotFoundError:
            cls.report({"WARNING"}, "No textures exported")
        except PermissionError:
            cls.report({"WARNING"}, "Couldn't delete textures_TEMP folder")

        with open(gltf_file, "r") as json_file:
            data = json.load(json_file)

        errors = []
        for p in data["images"]:
            uri = p["uri"]
            uri = uri.replace("textures_TEMP", "textures")
            if uri.endswith("_png.png"):
                uri = uri.replace("_png.png", ".png")
            if uri.endswith("_rough.png"):
                uri = uri.replace("_rough.png", "_arm.png")
            if uri.endswith("-" + slug + "_arm.png"):
                # Turn slug_metal-slug_arm into slug_arm
                uri = "textures/" + slug + "_arm.png"

            fp = os.path.join(os.path.dirname(bpy.data.filepath), uri)
            if not os.path.exists(fp):
                errors.append(uri)

            p["uri"] = uri

        if errors:
            cls.report({"ERROR"}, "Image not found:\n" + "\n".join(errors))

        with open(gltf_file, "w") as f:
            json.dump(data, f, indent=4)

        return {"FINISHED"}
