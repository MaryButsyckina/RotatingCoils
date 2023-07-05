import gzip
import xml.parsers.expat

import Libs


class GetMainData:
    @staticmethod
    def parse_data(path_of_file):
        while True:
            try:
                file = Libs.gz.open(path_of_file, mode='rt')
                doc = Libs.xml.parse(file.read())
                break
            except gzip.BadGzipFile:
                try:
                    with open(path_of_file) as file:
                        doc = Libs.xml.parse(file.read())
                except xml.parsers.expat.ExpatError:
                    doc = 'Not an rcf file'
                break

        return doc

    @staticmethod
    def get_num_of_meas(doc):
        return [i for i in range(len(doc['Magnet']['Measurements']))]

    @staticmethod
    def get_measurements(doc):
        return doc['Magnet']['Measurements']

    @staticmethod
    def get_lens_length(doc):
        return float(doc['Magnet']['Length']) / 100


class GetConfigData:
    @staticmethod
    def parse_config_data(path_of_config):
        while True:
            try:
                with open(path_of_config) as fd:
                    doc = Libs.xml.parse(fd.read())
                break
            except UnicodeDecodeError:
                doc = 'Not a config file'
                break
            except xml.parsers.expat.ExpatError:
                doc = 'Not a config file'
                break

        return doc

    @staticmethod
    def get_num_of_turns(doc):
        Num_of_Turns = []
        for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
            Num_of_Turns.append(int(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['NumberOfTurns']))

        return Num_of_Turns

    @staticmethod
    def get_num_of_layers(doc):
        Num_of_Layers = []
        for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
            Num_of_Layers.append(int(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['LayerNumber']))

        return Num_of_Layers

    @staticmethod
    def get_coil_length(doc):
        Coil_length = []
        for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
            if (doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Length']) == 'Full':
                Coil_length.append(1)
            else:
                Coil_length.append(0.5)

        return Coil_length

    @staticmethod
    def get_num_of_comp_coil(doc):
        Num_of_Comp_Coil = None
        for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
            if doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['@xsi:type'] == 'QuadrupoleCompensationCoil':
                Num_of_Comp_Coil = i

        return Num_of_Comp_Coil

    @staticmethod
    def get_ro(doc):
        Ro = []
        for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
            Ro.append([])
            while True:
                try:
                    if doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['NumberOfTurns'] == '1':
                        Ro[i].append(float(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['Turn']['OuterRadius']) / 100)
                    else:
                        for k in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['Turn'])):
                            Ro[i].append(float(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['Turn'][k]['OuterRadius']) / 100)
                    break
                except KeyError:
                    for k in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['CompensationTurn'])):
                        Ro[i].append(float(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['CompensationTurn'][k]['OuterRadius']) / 100)
                    break

        return Ro

    @staticmethod
    def get_ri(doc):
        Ri = []
        for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
            Ri.append([])
            while True:
                try:
                    if doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['NumberOfTurns'] == '1':
                        Ri[i].append(float(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['Turn']['InnerRadius']) / 100)
                    else:
                        for k in range(len(
                                doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['Turn'])):
                            Ri[i].append(float(
                                doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['Turn'][k]['InnerRadius']) / 100)
                    break
                except KeyError:
                    for k in range(len(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns'][
                                'CompensationTurn'])):
                        Ri[i].append(float(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns'][
                                'CompensationTurn'][k]['InnerRadius']) / 100)
                    break

        return Ri

    @staticmethod
    def get_rms(doc):
        Rms = []
        while True:
            try:
                for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
                    Rms.append([])
                    for k in range(len(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns'][
                                        'CompensationTurn'])):
                        Rms[i].append(float(doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns']['CompensationTurn'][k]['MiddleRadiusSmall']) / 100)
                break
            except KeyError:
                break

        return Rms

    @staticmethod
    def get_rml(doc):
        Rml = []
        while True:
            try:
                for i in range(len(doc['ControlSystemConfiguration']['Integrators']['Integrator'])):
                    Rml.append([])
                    for k in range(len(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns'][
                                'CompensationTurn'])):
                        Rml[i].append(float(
                            doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Turns'][
                                'CompensationTurn'][k]['MiddleRadiusLarge']) / 100)
                break
            except KeyError:
                break

        return Rml

    @staticmethod
    def get_type(doc):
        coil_type = []
        for i in range(3):
            if doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['@xsi:type'] == 'QuadrupoleCompensationCoil':
                coil_type.append(0)
            else:
                coil_type.append(1)

        return coil_type


    @staticmethod
    def get_calibr(doc):
        calibr = []
        for i in range(3):
            x = doc['ControlSystemConfiguration']['Integrators']['Integrator'][i]['Coils']['Calibration']
            y = ''
            k = 0
            while x[k] != 'E':
                y += x[k]
                k += 1
            calibr.append(float(y))
        return calibr
