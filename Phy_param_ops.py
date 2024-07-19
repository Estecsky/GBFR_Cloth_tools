import bpy
from bpy.types import Operator, Context


class Change_all_dict_name(Operator):
    bl_label = 'Change_all_dict_name'
    bl_description = '应用更改并替换所有其他骨骼参数中出现的该名称'
    bl_idname = 'change_dict.ops'

    @classmethod
    def poll(cls, context: Context):
        a = bpy.context.active_pose_bone

        try:
            a['no']
        except KeyError:
            b = False
        else:
            b = True
        return bpy.context.mode == 'POSE' and b

    def change_all_name(a):
        lst = ['noUp', 'noDown', 'noSide', 'noPoly', 'noFix']
        ori_name = a['no']
        b = bpy.context.object.pose.bones
        change_name = a.name.replace('_', '')
        a['no'] = change_name
        for i in b:
            try:
                i['no']
            except KeyError:
                pass
            else:
                for x in lst:
                    if i[x] == ori_name:
                        i[x] = change_name

    def execute(self, context: Context):
        a = bpy.context.active_pose_bone
        if a.name.startswith('_dec_') or a.name.startswith('_hex_'):
            self.report({'ERROR'},'名称不应该有进制前缀')
            
            return {'CANCELLED'}
        
        elif a.name.endswith('4095'):
            self.report({'ERROR'},'名称不可为4095,4095意为无')
            
            return {'CANCELLED'}
        else:
            
            Change_all_dict_name.change_all_name(a)
            self.report({'INFO'}, '骨骼名称批量修改完成')

            return {'FINISHED'}
