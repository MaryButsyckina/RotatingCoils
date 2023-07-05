import Libs
import Get_data


class SignalFromCoils:
    def __init__(self, doc, selected_meas, calibr):
        super().__init__()

        self.N = selected_meas
        self.Measurements = Get_data.GetMainData.get_measurements(doc)
        self.calibr = calibr

        self.Position_of_coils = [[0 for x in range(
            len(self.Measurements[self.N[0]]['Data']['item'][0]['value']['ArrayOfMeasurementData']['MeasurementData']))]
                                  for y in range(len(self.N))]
        self.Signal = [[] for i in range(len(self.N))]
        self.Integrated_Signal = [[] for i in range(len(self.N))]
        self.Integrated_Signal_from_zero_angle = [[] for i in range(len(self.N))]
        self.k = 0
        self.two_periods_start_position = 0
        self.angle = [[] for i in range(len(self.N))]
        self.Splined_Signal = [[] for i in range(len(self.N))]
        self.xs = Libs.np.arange(0, 360, 360 / 128)
        self.doc = doc

    def get_position_data(self):
        for n in range(len(self.N)):
            start_position_of_coils = \
                self.Measurements[self.N[n]]['Data']['item'][0]['value']['ArrayOfMeasurementData'][
                    'MeasurementData'][0]
            start_position_of_coils = float(start_position_of_coils['AbsolutePosition']) * 180 / Libs.np.pi
            self.Position_of_coils[n][0] = start_position_of_coils
            for i in range(len(
                    self.Measurements[self.N[n]]['Data']['item'][0]['value']['ArrayOfMeasurementData'][
                        'MeasurementData'])):
                start_position_of_coils = start_position_of_coils + (float(
                    self.Measurements[self.N[n]]['Data']['item'][0]['value']['ArrayOfMeasurementData'][
                        'MeasurementData'][i]['StopPosition']) - float(
                    self.Measurements[self.N[n]]['Data']['item'][0]['value']['ArrayOfMeasurementData'][
                        'MeasurementData'][i]['StartPosition'])) * 180 / Libs.np.pi
                if i < len(self.Position_of_coils[n]):
                    self.Position_of_coils[n][i] = start_position_of_coils
                else:
                    self.Position_of_coils[n].append(start_position_of_coils)

            if len(self.Position_of_coils[n]) > len(
                    self.Measurements[self.N[n]]['Data']['item'][0]['value']['ArrayOfMeasurementData'][
                        'MeasurementData']):
                for i in range(0, len(self.Position_of_coils[n]) - len(
                        self.Measurements[self.N[n]]['Data']['item'][0]['value']['ArrayOfMeasurementData'][
                            'MeasurementData'])):
                    self.Position_of_coils[n].pop()

        return self.Position_of_coils

    def get_signal_from_coils(self, j):
        for n in range(len(self.N)):
            for dat in \
                    self.Measurements[self.N[n]]['Data']['item'][j]['value']['ArrayOfMeasurementData'][
                        'MeasurementData']:
                self.Signal[n].append(self.calibr[j] * (float(dat['Data']) - float(dat['Offset'])))

        return self.Signal

    def integrate_signal_from_coils(self, j):
        Signal = self.get_signal_from_coils(j)
        for n in range(len(self.N)):
            self.Integrated_Signal[n].append(Signal[n][0])
            for i in range(1, len(Signal[n])):
                self.Integrated_Signal[n].append(self.Integrated_Signal[n][i - 1] + Signal[n][i])

        return self.Integrated_Signal

    def find_zero_angle(self, j):
        Integrated_Signal = self.integrate_signal_from_coils(j)
        self.Position_of_coils = self.get_position_data()
        for n in range(len(self.N)):
            i = 0
            for i in range(len(self.Position_of_coils[n])):
                if self.Position_of_coils[n][i] > -6:
                    k = i
                    break
                else:
                    pass
            while True:
                i += 1
                if Integrated_Signal[n][i - 1] < Integrated_Signal[n][i] > Integrated_Signal[n][i + 1]:
                    if self.Position_of_coils[n][i] < 6:
                        self.two_periods_start_position = i
                    else:
                        self.two_periods_start_position = None
                    break

        return self.two_periods_start_position

    def two_periods_signal(self, j, two_periods_start_position):
        Integrated_Signal = self.integrate_signal_from_coils(j)
        for n in range(len(self.N)):
            for x in range(two_periods_start_position, 128 + two_periods_start_position):
                self.Integrated_Signal_from_zero_angle[n].append(Integrated_Signal[n][x])

        return self.Integrated_Signal_from_zero_angle

    def angle_of_coils(self, two_periods_start_position):
        Position_of_coils = self.get_position_data()

        for n in range(len(self.N)):
            for i in range(two_periods_start_position, 128 + two_periods_start_position):
                self.angle[n].append(Position_of_coils[n][i])
        print(self.angle)
        return self.angle

    def spline_signal(self, j):
        two_periods_start_position = self.find_zero_angle(j)
        if two_periods_start_position is None:
            self.__init__(self.doc, self.N, self.calibr)
            two_periods_start_position = 51
        angle = self.angle_of_coils(two_periods_start_position)
        Integrated_Signal_from_zero_angle = self.two_periods_signal(j, two_periods_start_position)
        for n in range(len(self.N)):
            self.Splined_Signal[n] = Libs.sp.interpolate.CubicSpline(angle[n],Integrated_Signal_from_zero_angle[n])(
                self.xs)

        return self.Splined_Signal


    def return_spline(self, j):
        angle = self.get_position_data()
        Signal = self.get_signal_from_coils(j)
        full_xs = [[] for y in range(len(self.N))]
        splined_signal = [[] for y in range(len(self.N))]

        for n in range(len(self.N)):
            full_xs[n] = Libs.np.arange(min(angle[n]), max(angle[n]), (max(angle[n]) - min(angle[n]))/len(self.Signal[n]))
            splined_signal[n] = Libs.sp.interpolate.CubicSpline(angle[n], Signal[n])(full_xs[n])

        return [full_xs, splined_signal]


