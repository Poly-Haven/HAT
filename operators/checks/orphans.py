from xmlrpc.client import DateTime
import bpy


def check(slug):
    result = "SUCCESS"
    messages = []

    for data_type in dir(bpy.data):
        if hasattr(getattr(bpy.data, data_type), '__iter__'):
            l = list(getattr(bpy.data, data_type))
            for item in l:
                if not hasattr(item, 'users'):
                    continue
                if item.users == 0:
                    dt_name = (data_type[:-2]
                               if data_type.endswith('es')
                               else data_type[:-1]
                               if data_type.endswith('s')
                               else data_type).replace('_', ' ')
                    result = 'ERROR'
                    messages.append(
                        f'Unused {dt_name}: {item.name}')

    return result, messages
