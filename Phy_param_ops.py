import bpy
from bpy.types import Operator, Context

num = 0
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

class ALL_change_all_dict_name(Operator):
    bl_label = 'all_Change_all_dict_name'
    bl_description = '应用全部更改并替换所有其他骨骼参数中出现的各个原始名称'
    bl_idname = 'all_change_dict.ops'

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
    
    def execute(self, context: Context):
        a = bpy.context.object.pose.bones
        global num
        for x in a:
            if x.name.startswith('_dec_') or x.name.startswith('_hex_'):
                self.report({'ERROR'},'名称不应该有进制前缀')
                
                return {'CANCELLED'}
            
            elif x.name.endswith('4095'):
                self.report({'ERROR'},'名称不可为4095,4095意为无')
                
                return {'CANCELLED'}
            else:
                try:
                    x['no']
                except KeyError:
                    pass
                else:
                    ori_name = x.name.replace('_', '')
                    if x['no'] == ori_name :
                        pass
                    else:
                        Change_all_dict_name.change_all_name(x)
                        num = num + 1
                    
        self.report({'INFO'}, f'名称批量修改完成，应用了{num}段骨骼更改')
        num = 0
        return {'FINISHED'}