class FieldCoefficients:
    def __init__(self, doc, config_doc, splined_signal, selected_meas, r_ref):
        super().__init__()

        self.Splined_Signal = splined_signal

        self.doc = doc
        self.config_doc = config_doc

        self.N = selected_meas
        self.Number_of_compensation_coil = Get_data.GetConfigData.get_num_of_comp_coil(config_doc)
        self.Number_of_layers = Get_data.GetConfigData.get_num_of_layers(config_doc)
        self.Lens_length = Get_data.GetMainData.get_lens_length(doc)
        self.Coil_length = Get_data.GetConfigData.get_coil_length(config_doc)
        self.Num_of_turns = Get_data.GetConfigData.get_num_of_turns(config_doc)
        self.Rms = Get_data.GetConfigData.get_rms(config_doc)
        self.Rml = Get_data.GetConfigData.get_rml(config_doc)
        self.Ri = Get_data.GetConfigData.get_ri(config_doc)
        self.Ro = Get_data.GetConfigData.get_ro(config_doc)
        self.Rref = r_ref

        self.FFT_of_signal = []
        self.FFT_Coef = [[[] for i in range(len(self.N))],
                         [[] for i in range(len(self.N))]]  # FFT_Coef[0] - coef a, FFT_Coef[1] - coef b
        self.A_Coef = [[] for i in range(len(self.N))]
        self.B_Coef = [[] for i in range(len(self.N))]


    def fft_coefficients(self, j):
        for n in range(len(self.N)):
            self.FFT_of_signal = Libs.fft.rfft(self.Splined_Signal[j][n])
            print(len(self.Splined_Signal[j][n]))
            self.FFT_Coef[0][n] = self.FFT_of_signal.imag
            self.FFT_Coef[1][n] = -self.FFT_of_signal.real

        return self.FFT_Coef

    def harmonics_for_compensation_coil(self, j):
        self.FFT_Coef = self.fft_coefficients(j)
        for n in range(len(self.N)):
            for i in range(1, 16):
                S_comp = 0
                for k in range(self.Num_of_turns[self.Number_of_compensation_coil]):
                    S_comp += (-(-self.Rms[self.Number_of_compensation_coil][k]) ** i + (
                        -self.Ri[self.Number_of_compensation_coil][k]) ** i + (
                                   self.Ro[self.Number_of_compensation_coil][k]) ** i - (
                                   self.Rml[self.Number_of_compensation_coil][k]) ** i) / 2 - (
                                  self.Rms[self.Number_of_compensation_coil][k]) ** i + (
                                  self.Ri[self.Number_of_compensation_coil][k]) ** i

                Field_Coef = i * self.Rref ** (i - 1) / (64 * self.Number_of_layers[self.Number_of_compensation_coil] * self.Lens_length * S_comp) * 10000
                self.A_Coef[n].append(self.FFT_Coef[0][n][i] * Field_Coef)
                self.B_Coef[n].append(self.FFT_Coef[1][n][i] * Field_Coef)
        return [self.A_Coef, self.B_Coef]

    def harmonics_for_coil(self, coil_num):
        j = coil_num
        self.FFT_Coef = self.fft_coefficients(j)
        for n in range(len(self.N)):
            for i in range(1, 16):
                S = 0
                for k in range(self.Num_of_turns[coil_num]):
                    S += self.Ro[coil_num][k] ** i - self.Ri[coil_num][k] ** i

                Field_Coef = i * self.Rref ** (i - 1) / (
                        64 * self.Number_of_layers[coil_num] * self.Lens_length * self.Coil_length[coil_num] * S) * 10000

                self.A_Coef[n].append(self.FFT_Coef[0][n][i] * Field_Coef)
                self.B_Coef[n].append(self.FFT_Coef[1][n][i] * Field_Coef)

        return [self.A_Coef, self.B_Coef]


