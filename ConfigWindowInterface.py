import xml.etree.ElementTree

import Libs

from PySide6.QtWidgets import QDialog, QFileDialog
from PySide6.QtGui import QIcon

from Style import StyleSheets, Fonts, Labels, WarningLabels

from ui_form import Ui_Form


class ConfigWindow(QDialog):
    def __init__(self):
        super(ConfigWindow, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.style_window()
        self.style_labels()
        self.add_functions_to_buttons()


    def add_functions_to_buttons(self):
        self.ui.OpenATemp.clicked.connect(self.open_template)
        self.ui.pushButton.clicked.connect(self.create_config_file)


    def style_window(self):
        self.setWindowTitle('Rotating Coils')
        self.setWindowIcon(QIcon('winIcon.png'))
        StyleSheets.stylesheet_central_widget(self)


    def style_labels(self):
        self.ui.label.setFont(Fonts.bigger_headers())
        self.ui.label_11.setFont(Fonts.bigger_headers())
        self.ui.label_19.setFont(Fonts.bigger_headers())
        self.ui.label_2.setFont(Fonts.small_headers())
        self.ui.label_12.setFont(Fonts.small_headers())
        self.ui.label_20.setFont(Fonts.small_headers())
        self.ui.label_3.setFont(Fonts.small_headers())
        self.ui.label_13.setFont(Fonts.small_headers())
        self.ui.label_21.setFont(Fonts.small_headers())
        self.ui.label_6.setFont(Fonts.small_headers())
        self.ui.label_14.setFont(Fonts.small_headers())
        self.ui.label_22.setFont(Fonts.small_headers())
        self.ui.label_4.setFont(Fonts.small_headers())
        self.ui.label_5.setFont(Fonts.small_headers())
        self.ui.label_7.setFont(Fonts.small_headers())
        self.ui.label_8.setFont(Fonts.small_headers())
        self.ui.label_15.setFont(Fonts.small_headers())
        self.ui.label_16.setFont(Fonts.small_headers())
        self.ui.label_17.setFont(Fonts.small_headers())
        self.ui.label_18.setFont(Fonts.small_headers())
        self.ui.label_23.setFont(Fonts.small_headers())
        self.ui.label_24.setFont(Fonts.small_headers())
        self.ui.label_25.setFont(Fonts.small_headers())
        self.ui.label_26.setFont(Fonts.small_headers())
        self.ui.label_9.setFont(Fonts.small_headers())
        self.ui.label_10.setFont(Fonts.small_headers())
        self.ui.MiddleRadiusSmall.setFont(Fonts.button_text())
        self.ui.MiddleRadiusLarge.setFont(Fonts.button_text())
        self.ui.LayerNumber1.setFont(Fonts.button_text())
        self.ui.LayerNumber2.setFont(Fonts.button_text())
        self.ui.LayerNumber3.setFont(Fonts.button_text())
        self.ui.TurnsNumber1.setFont(Fonts.button_text())
        self.ui.TurnsNumber2.setFont(Fonts.button_text())
        self.ui.TurnsNumber3.setFont(Fonts.button_text())
        self.ui.InnerRadius1.setFont(Fonts.button_text())
        self.ui.InnerRadius2.setFont(Fonts.button_text())
        self.ui.InnerRadius3.setFont(Fonts.button_text())
        self.ui.OuterRadius1.setFont(Fonts.button_text())
        self.ui.OuterRadius2.setFont(Fonts.button_text())
        self.ui.OuterRadius3.setFont(Fonts.button_text())
        self.ui.CoilsType1.setFont(Fonts.button_text())
        self.ui.CoilsType2.setFont(Fonts.button_text())
        self.ui.CoilsType3.setFont(Fonts.button_text())
        self.ui.Type1.setFont(Fonts.button_text())
        self.ui.Type2.setFont(Fonts.button_text())
        self.ui.Type3.setFont(Fonts.button_text())
        self.ui.Length1.setFont(Fonts.button_text())
        self.ui.Length2.setFont(Fonts.button_text())
        self.ui.Length3.setFont(Fonts.button_text())
        Labels.output(self.ui.label_27)
        WarningLabels.style_1(self.ui.label_37)
        self.ui.label_37.setFont(Fonts.button_text())
        WarningLabels.style_2(self.ui.label_36)


    def open_template(self):
        template_path, _ = QFileDialog.getOpenFileName(self)
        self.ui.label_27.setText(template_path)


    def get_coil_type(self):
        coil_type = []
        if self.ui.CoilsType1.currentRow() == 0:
            coil_type.append('QuadrupoleCoil')
        elif self.ui.CoilsType1.currentRow() == 1:
            coil_type.append('QuadrupoleCompensationCoil')
        else:
            coil_type.append(None)

        if self.ui.CoilsType2.currentRow() == 0:
            coil_type.append('QuadrupoleCoil')
        elif self.ui.CoilsType2.currentRow() == 1:
            coil_type.append('QuadrupoleCompensationCoil')
        else:
            coil_type.append(None)

        if self.ui.CoilsType3.currentRow() == 0:
            coil_type.append('QuadrupoleCoil')
        elif self.ui.CoilsType3.currentRow() == 1:
            coil_type.append('QuadrupoleCompensationCoil')
        else:
            coil_type.append(None)

        return coil_type


    def get_type(self):
        config_type = []
        if self.ui.Type1.currentRow() == 0:
            config_type.append('Axial')
        elif self.ui.Type1.currentRow() == 1:
            config_type.append('Radial')
        else:
            config_type.append(None)

        if self.ui.Type2.currentRow() == 0:
            config_type.append('Axial')
        elif self.ui.Type2.currentRow() == 1:
            config_type.append('Radial')
        else:
            config_type.append(None)

        if self.ui.Type3.currentRow() == 0:
            config_type.append('Axial')
        elif self.ui.Type3.currentRow() == 1:
            config_type.append('Radial')
        else:
            config_type.append(None)

        return config_type


    def get_length(self):
        length = []
        if self.ui.Length1.currentRow() == 0:
            length.append(1)
        elif self.ui.Length1.currentRow() == 1:
            length.append(0.5)
        else:
            length.append(None)

        if self.ui.Length2.currentRow() == 0:
            length.append(1)
        elif self.ui.Length2.currentRow() == 1:
            length.append(0.5)
        else:
            length.append(None)

        if self.ui.Length3.currentRow() == 0:
            length.append(1)
        elif self.ui.Length3.currentRow() == 1:
            length.append(0.5)
        else:
            length.append(None)

        return length


    def get_number_of_layers(self):
        layer_number = []
        while True:
            try:
                layer_number.append(int(self.ui.LayerNumber1.text()))
                break
            except ValueError:
                self.ui.label_36.setText(f'Number of Layers for 1 coil is empty')
                break

        while True:
            try:
                layer_number.append(int(self.ui.LayerNumber2.text()))
                break
            except ValueError:
                self.ui.label_36.setText(f'Number of Layers for 2 coil is empty')
                break

        while True:
            try:
                layer_number.append(int(self.ui.LayerNumber3.text()))
                break
            except ValueError:
                self.ui.label_36.setText(f'Number of Layers for 3 coil is empty')
                break

        return layer_number


    def get_number_of_turns(self):
        turns_number = []
        while True:
            try:
                turns_number.append(int(self.ui.TurnsNumber1.text()))
                break
            except ValueError:
                self.ui.label_36.setText(f'Number of Turns for 1 coil is empty')
                break

        while True:
            try:
                turns_number.append(int(self.ui.TurnsNumber2.text()))
                break
            except ValueError:
                self.ui.label_36.setText(f'Number of Turns for 2 coil is empty')
                break

        while True:
            try:
                turns_number.append(int(self.ui.TurnsNumber3.text()))
                break
            except ValueError:
                self.ui.label_36.setText(f'Number of Turns for 3 coil is empty')
                break

        return turns_number


    def get_inner_radius(self):
        inner_radius = [(self.ui.InnerRadius1.text().split(',')), (self.ui.InnerRadius2.text().split(',')),
                        (self.ui.InnerRadius3.text().split(','))]
        for j in range(3):
            for i in range(len(inner_radius[j])):
                while True:
                    try:
                        inner_radius[j][i] = int(inner_radius[j][i])
                        break
                    except ValueError:
                        break

        return inner_radius


    def get_outer_radius(self):
        outer_radius = [(self.ui.OuterRadius1.text().split(',')), (self.ui.OuterRadius2.text().split(',')),
                        (self.ui.OuterRadius3.text().split(','))]
        for j in range(3):
            for i in range(len(outer_radius[j])):
                while True:
                    try:
                        outer_radius[j][i] = int(outer_radius[j][i])
                        break
                    except ValueError:
                        break

        return outer_radius


    def get_middle_radius_large(self):
        while True:
            try:
                middle_radius_large = self.ui.MiddleRadiusLarge.text().split(',')
                for i in range(len(middle_radius_large)):
                    middle_radius_large[i] = int(middle_radius_large[i])
                break
            except ValueError:
                middle_radius_large = None
                break

        return middle_radius_large


    def get_middle_radius_small(self):
        while True:
            try:
                middle_radius_small = self.ui.MiddleRadiusSmall.text().split(',')
                for i in range(len(middle_radius_small)):
                    middle_radius_small[i] = int(middle_radius_small[i])
                break
            except ValueError:
                middle_radius_small = None
                break

        return middle_radius_small


    def create_config_file(self):
        self.ui.label_36.setText('')
        path = self.ui.label_27.text()
        if path == '':
            self.ui.label_36.setText('Choose a template')
        else:
            while True:
                try:
                    tree = Libs.ET.parse(path)
                    break
                except xml.etree.ElementTree.ParseError:
                    self.ui.label_36.setText('Choose a cfg template')
                    tree = None
                    break

            if tree is not None:
                root = tree.getroot()
                Number_of_comp_coil = None
                coil_type = self.get_coil_type()

                for i in range(3):
                    if coil_type[i] == 'QuadrupoleCompensationCoil':
                        Number_of_comp_coil = i
                    elif coil_type[i] is None:
                        self.ui.label_36.setText(f'Coil type for {i+1} coil is empty')

                config_type = self.get_type()
                for i in range(3):
                    if config_type[i] is None:
                        self.ui.label_36.setText(f'Type for {i + 1} coil is empty')

                coil_length = self.get_length()
                for i in range(3):
                    if coil_length[i] is None:
                        self.ui.label_36.setText(f'Length for {i + 1} coil is empty')

                number_of_layers = self.get_number_of_layers()
                number_of_turns = self.get_number_of_turns()
                inner_radius = self.get_inner_radius()
                for i in range(3):
                    if len(inner_radius[i]) > number_of_turns[i]:
                        self.ui.label_36.setText(f'Extra inner radius in {i+1} coil')
                    elif len(inner_radius[i]) < number_of_turns[i]:
                        self.ui.label_36.setText(f'Add {-len(inner_radius[i]) + number_of_turns[i]} more inner radiuses in {i + 1} coil')

                outer_radius = self.get_outer_radius()
                for i in range(3):
                    if len(outer_radius[i]) > number_of_turns[i]:
                        self.ui.label_36.setText(f'Extra inner radius in {i+1} coil')
                    elif len(outer_radius[i]) < number_of_turns[i]:
                        self.ui.label_36.setText(f'Add {-len(outer_radius[i]) + number_of_turns[i]} more outer radiuses in {i + 1} coil')

                if Number_of_comp_coil is not None:
                    while True:
                        try:
                            middle_radius_large = self.get_middle_radius_large()
                            middle_radius_small = self.get_middle_radius_small()
                            break
                        except ValueError:
                            self.ui.label_36.setText('Add middle radius for comp coil')
                            break

                    for elem in root[0][Number_of_comp_coil][2].iter('Coils'):
                        elem.set('xsi:type', coil_type[Number_of_comp_coil])

                    for elem in root[0][Number_of_comp_coil][2][2].iter('Type'):
                        elem.text = str(config_type[Number_of_comp_coil])

                    for elem in root[0][Number_of_comp_coil][2][3].iter('TypeName'):
                        elem.text = str(config_type[Number_of_comp_coil])

                    for elem in root[0][Number_of_comp_coil][2][4].iter('LayerNumber'):
                        elem.text = str(number_of_layers[Number_of_comp_coil])

                    for elem in root[0][Number_of_comp_coil][2][7].iter('NumberOfTurns'):
                        elem.text = str(number_of_turns[Number_of_comp_coil])

                    for elem in root[0][Number_of_comp_coil][2][10].iter('Length'):
                        elem.text = str(coil_length[Number_of_comp_coil])

                    for k in range(number_of_turns[Number_of_comp_coil]):
                        attrib = {}
                        element = root.makeelement('CompensationTurn', attrib)
                        root[0][Number_of_comp_coil][2][12].append(element)
                        Libs.ET.SubElement(root[0][Number_of_comp_coil][2][12][k], 'InnerRadius', attrib)
                        Libs.ET.SubElement(root[0][Number_of_comp_coil][2][12][k], 'OuterRadius', attrib)
                        Libs.ET.SubElement(root[0][Number_of_comp_coil][2][12][k], 'MiddleRadiusSmall', attrib)
                        Libs.ET.SubElement(root[0][Number_of_comp_coil][2][12][k], 'MiddleRadiusLarge', attrib)
                        for elem in root[0][Number_of_comp_coil][2][12][k].iter('InnerRadius'):
                            elem.text = str(inner_radius[Number_of_comp_coil][k])
                        for elem in root[0][Number_of_comp_coil][2][12][k].iter('OuterRadius'):
                            elem.text = str(outer_radius[Number_of_comp_coil][k])
                        for elem in root[0][Number_of_comp_coil][2][12][k].iter('MiddleRadiusSmall'):
                            elem.text = str(middle_radius_small[k])
                        for elem in root[0][Number_of_comp_coil][2][12][k].iter('MiddleRadiusLarge'):
                            elem.text = str(middle_radius_large[k])

                for j in range(3):
                    if j != Number_of_comp_coil:
                        for elem in root[0][j][2].iter('Coils'):
                            elem.set('xsi:type', coil_type[j])

                        for elem in root[0][j][2][2].iter('Type'):
                            elem.text = str(config_type[j])

                        for elem in root[0][j][2][3].iter('TypeName'):
                            elem.text = str(config_type[j])

                        for elem in root[0][j][2][4].iter('LayerNumber'):
                            elem.text = str(number_of_layers[j])

                        for elem in root[0][j][2][7].iter('NumberOfTurns'):
                            elem.text = str(number_of_turns[j])

                        for elem in root[0][j][2][10].iter('Length'):
                            elem.text = str(coil_length[j])

                        for k in range(number_of_turns[j]):
                            attrib = {}
                            element = root.makeelement('Turn', attrib)
                            root[0][j][2][12].append(element)
                            Libs.ET.SubElement(root[0][j][2][12][k], 'InnerRadius', attrib)
                            Libs.ET.SubElement(root[0][j][2][12][k], 'OuterRadius', attrib)
                            for elem in root[0][j][2][12][k].iter('InnerRadius'):
                                elem.text = str(inner_radius[j][k])
                            for elem in root[0][j][2][12][k].iter('OuterRadius'):
                                elem.text = str(outer_radius[j][k])

                Libs.ET.indent(tree, space='  ')
                tree.write('NewConfig.cfg', encoding='utf-8')
                self.ui.label_36.setText('Saved')
