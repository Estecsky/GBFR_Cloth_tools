from typing import Set
import bpy
from bpy.types import Context


lst_p = ['dataVersion_', 'no', 'noUp', 'noDown', 'noSide', 'noPoly', 'noFix', 'rotLimit', 'friction', 'gravityBlendRate_', 'offset',
         'originalRate_', 'weight_', 'thick_', 'windForceArea_', 'jointScale_', 'bAllowChangeScale_', 'axisAdjustRate_']


class add_prefix_hex(bpy.types.Operator):
    bl_label = 'Add_prefix_hex'
    bl_description = '添加进制16进制前缀'
    bl_idname = 'add_prefix_hex.add_ops'

    # bl_options = {"REGISTER", "UNDO", }

    # prefix: bpy.props.EnumProperty(items=(
    #     ('hex', '16进制', '添加16进制前缀', 0), ('dec', '10进制', '添加10进制前缀', 1)), name='添加进制标记')  # type: ignore

    def execute(self, context):
        arm_obj = bpy.context.object

        if arm_obj.type != 'ARMATURE':
            print('所选物体不是骨架物体！！！')
            self.report({"ERROR"}, "所选物体不是骨架物体！！！")
            return {'CANCELLED'}

        arm_data = arm_obj.data
        arm_bones = arm_data.bones
        
        if arm_bones[0].name.startswith('_hex_'):
            pass
        elif arm_bones[0].name.startswith('_dec_'):

            for i in arm_bones:
                c = i.name.replace('_dec_', '')
                i.name = '_hex_' + c
        else:
            for i in arm_bones:
                c = i.name.replace('_', '')
                i.name = '_hex_' + c
                
                
       

        return {'FINISHED'}
    
class add_prefix_dec(bpy.types.Operator):
    bl_label = 'Add_prefix_dec'
    bl_description = '添加进制10进制前缀'
    bl_idname = 'add_prefix_dec.add_ops'
    
    def execute(self, context):
        arm_obj = bpy.context.object

        if arm_obj.type != 'ARMATURE':
            print('所选物体不是骨架物体！！！')
            self.report({"ERROR"}, "所选物体不是骨架物体！！！")
            return {'CANCELLED'}

        arm_data = arm_obj.data
        arm_bones = arm_data.bones
        
        if arm_bones[0].name.startswith('_dec_'):
            pass
        elif arm_bones[0].name.startswith('_hex_'):
            for i in arm_bones:
                c = i.name.replace('_hex_', '')
                i.name = '_dec_' + c
        else:
            for i in arm_bones:
                c = i.name.replace('_', '')
                i.name = '_dec_' + c
                
        return {'FINISHED'}


class cancel_prefix(bpy.types.Operator):
    bl_label = 'cancel_prefix'
    bl_description = '去掉进制前缀'
    bl_idname = 'cancel_prefix.cancel_ops'

    def execute(self, context):

        arm_obj = bpy.context.object

        if arm_obj.type != 'ARMATURE':  # 判断是否选的是骨架物体
            print('所选物体不是骨架物体！！！')
            self.report({"ERROR"}, "所选物体不是骨架物体！！！")
            return {'CANCELLED'}

        arm_data = arm_obj.data
        arm_bones = arm_data.bones  # 获取骨架物体数据里的骨骼信息

        if arm_bones[0].name.startswith('_hex_'):
            for i in arm_bones:
                c = i.name.replace('_hex_', '')
                i.name = '_' + c

        elif arm_bones[0].name.startswith('_dec_'):
            for i in arm_bones:
                c = i.name.replace('_dec_', '')
                i.name = '_' + c

        else:
            self.report({'ERROR'}, '骨骼名称没有进制前缀标记！！')
            return {'CANCELLED'}

        return {'FINISHED'}


class hex2decimal(bpy.types.Operator):
    bl_label = 'hex2decimal_bone'
    bl_description = '将骨骼16进制名称转为10进制'
    bl_idname = 'hex2deciaml.ops1'

    def execute(self, context):

        arm_obj = bpy.context.object
        arm_data = arm_obj.data

        arm_bones = arm_data.bones

        if arm_bones[0].name.find('_hex_') == 0:

            for i in arm_bones:

                c = i.name.replace('_hex_', '')
                b = str((int(c, 16)))
                i.name = '_dec_' + b

        else:
            self.report({'ERROR'}, '转换前没有添加进制前缀或为十进制前缀')
            return {'CANCELLED'}

        return {'FINISHED'}


class decimal2hex(bpy.types.Operator):
    bl_label = 'decimal2hex_bone'
    bl_description = '将骨骼10进制名称转为16进制'
    bl_idname = 'decimal2hex.ops1'

    def execute(self, context):

        arm_obj = bpy.context.object
        arm_data = arm_obj.data

        arm_bones = arm_data.bones

        if arm_bones[0].name.find('_dec_') == 0:

            for i in arm_bones:

                c = i.name.replace('_dec_', '')
                b = hex(int(c))[2:]
                i.name = '_hex_' + b.zfill(3)

        else:
            self.report({'ERROR'}, '转换前没有添加进制前缀或为十六进制前缀')
            return {'CANCELLED'}

        return {'FINISHED'}

class Batch_apply(bpy.types.Operator):
    bl_label = 'batch_apply_names'
    bl_description = '将所有骨骼名称前两位应用更改'
    bl_idname = 'batch_apply.ops_apply'

    @classmethod
    def poll(cls, context: Context):
        from .ui import apply_bool
        a = bpy.context.object
        
        return a.type == 'ARMATURE' and apply_bool
    
    def execute(self, context: Context):
        
        a = bpy.context.scene.my_properties
        name_two = a.name_bones
        b = bpy.context.object
        bone_names = b.data.bones
        for x in bone_names:
            ori_name = x.name.replace('_', '')
            new_name = '_'+ name_two + ori_name[2:]
            x.name = new_name
            
        return {'FINISHED'}