class Field:
    def __init__(self, selected_meas, a_coef, b_coef):
        super().__init__()

        self.N = selected_meas
        self.A_coef = a_coef
        self.B_Coef = b_coef

        self.Field = [[] for i in range(len(self.N))]

    def field_harmonics(self):
        for n in range(len(self.N)):
            for i in range(15):
                self.Field[n].append(Libs.np.sqrt(self.A_coef[n][i] ** 2 + self.B_Coef[n][i] ** 2))

        return self.Field


class Displacement:
    def __init__(self, j, a_coef, b_coef, field, r_ref, is_sextuple):
        super().__init__()

        self.B_Coef = b_coef
        self.A_Coef = a_coef
        self.Field = field
        self.Rref = r_ref
        self.j = j
        self.is_sextuple = is_sextuple
        self.main_harm = 1
        self.displacement_harm = 0
        self.magnet_type()


    def magnet_type(self):
        if self.is_sextuple:
            self.main_harm = 2
            self.displacement_harm = 1



    def calc_x(self):
        x = []
        for n in range(len(self.B_Coef[self.j])):
            x.append(self.Rref * 1000 * self.B_Coef[self.j][n][self.displacement_harm] / self.Field[self.j][n][self.main_harm] * 1000)
            # print('x', n, x[-1])

        return x

    def calc_y(self):
        y = []
        for n in range(len(self.A_Coef[self.j])):
            y.append(self.Rref * 1000 * self.A_Coef[self.j][n][self.displacement_harm] / self.Field[self.j][n][self.main_harm] * 1000)
            # print('y', n, y[-1])

        return y


