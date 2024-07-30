import bpy
from .ops import add_prefix_hex, add_prefix_dec, cancel_prefix, hex2decimal, decimal2hex, Batch_apply, Select_attr
from .ops import RemoveEmpty, RemoveUnusedBones
from .ops import lst_p
from bpy.types import Context
# from bpy_extras.io_utils import ImportHelper
from .xml_oi import ImportXMLFileOperator_B, ImportXMLFileOperator_A, Remove_dup, ExportXMLFileOperator, Add_custom_attr
from .xml_oi import del_fileA_list, del_fileB_list
from .Phy_param_ops import Change_all_dict_name, ALL_change_all_dict_name

apply_bool = True
class Convert_f(bpy.types.Panel):
    # 标签
    bl_label = '骨骼名称进制转换'  # 面板显示名称
    bl_idname = 'GBFR_mod_cloth_tools_convert'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator(hex2decimal.bl_idname, text='16转10进制')
        row.operator(decimal2hex.bl_idname, text='10转16进制')


class Prefix_Panel(bpy.types.Panel):
    # 标签
    bl_label = '进制前缀标记'  # 面板显示名称
    bl_idname = 'GBFR_mod_cloth_tools'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        col = layout.column()
        row.operator(add_prefix_hex.bl_idname, text='添加16进制前缀')
        row.operator(add_prefix_dec.bl_idname, text='添加10进制前缀')
        col.operator(cancel_prefix.bl_idname, text='去掉前缀')


class Import_Export_Xml(bpy.types.Panel):
    # 标签
    bl_label = 'clp文件预处理'  # 面板显示名称
    bl_idname = 'ImportExportXml'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"

    def draw(self, context):
        layout = self.layout
        props = context.scene.my_properties
        col = layout.column()
        col.label(text="A==>B")
        box = layout.box()
        box.label(text='1.导入将要被合并到的文件B')
        box_row = box.row()
        box_row.operator(ImportXMLFileOperator_B.bl_idname,
                         text='导入文件B', icon='IMPORT')
        box_row.operator(del_fileB_list.bl_idname, text='', icon='TRASH')
        box.prop(props, "filepath_b", text='B文件路径', emboss=False)
        box = layout.box()
        box.label(text='2.导入要合并的clp文件A')
        box_row = box.row()
        box_row.operator(ImportXMLFileOperator_A.bl_idname,
                         text='导入文件A', icon='IMPORT')
        box_row.operator(del_fileA_list.bl_idname, text='', icon='TRASH')
        box.prop(props, "filepath_a", text='A文件路径', emboss=False)
        box = layout.box()
        box.label(text='3.进行文件去重合并')
        box.operator(Remove_dup.bl_idname, text='去重合并', icon='FILE_VOLUME')
        box = layout.box()
        box.label(text='4.为骨骼添加自定义物理属性（注意必须为十进制名称）')
        box.operator(Add_custom_attr.bl_idname,
                     text='添加物理属性', icon='SEQ_CHROMA_SCOPE')

        # box.prop(props, "number")
        # box.prop(props, "boolean")

class Batch_modify_bone_name(bpy.types.Panel):
    # 标签
    bl_label = '批量修改骨骼名称（必须十进制且无前缀）'  # 面板显示名称
    bl_idname = 'Modify_name'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"
    
    def draw(self, context):
        layout = self.layout
        name_lst = []
        a = bpy.context.object 
        col = layout.column()
        global apply_bool
        col.label(text='选择一个骨架。')
        if a.type == 'ARMATURE':    
            same_num = 0
            b = a.data.bones

            for x in b:
                name = x.name.replace('_', '')
                name_lst.append(name)
            first_two = name_lst[0][0:2]
            for y in name_lst:
                name_two = y[0:2]
                # print(name_two)
                if first_two == name_two:
                    same_num =same_num + 1
            if same_num == len(name_lst):
                box = layout.box()
                box.label(text=f'该骨架名称有{len(name_lst)}段骨骼前两位数统一为： {first_two}')
                apply_bool = True
                
                # box = layout.box()
                # box.label(text=f'该骨架名称有{len(name_lst)}段骨骼前两位数统一为： {first_two}')
                
            else:
                box = layout.box()
                box.label(text='该骨架名称前两位数不统一。')
                apply_bool = False
            
        else:
            box = layout.box()
            box.label(text='所选物体不是骨架。')
        row = layout.row()
        props = context.scene.my_properties
        row.prop(props,'name_bones',text='将其改为')
        row.operator(Batch_apply.bl_idname,text='应用名称更改',icon='CHECKMARK')
            
        
        

class Phy_parem_UI(bpy.types.Panel):
    # 标签
    bl_label = '物理参数'  # 面板显示名称
    bl_idname = 'Phy_parem_UI'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"

    def draw(self, context):
        layout = self.layout
        col = layout.column()

        act_pose_bone = bpy.context.active_pose_bone

        if act_pose_bone:
            col.label(text="物理骨骼参数")
            row = layout.row()

            try:
                act_pose_bone['no']

            except KeyError:
                box = layout.box()
                box.label(text='该骨骼没有写入物理参数')
            else:
                box = layout.box()
                for key in lst_p:
                    box.prop(act_pose_bone, f'["{key}"]')

        else:
            col.label(text="进入姿态模式下选择任意骨骼")
        if act_pose_bone:
            row.prop(act_pose_bone, 'name')
            row.operator(Change_all_dict_name.bl_idname,
                         text='应用更改', icon='CHECKMARK')
            row.operator(ALL_change_all_dict_name.bl_idname, text='应用所有更改', icon='SELECT_DIFFERENCE')


class ExportModifiedXml(bpy.types.Panel):
    # 标签
    bl_label = '导出'  # 面板显示名称
    bl_idname = 'ExportModified_Xml'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.operator(ExportXMLFileOperator.bl_idname,
                     text='导出修改后的clp文件', icon='EXPORT')
        
class Miscellaneous(bpy.types.Panel):
    # 标签
    bl_label = '杂项'  # 面板显示名称
    bl_idname = 'Miscellaneous_UI'
    # 面板所属区域
    bl_space_type = "VIEW_3D"
    # 显示面板的地方
    bl_region_type = "UI"
    # 显示面板的地方的归类
    bl_category = "cloth_tools"
    
    def draw(self, context: Context):
        layout = self.layout
        col = layout.column()
        
        col.operator(Select_attr.bl_idname,
                     text='全选所有物理骨骼')
        col.operator(RemoveEmpty.bl_idname,
                     text='移除空顶点组')
        col.operator(RemoveUnusedBones.bl_idname,
                     text='移除未使用骨骼')
