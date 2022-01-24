import bpy
import json
import os
from shutil import rmtree


class HAT_OT_export_gltf(bpy.types.Operator):
    bl_idname = "hat.export_gltf"
    bl_label = "Export GLTF"
    bl_description = "Export this file as a GLTF file as standard for uploading to polyhaven.com"

    @classmethod
    def poll(cls, context):
        return bpy.data.is_saved and context.scene.hat_props.asset_type == 'model'

    def execute(self, context):
        slug = bpy.path.display_name_from_filepath(bpy.data.filepath)

        try:
            collection = bpy.data.collections[slug]
        except KeyError:
            self.report({'ERROR'}, "No collection named " + slug)
            return {'CANCELLED'}

        for o in bpy.data.objects:
            o.select_set(o in list(collection.objects))

        gltf_file = os.path.join(os.path.dirname(
            bpy.data.filepath), slug + '.gltf')

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
            self.report({'WARNING'}, "No textures exported")

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
            self.report({'ERROR'}, "Image not found:\n" + '\n'.join(errors))

        with open(gltf_file, 'w') as f:
            json.dump(data, f, indent=4)

        return {'FINISHED'}