class PolesGeometry:
    def __init__(self, selected_meas, distance, a_coef, b_coef, j):
        super().__init__()

        self.j = j
        self.selected_meas = selected_meas

        self.alpha = Libs.np.arange(0, 360, 360 / 128)
        self.FieldQuad = [[0 for x in range(128)] for y in range(len(selected_meas))]
        self.FieldFull = [[0 for x in range(128)] for y in range(len(selected_meas))]

        self.A_Coef = a_coef
        self.B_Coef = b_coef

        self.deviation = [[0 for x in range(4)] for y in range(len(selected_meas))]
        self.dist_between_poles = distance
        self.point = [[0 for i in range(4)] for y in range(len(selected_meas))]

    def calc_quad_field(self):
        for n in range(len(self.selected_meas)):
            for i in range(128):
                self.FieldQuad[n][i] = abs(
                    self.A_Coef[self.j][n][1] * Libs.np.sin(2 * self.alpha[i] * Libs.np.pi / 180) +
                    self.B_Coef[self.j][n][1] * Libs.np.cos(2 * self.alpha[i] * Libs.np.pi / 180))

        return self.FieldQuad

    def calc_full_field(self):
        for n in range(len(self.selected_meas)):
            for i in range(128):
                for x in range(1, 15):
                    self.FieldFull[n][i] += self.A_Coef[self.j][n][x] * Libs.np.sin(
                        (x + 1) * self.alpha[i] * Libs.np.pi / 180) + self.B_Coef[self.j][n][x] * Libs.np.cos(
                        (x + 1) * self.alpha[i] * Libs.np.pi / 180)

        return self.FieldFull

    def calc_deviation(self):
        FieldFull = self.calc_full_field()
        FieldQuad = self.calc_quad_field()
        counter = [0, 0, 0, 0]

        for n in range(len(self.selected_meas)):
            k = 0

            for i in range(1, len(FieldFull[n]) - 1):
                if abs(FieldFull[n][i - 1]) < abs(FieldFull[n][i]) > abs(FieldFull[n][i + 1]):
                    try:
                        self.point[n][k] = abs(FieldFull[n][i])
                    except IndexError:
                        self.point[n].append(abs(FieldFull[n][i]))
                    k += 1

            if self.point[n][3] == 0:
                for i in range(3):
                    self.point[n][3 - i] = self.point[n][2 - i]
                    counter[3-i] = counter[2 - i]
                self.point[n][0] = abs(FieldFull[n][0])

            if max(FieldQuad[n]) > abs(min(FieldQuad[n])):
                maxFieldQuad = max(FieldQuad[n])
            else:
                maxFieldQuad = min(FieldQuad[n])

            for i in range(4):
                self.deviation[n][i] = (self.dist_between_poles - (
                        self.point[n][i] / maxFieldQuad * self.dist_between_poles)) * 10 ** 6

        return self.deviation


class Hyperbola:
    def __init__(self, deviation, dist_between_poles, g, number_of_coil, pole, hyperbola):
        super(Hyperbola, self).__init__()
        self.deviation = deviation
        self.dist_between_poles = dist_between_poles
        self.g = g
        self.pole = pole
        self.hyperbola = hyperbola
        self.j = number_of_coil

        theta = Libs.np.pi * 45 / 180
        self.k = abs(Libs.np.cos(theta))

    def calc_x_range(self):
        x_start = 3 * self.dist_between_poles / (2 * self.k)
        x_finish = 2 * self.dist_between_poles / self.k

        return [x_start, x_finish]

    def calc_hyperbola_coef(self):
        a = 3 * self.dist_between_poles / (2 * self.k)

        if self.hyperbola == 'real':
            if self.pole < 3:
                deviation_up = self.deviation[self.j][self.g][self.pole]
                deviation_down = self.deviation[self.j][self.g][self.pole + 1]
            else:
                deviation_up = self.deviation[self.j][self.g][self.pole]
                deviation_down = self.deviation[self.j][self.g][0]
        else:
            deviation_up = 0
            deviation_down = 0

        b_up = 3 * (self.dist_between_poles + deviation_up) / (Libs.np.sqrt(7) * self.k)
        b_down = 3 * (self.dist_between_poles + deviation_down) / (Libs.np.sqrt(7) * self.k)

        return [a, [b_up, b_down]]

    def calc_hyperbola(self):
        x = []
        y = []
        x_range = self.calc_x_range()
        x_start = x_range[0]
        x_finish = x_range[1]
        coef = self.calc_hyperbola_coef()
        a = coef[0]
        b_up = coef[1][0]
        b_down = coef[1][1]

        for i in range(51):
            x.append(x_finish - i * (x_finish - x_start) / 50)
            y.append(Libs.np.sqrt((x[i] / a) ** 2 - 1) * b_up)
        for i in range(1, 51):
            x.append(x_start + i * (x_finish - x_start) / 50)
            y.append(-Libs.np.sqrt((x[50 + i] / a) ** 2 - 1) * b_down)

        return [x, y]

    def rotation_matrix(self):
        theta = Libs.np.pi * (45 - 90 * self.pole) / 180
        rotation_matrix = [[Libs.np.cos(theta), Libs.np.sin(theta)], [Libs.np.sin(theta), Libs.np.cos(theta)]]

        return rotation_matrix

    def rotate_hyperbola(self):
        u = []
        w = []

        x_y = self.calc_hyperbola()
        x = x_y[0]
        y = x_y[1]
        rotation_matrix = self.rotation_matrix()

        for i in range(101):
            w.append(rotation_matrix[0][0] * x[i] - rotation_matrix[0][1] * y[i])
            u.append(rotation_matrix[1][0] * x[i] + rotation_matrix[1][1] * y[i])

        return [w, u]

    def check_w(self, w):
        for i in range(101):
            if abs(w[i]) > 3 * self.dist_between_poles:
                if w[i] > 0:
                    w[i] = 3 * self.dist_between_poles
                else:
                    w[i] = -3 * self.dist_between_poles

        if self.pole == 0 or self.pole == 2:
            if abs(w[len(w) - 1]) < 3 * self.dist_between_poles:
                if w[len(w) - 1] > 0:
                    w[len(w) - 1] = 3 * self.dist_between_poles
                else:
                    w[len(w) - 1] = -3 * self.dist_between_poles
        else:
            if abs(w[0]) < 3 * self.dist_between_poles:
                if w[0] > 0:
                    w[0] = 3 * self.dist_between_poles
                else:
                    w[0] = -3 * self.dist_between_poles

        return w

    def check_u(self, u):
        for i in range(101):
            if abs(u[i]) > 3 * self.dist_between_poles:
                if u[i] > 0:
                    u[i] = 3 * self.dist_between_poles
                else:
                    u[i] = -3 * self.dist_between_poles

        if self.pole == 0 or self.pole == 2:
            if abs(u[0]) < 3 * self.dist_between_poles:
                if u[0] > 0:
                    u[0] = 3 * self.dist_between_poles
                else:
                    u[0] = -3 * self.dist_between_poles
        else:
            if abs(u[len(u) - 1]) < 3 * self.dist_between_poles:
                if u[len(u) - 1] > 0:
                    u[len(u) - 1] = 3 * self.dist_between_poles
                else:
                    u[len(u) - 1] = -3 * self.dist_between_poles

        return u


