from typing import Set
from bpy.types import Context
from bpy_extras.io_utils import ImportHelper
from bpy_extras.io_utils import ExportHelper
import bpy
import copy
from bpy.props import StringProperty, BoolProperty
import xml.etree.ElementTree as ET
from .ops import lst_p
import xml.dom.minidom
from mathutils import Quaternion

cloth_wk_list = []
cloth_wk_list_plus = []
cloth_wk_list_2 = []
cloth_wk_list_3 = []
cloth_wk_list_4 = []


class MyProperties(bpy.types.PropertyGroup):
    filepath_b: StringProperty(
        name="Xml File Path",
        subtype='NONE',

        default=''
    )  # type: ignore

    filepath_a: StringProperty(
        name="Xml File Path",
        subtype='NONE',

        default=''
    )  # type: ignore

    def invoke(self, context, event):
        if self.filepath_b:
            if not self.filepath_b.endswith('.xml'):
                self.report({'ERROR'}, "必须选择一个xml文件")
                return {'CANCELLED'}
            elif not self.filepath_a.endswith('.xml'):
                self.report({'ERROR'}, "必须选择一个xml文件")
                return {'CANCELLED'}

        return bpy.types.PropertyGroup.invoke(self, context, event)


class ImportXMLFileOperator_B(bpy.types.Operator, ImportHelper):
    """Import an XML file"""
    bl_idname = "wm.import_xml_file_b"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Import XML File_B"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # ImportHelper mixin class uses this
    filename_ext = ".xml"

    filter_glob: StringProperty(
        default="*.xml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be truncated.
    )  # type: ignore

    def execute(self, context):
        # The file path selected by the user
        filepath = self.filepath
        bpy.context.scene.my_properties.filepath_b = filepath

        global cloth_wk_list
        # 解析将要合并到的XML文件
        tree_1 = ET.parse(filepath)
        global root
        root = tree_1.getroot()
        global cloth_list
        global cloth_header

        cloth_list = root[2]   # 进入xml中的CLOTH_WK
        cloth_header = root[0]  # 获取header
        cloth_wk_list = []     # 该列表为具体的cloth_wk,储存每个字典

        # 将某些带空格的参照的空格保护起来
        gravityVec = cloth_header.find('gravityVec_')
        gravityVec.text = gravityVec.text.replace(' ', '@')

        # 遍历CLOTH_WK,将得到的每个名称分别存为每个字典
        for i in range(len(cloth_list)):
            cloth_dict = {}
            for x in range(len(cloth_list[i])):

                cloth_dict[cloth_list[i][x].tag] = cloth_list[i][x].text
                # 字典中添加一个原始骨骼名称的键
                cloth_dict['Ori_bone_name'] = cloth_list[i][1].text

            dict_mine = copy.deepcopy(cloth_dict)
            cloth_wk_list.append(dict_mine)

        # 对字典列表进行排序
        cloth_wk_list.sort(key=lambda x: int(x['no']))

        len_num = len(cloth_wk_list)

        self.report({'INFO'}, f"解析完成！ B得到{len_num}段骨骼物理参数。")

        return {'FINISHED'}


class ImportXMLFileOperator_A(bpy.types.Operator, ImportHelper):
    """Import an XML file"""
    bl_idname = "wm.import_xml_file_a"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Import XML File_A"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    # ImportHelper mixin class uses this
    filename_ext = ".xml"

    filter_glob: StringProperty(
        default="*.xml",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be truncated.
    )  # type: ignore

    def execute(self, context):
        # The file path selected by the user
        filepath = self.filepath
        bpy.context.scene.my_properties.filepath_a = filepath

        # 读取需要合并的xml文件
        tree_2 = ET.parse(filepath)
        root_2 = tree_2.getroot()

        cloth_list_2 = root_2[2]
        global cloth_wk_list_2
        cloth_wk_list_2 = []  # 每次执行存储前都进行列表清空

        for i in range(len(cloth_list_2)):
            cloth_dict = {}
            for x in range(len(cloth_list_2[i])):

                cloth_dict[cloth_list_2[i][x].tag] = cloth_list_2[i][x].text
                # 字典中添加一个骨骼名称的键
                cloth_dict['Ori_bone_name'] = cloth_list_2[i][1].text

            dict_mine = copy.deepcopy(cloth_dict)
            cloth_wk_list_2.append(dict_mine)

        # 对字典2列表进行排序
        cloth_wk_list_2.sort(key=lambda x: int(x['no']))

        len_num = len(cloth_wk_list_2)

        self.report({'INFO'}, f"解析完成！ A得到{len_num}段骨骼物理参数。")

        return {'FINISHED'}


