import Libs


class SavePathOfConfigurationFile:
    def __init__(self, path):
        super(SavePathOfConfigurationFile, self).__init__()
        tree = Libs.ET.parse('Configuration.cfg')
        root = tree.getroot()
        for elem in root[1].iter('PathOfConfig'):
            elem.text = path

        tree.write('Configuration.cfg')


class SavePathOfFile:
    def __init__(self, path):
        super(SavePathOfFile, self).__init__()
        tree = Libs.ET.parse('Configuration.cfg')
        root = tree.getroot()
        for elem in root[0].iter('PathOfFile'):
            elem.text = path

        tree.write('Configuration.cfg')


class SavingTemplate:
    def __init__(self, template_name):
        super(SavingTemplate, self).__init__()
        tree = Libs.ET.parse('Configuration.cfg')
        root = tree.getroot()
        for elem in root[2].iter('SavingTemplate'):
            elem.text = template_name

        tree.write('Configuration.cfg')