class CalculationsForExcel:
    def __init__(self, a_coef_volts, b_coef_volts, selected_meas, main_harm):
        super(CalculationsForExcel, self).__init__()
        self.a_coef_volts = a_coef_volts
        self.b_coef_volts = b_coef_volts
        self.selected_meas = selected_meas
        self.main_harm = main_harm

        self.a_for_graph_volts = [[0 for x in range(len(selected_meas))] for y in range(15)]
        self.b_for_graph_volts = [[0 for x in range(len(selected_meas))] for y in range(15)]
        self.alpha = 0


    def calculate_alpha(self):
        for n in self.selected_meas:
            self.alpha += Libs.np.arctan(self.a_coef_volts[n][self.main_harm]/self.b_coef_volts[n][self.main_harm] / self.main_harm)
        self.alpha = self.alpha/len(self.selected_meas)

        return self.alpha


    def calculate_coefficients_for_graph(self, alpha):
        for h in range(15):
            for n in range(len(self.selected_meas)):
                self.a_for_graph_volts[h][n] = (self.a_coef_volts[n][h+1]/Libs.np.sqrt(self.b_coef_volts[n][self.main_harm] ** 2 + self.a_coef_volts[n][self.main_harm] ** 2) * Libs.np.cos(h * alpha) - self.b_coef_volts[n][h+1] / Libs.np.sqrt(self.b_coef_volts[n][self.main_harm] **2 + self.a_coef_volts[n][self.main_harm] ** 2) * Libs.np.sin(h * alpha)) * 10000
                self.b_for_graph_volts[h][n] = (self.a_coef_volts[n][h+1]/Libs.np.sqrt(self.b_coef_volts[n][self.main_harm] ** 2 + self.a_coef_volts[n][self.main_harm] ** 2) * Libs.np.sin(h * alpha) + self.b_coef_volts[n][h+1] / Libs.np.sqrt(self.b_coef_volts[n][self.main_harm] **2 + self.a_coef_volts[n][self.main_harm] ** 2) * Libs.np.cos(h * alpha)) * 10000
                print(n, h, self.a_for_graph_volts[h][n])

        return [self.a_for_graph_volts, self.b_for_graph_volts]