class Remove_dup(bpy.types.Operator):
    bl_label = '合并去重处理xml'
    bl_idname = 'wm.remove_dup_ops'

    @classmethod
    def poll(cls, context):

        return cloth_wk_list_2 and cloth_wk_list

    def execute(self, context):
        cloth_wk_list_name = [i['no'] for i in cloth_wk_list]
        cloth_wk_list_2_name = [i['no'] for i in cloth_wk_list_2]

        same_bone = []
        append_bone = []
        unchange_bone = []
        for i in cloth_wk_list_2_name:
            if i in cloth_wk_list_name:
                same_bone.append(i)

            else:
                append_bone.append(i)

        for i in cloth_wk_list_name:
            if not (i in same_bone):
                unchange_bone.append(i)

        global cloth_wk_list_3
        cloth_wk_list_3 = []
        for i in same_bone:
            for y in cloth_wk_list_2:
                if i == y['no']:
                    num = cloth_wk_list_2.index(y)
                    for x in cloth_wk_list:
                        if i == x['no']:
                            num2 = cloth_wk_list.index(x)
                            new_dict = {
                                **cloth_wk_list[num2], **cloth_wk_list_2[num]}
                            cloth_wk_list_3.append(new_dict)

        for i in unchange_bone:
            for y in cloth_wk_list:
                if i == y['no']:
                    num = cloth_wk_list.index(y)
                    cloth_wk_list_3.append(cloth_wk_list[num])

        cloth_wk_list_3.sort(key=lambda x: int(x['no']))

        for i in append_bone:
            for y in cloth_wk_list_2:
                if i == y['no']:
                    num = cloth_wk_list_2.index(y)
                    cloth_wk_list_3.append(cloth_wk_list_2[num])

        cloth_wk_list_3.sort(key=lambda x: int(x['no']))

        len_num = len(cloth_wk_list_3)

        self.report({'INFO'}, f"处理完成！ 合并后有{len_num}段骨骼物理参数。")

        return {'FINISHED'}


class Add_custom_attr(bpy.types.Operator):
    bl_idname = "wm.add_custom_attr"
    bl_label = "Add_custom_attr"
    # bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):

        return cloth_wk_list_3 or cloth_wk_list

    def execute(self, context):
        obj = bpy.context.object
        add_finish = 0
        # 检查对象是否是骨架
        if obj and obj.type == 'ARMATURE':
            # 进入姿态模式
            bpy.ops.object.mode_set(mode='POSE')
            if cloth_wk_list_3:
                bone_data = cloth_wk_list_3

            else:
                bone_data = cloth_wk_list
            # 迭代每个字典并添加自定义属性
            for data in bone_data:
                bone_name = '_' + data['no']
                if bone_name in obj.pose.bones:
                    add_finish += 1
                    for i in data.keys():

                        custom_value = data.get(i, None)  # 获取自定义属性值
                        if custom_value.find(' ') >= 0:
                            # 拆分四元数字符串为四个浮点数
                            values = custom_value.split(' ')
                            quaternion = Quaternion((float(values[0]), float(
                                values[1]), float(values[2]), float(values[3])))
                            # 添加新属性
                            pose_bone = obj.pose.bones[bone_name]
                            pose_bone[i] = quaternion

                        else:
                            pose_bone = obj.pose.bones[bone_name]
                            if custom_value is not None:
                                pose_bone[i] = custom_value
                else:
                    notfound = bone_name.replace('_', '')
                    self.report(
                        {"WARNING"}, f"clp文件中骨骼名为 '{notfound}' 在骨架中未找到")
                    print(
                        f"Bone named '{notfound}' not found in the armature.")

            # 返回对象模式
            # bpy.ops.object.mode_set(mode='OBJECT')
            print('finished')
            self.report({"INFO"}, f"已经为{add_finish}段骨骼添加了物理属性。")
            return {"FINISHED"}
        else:
            self.report({"ERROR"}, '所选物体不是骨架')
            print("Active object is not an armature.")
            return {'CANCELLED'}


