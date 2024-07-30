# import sys
# path = (r'C:\Users\apsur\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\addons\GBFR_Cloth_tools')
# sys.path.append(path)


from .ops import add_prefix_hex, add_prefix_dec, cancel_prefix, hex2decimal, decimal2hex, Batch_apply, Select_attr, RemoveEmpty, RemoveUnusedBones
from .ui import Convert_f, Prefix_Panel, Import_Export_Xml, Phy_parem_UI, ExportModifiedXml, Batch_modify_bone_name, Miscellaneous
from .Phy_param_ops import Change_all_dict_name, ALL_change_all_dict_name
from .xml_oi import MyProperties, ImportXMLFileOperator_B, ImportXMLFileOperator_A, Remove_dup, ExportXMLFileOperator, Add_custom_attr
from .xml_oi import del_fileA_list, del_fileB_list
from bpy.props import PointerProperty
import bpy


bl_info = {
    "name": "GBFR_cloth_Addon",
    "author": "Estecsky",
    "description": "测试中",
    "blender": (3, 4, 0),  # 插件所支持的blender版本
    "location": "3D视图 > 侧边栏",  # 插件显示的位置
    "warning": "插件处于测试阶段",    # 警告信息
    "category": "3D View",  # 归类信息 搜索插件的时候显示的分类
    "version": (0, 5, 0)
}


lst = [add_prefix_hex, add_prefix_dec, cancel_prefix, hex2decimal, Change_all_dict_name, MyProperties, del_fileA_list,
       ImportXMLFileOperator_B, ImportXMLFileOperator_A, Remove_dup, ExportXMLFileOperator, Add_custom_attr, del_fileB_list, ALL_change_all_dict_name,
       Batch_apply, Select_attr, RemoveEmpty, RemoveUnusedBones,
       decimal2hex, Import_Export_Xml, Miscellaneous, Prefix_Panel, Convert_f, Batch_modify_bone_name, Phy_parem_UI, ExportModifiedXml]


# def reset_filepath_properties(scene):
#     scene.my_properties.filepath_b = ""
#     scene.my_properties.filepath_a = ""


def register():
    for i in lst:
        bpy.utils.register_class(i)

    bpy.types.Scene.my_properties = PointerProperty(type=MyProperties)

    #bpy.app.handlers.load_post.append(reset_filepath_properties)
    # bpy.context.scene.my_properties.filepath_a = ''
    # bpy.context.scene.my_properties.filepath_b = ''



def unregister():
    for i in lst:
        bpy.utils.unregister_class(i)

    del bpy.types.Scene.my_properties
    #bpy.app.handlers.load_post.remove(reset_filepath_properties)


if __name__ == "__main__":
    register()