class ExportXMLFileOperator(bpy.types.Operator, ExportHelper):
    """Export modified XML file"""
    bl_idname = "wm.export_xmlfile_ops"
    bl_label = "Export XML File"
    # bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".xml"

    filter_glob: StringProperty(
        default="*.xml",
        options={'HIDDEN'},
        maxlen=255,
    )  # type: ignore

    @classmethod
    def poll(cls, context):
        b = False
        if (cloth_wk_list_3 and cloth_list) or cloth_wk_list:
            b = True

        return b

    def change_dict_user(a):
        obj = bpy.context.object

        global cloth_wk_list_4

        for i in obj.pose.bones[:]:
            try:
                i['no']

            except KeyError:
                pass

            else:

                for x in a:
                    if i['Ori_bone_name'] == x['Ori_bone_name']:
                        new_offset = ExportXMLFileOperator.format_float_list(
                            list(i['offset']))
                        num = a.index(x)

                        num2 = obj.pose.bones[:].index(i)
                        obj.pose.bones[num2]['offset_1'] = new_offset
                        new_dict = {**a[num], **obj.pose.bones[num2]}
                        cloth_wk_list_4.append(new_dict)

        cloth_wk_list_4.sort(key=lambda x: int(x['no']))

    def change_dict_only_B(a):
        obj = bpy.context.object

        global cloth_wk_list_plus

        for i in obj.pose.bones[:]:
            try:
                i['no']

            except KeyError:
                pass

            else:

                for x in a:
                    if i['Ori_bone_name'] == x['Ori_bone_name']:
                        new_offset = ExportXMLFileOperator.format_float_list(
                            list(i['offset']))
                        num = a.index(x)

                        num2 = obj.pose.bones[:].index(i)
                        obj.pose.bones[num2]['offset_1'] = new_offset
                        new_dict = {**a[num], **obj.pose.bones[num2]}
                        cloth_wk_list_plus.append(new_dict)

        cloth_wk_list_plus.sort(key=lambda x: int(x['no']))

    def format_float_list(float_list):
        formatted_list = []
        for num in float_list:
            formatted_num = '{:.6f}'.format(num)  # 格式化浮点数，保留六位小数
            formatted_list.append(formatted_num)

        result = ' '.join(formatted_list)  # 以空格连接所有元素
        return result

    def execute(self, context):
        global cloth_list
        # 检查对象是否是骨架
        obj = bpy.context.object
        if obj and obj.type == 'ARMATURE' and cloth_wk_list_3:
            ExportXMLFileOperator.change_dict_user(cloth_wk_list_3)

        elif obj and obj.type == 'ARMATURE' and cloth_wk_list:
            ExportXMLFileOperator.change_dict_only_B(cloth_wk_list)

        else:
            self.report({"ERROR"}, '所选物体不是骨架')
            print("Active object is not an armature.")
            return {'CANCELLED'}
        # 导出更改
        # 对于所有更改一次性全部写入
        global cloth_wk_list_4
        global cloth_wk_list_plus
        # 判断是否只有主文件单个被导入
        if cloth_wk_list_4 and cloth_wk_list_2:
            export_lst = cloth_wk_list_4

        elif not cloth_wk_list_2:
            export_lst = cloth_wk_list_plus

        elif not cloth_wk_list_4:
            export_lst = cloth_wk_list_3

        else:
            self.report({"ERROR"}, "同时导入了文件A却没有进行合并，无法确定是否导出主文件B。需要取消对A的解析")
            return {'CANCELLED'}

        for y in range(len(cloth_wk_list)):
            for i in list(export_lst[y].keys()):
                if i == 'offset_1':
                    key = cloth_list[y].find('offset')
                    key.text = export_lst[y]['offset_1']
                elif i == 'offset':
                    pass
                else:
                    key = cloth_list[y].find(i)
                    if key != None:
                        key.text = export_lst[y][i]

        # 检查是否超出合并到的clp,超出则增添新的子元素
        if len(cloth_wk_list) < len(export_lst):
            for y in range(len(cloth_wk_list), len(export_lst)):

                new_clp_bone = ET.SubElement(cloth_list, 'CLOTH_WK')
                for i in lst_p:
                    ET.SubElement(new_clp_bone, i)

                for i in list(export_lst[y].keys()):
                    if i == 'offset_1':
                        key = cloth_list[y].find('offset')
                        key.text = export_lst[y]['offset_1']
                    elif i == 'offset':
                        pass
                    else:
                        key = cloth_list[y].find(i)
                        if key != None:
                            key.text = export_lst[y][i]

        # 同时修改物理骨骼计数
        key = root.find('CLOTH_WK_NUM')
        key.text = str(len(export_lst))

        # print(cloth_list[0].find('offset'))
        for i in cloth_list:
            offset = i.find('offset')
            offset.text = str(offset.text).replace(' ', '@')

        # 将XML转换为字符串
        xml_str = ET.tostring(root, encoding='unicode', method='xml')

        # 去除所有换行和缩进（取消原来的所有格式化）
        xml_str_no_format = ''.join(xml_str.split())

        # 重新格式化
        dom = xml.dom.minidom.parseString(xml_str_no_format)
        formatted_xml = dom.toprettyxml()
        formatted_xml = formatted_xml.replace('@', ' ')  # 将空格还原

        # 导出修改后的xml文件
        with open(self.filepath, 'w', encoding='utf-8') as file:
            file.write(formatted_xml)

        self.report({'INFO'}, f"XML file saved at: {self.filepath}")
        if export_lst == cloth_wk_list_4:
            cloth_wk_list_4 = []
        if export_lst == cloth_wk_list_plus:
            cloth_wk_list_plus = []
        return {'FINISHED'}


class del_fileA_list(bpy.types.Operator):
    bl_label = '删除对于文件A的解析'
    bl_idname = 'del_lst.del_ops'

    @classmethod
    def poll(cls, context):

        return cloth_wk_list_2 or bpy.context.scene.my_properties.filepath_a

    def execute(self, context):
        global cloth_wk_list_2
        global cloth_wk_list_3

        cloth_wk_list_2 = []
        cloth_wk_list_3 = []
        bpy.context.scene.my_properties.filepath_a = ''

        return {'FINISHED'}


class del_fileB_list(bpy.types.Operator):
    bl_label = '删除对于文件B的解析'
    bl_idname = 'del_lst_2.del_ops2'

    @classmethod
    def poll(cls, context):

        return cloth_wk_list or bpy.context.scene.my_properties.filepath_b

    def execute(self, context):
        global cloth_wk_list

        cloth_wk_list = []

        bpy.context.scene.my_properties.filepath_b = ''

        return {'FINISHED'}
