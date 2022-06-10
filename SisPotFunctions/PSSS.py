import numpy as np
import scipy as sp
import pandas as pd
import os
from cmath import rect
from scipy.stats import chi2
# from tqdm import tqdm

nprect = np.vectorize(rect)

def line_params(r: float, x: float, c_total: float, a: float) -> complex:
    diag_value = 1/(r + x*1j) + c_total*0.5j if a == 0 else (1/(r + x*1j) + c_total*0.5j)/(a**2)
    out_diag_value = 1/(r + x*1j) if a == 0 else (1/(r + x*1j))/(a)
    return diag_value, out_diag_value

def get_line_values(parameter: str, bus_from: int, bus_to: int, network_values: dict) -> float:
    bus_from = int(bus_from - 1)
    bus_to = int(bus_to - 1)
    search_1 = (parameter, bus_from, bus_to)
    search_2 = (parameter, bus_to, bus_from)
    key = search_1 in network_values.keys()
    if key:
        return network_values.get(search_1)
    else:
        return network_values.get(search_2)
        

def derivada_p_Flow(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: tuple, n_bus: int) -> np.ndarray:
    state_amount = n_bus*2 -1
    pFlowVector = np.zeros(shape = (state_amount, ))
    for i in range(state_amount):
        if i < (n_bus-1):
            if i + 2 in bus:
                vi = state_vector[bus[0] + n_bus -2]
                vj = state_vector[bus[1] + n_bus -2]
                gij = get_line_values('g', bus[0], bus[1], network_values)
                bij = get_line_values('b', bus[0], bus[1], network_values)
                tetai = state_vector[bus[0] - 2] if bus[0] > 1 else 0
                tetaj = state_vector[bus[1] - 2] if bus[1] > 1 else 0
                pFlowVector[i] = vi*vj*(gij*np.sin(tetai-tetaj) - bij*np.cos(tetai-tetaj)) if i + 2 == bus[0] else -vi*vj*(gij*np.sin(tetai-tetaj) - bij*np.cos(tetai-tetaj))
            else:
                pFlowVector[i] = 0
        else:
            actual_bus = i - (n_bus - 2)
            if actual_bus in bus:
                vi = state_vector[bus[0] + n_bus -2]
                vj = state_vector[bus[1] + n_bus -2]
                gij = get_line_values('g', bus[0], bus[1], network_values)
                bij = get_line_values('b', bus[0], bus[1], network_values)
                gsi = get_line_values('gs', bus[0], bus[1], network_values)
                tetai = state_vector[bus[0] - 2] if bus[0] > 1 else 0
                tetaj = state_vector[bus[1] - 2] if bus[1] > 1 else 0
                pFlowVector[i] = -vj*(gij*np.cos(tetai-tetaj) + bij*np.sin(tetai-tetaj)) + 2*(gij + gsi)*vi if actual_bus == bus[0] else -vi*(gij*np.cos(tetai-tetaj) + bij*np.sin(tetai-tetaj))
            else:
                pFlowVector[i] = 0
    return pFlowVector

def derivada_q_Flow(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: tuple, n_bus: int) -> np.ndarray:
    state_amount = n_bus*2 -1
    qFlowVector = np.zeros(shape = (state_amount, ))
    for i in range(state_amount):
        if i < (n_bus-1):
            if i + 2 in bus:
                vi = state_vector[bus[0] + n_bus -2]
                vj = state_vector[bus[1] + n_bus -2]
                gij = get_line_values('g', bus[0], bus[1], network_values)
                bij = get_line_values('b', bus[0], bus[1], network_values)
                tetai = state_vector[bus[0] - 2] if bus[0] > 1 else 0
                tetaj = state_vector[bus[1] - 2] if bus[1] > 1 else 0
                qFlowVector[i] = -vi*vj*(gij*np.cos(tetai-tetaj) + bij*np.sin(tetai-tetaj)) if i + 2 == bus[0] else vi*vj*(gij*np.cos(tetai-tetaj) + bij*np.sin(tetai-tetaj))
            else:
                qFlowVector[i] = 0
        else:
            actual_bus = i - (n_bus - 2)
            if actual_bus in bus:
                vi = state_vector[bus[0] + n_bus -2]
                vj = state_vector[bus[1] + n_bus -2]
                gij = get_line_values('g', bus[0], bus[1], network_values)
                bij = get_line_values('b', bus[0], bus[1], network_values)
                bsi = get_line_values('bs', bus[0], bus[1], network_values)
                tetai = state_vector[bus[0] - 2] if bus[0] > 1 else 0
                tetaj = state_vector[bus[1] - 2] if bus[1] > 1 else 0
                qFlowVector[i] = -vj*(gij*np.sin(tetai-tetaj) - bij*np.cos(tetai-tetaj)) - 2*(bij + bsi)*vi if actual_bus == bus[0] else -vi*(gij*np.sin(tetai-tetaj) - bij*np.cos(tetai-tetaj))
            else:
                qFlowVector[i] = 0
    return qFlowVector

def derivada_p_Inj(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: int, n_bus: int) -> np.ndarray:
    state_amount = n_bus*2 -1
    pInjVector = np.zeros(shape = (state_amount, ))
    for i in range(state_amount):
        if i < (n_bus-1):
            if i + 2 == bus:
                vi = state_vector[bus + n_bus -2]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Bii = y_bar[bus -1, bus - 1].imag
                bus_looking = range(n_bus)
                aux_p = 0
                for j in bus_looking:
                    vj = state_vector[j + n_bus - 1]
                    Gij = y_bar[i+1, j].real
                    Bij = y_bar[i+1, j].imag
                    tetaj = state_vector[j - 1] if j > 0 else 0
                    tetaij = tetai - tetaj
                    aux_p += vi*vj*(Bij*np.cos(tetaij) - Gij*np.sin(tetaij))
                pInjVector[i] = aux_p - vi*vi*Bii
            else:
                vi = state_vector[bus + n_bus -2]
                vj = state_vector[i + n_bus]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Gij = y_bar[bus - 1, i+1].real
                Bij = y_bar[bus - 1, i+1].imag
                tetaj = state_vector[i]
                tetaij = tetai - tetaj
                pInjVector[i] = vi*vj*(Gij*np.sin(tetaij) - Bij*np.cos(tetaij))
        else:
            actual_bus = i - (n_bus - 2)
            if actual_bus == bus:
                vi = state_vector[bus + n_bus -2]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Gii = y_bar[bus -1, bus - 1].real
                bus_looking = range(n_bus)
                aux_p = 0
                for j in bus_looking:
                    vj = state_vector[j + n_bus - 1]
                    Gij = y_bar[actual_bus-1, j].real
                    Bij = y_bar[actual_bus-1, j].imag
                    tetaj = state_vector[j - 1] if j > 0 else 0
                    tetaij = tetai - tetaj
                    aux_p += vj*(Bij*np.sin(tetaij) + Gij*np.cos(tetaij))
                pInjVector[i] = aux_p + vi*Gii
            else:
                vi = state_vector[bus + n_bus -2]
                vj = state_vector[i]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Gij = y_bar[bus - 1, actual_bus-1].real
                Bij = y_bar[bus - 1, actual_bus-1].imag
                tetaj = state_vector[actual_bus-2] if actual_bus > 1 else 0
                tetaij = tetai - tetaj
                pInjVector[i] = vi*(Gij*np.cos(tetaij) + Bij*np.sin(tetaij))
    return pInjVector

def derivada_q_Inj(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: int, n_bus: int) -> np.ndarray:
    state_amount = n_bus*2 -1
    qInjVector = np.zeros(shape = (state_amount, ))
    for i in range(state_amount):
        if i < (n_bus-1):
            if i + 2 == bus:
                vi = state_vector[bus + n_bus -2]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Gii = y_bar[bus -1, bus - 1].real
                bus_looking = range(n_bus)
                aux_p = 0
                for j in bus_looking:
                    vj = state_vector[j + n_bus - 1]
                    Gij = y_bar[i+1, j].real
                    Bij = y_bar[i+1, j].imag
                    tetaj = state_vector[j - 1] if j > 0 else 0
                    tetaij = tetai - tetaj
                    aux_p += vi*vj*(Bij*np.sin(tetaij) + Gij*np.cos(tetaij))
                qInjVector[i] = aux_p - vi*vi*Gii
            else:
                vi = state_vector[bus + n_bus -2]
                vj = state_vector[i + n_bus]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Gij = y_bar[bus - 1, i+1].real
                Bij = y_bar[bus - 1, i+1].imag
                tetaj = state_vector[i]
                tetaij = tetai - tetaj
                qInjVector[i] = -vi*vj*(Gij*np.cos(tetaij) + Bij*np.sin(tetaij))
        else:
            actual_bus = i - (n_bus - 2)
            if actual_bus == bus:
                vi = state_vector[bus + n_bus -2]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Bii = y_bar[bus -1, bus - 1].imag
                bus_looking = range(n_bus)
                aux_p = 0
                for j in bus_looking:
                    vj = state_vector[j + n_bus - 1]
                    Gij = y_bar[actual_bus-1, j].real
                    Bij = y_bar[actual_bus-1, j].imag
                    tetaj = state_vector[j - 1] if j > 0 else 0
                    tetaij = tetai - tetaj
                    aux_p += vj*(Gij*np.sin(tetaij) - Bij*np.cos(tetaij))
                qInjVector[i] = aux_p - vi*Bii
            else:
                vi = state_vector[bus + n_bus -2]
                vj = state_vector[i]
                tetai = state_vector[bus - 2] if bus > 1 else 0
                Gij = y_bar[bus - 1, actual_bus-1].real
                Bij = y_bar[bus - 1, actual_bus-1].imag
                tetaj = state_vector[actual_bus-2] if actual_bus > 1 else 0
                tetaij = tetai - tetaj
                qInjVector[i] = vi*(Gij*np.sin(tetaij) - Bij*np.cos(tetaij))
    return qInjVector

def derivada_voltage(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: int, n_bus: int) -> np.ndarray:
    state_amount = n_bus*2 -1
    vVector = np.zeros(shape = (state_amount, ))
    for i in range(state_amount):
        if i < (n_bus-1):
            vVector[i] = 0
        else:
            actual_bus = i - (n_bus - 2)
            if actual_bus == bus:
                vVector[i] = 1
            else:
                vVector[i] = 0
    return vVector

def derivada_current_Flow(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: tuple, n_bus: int) -> np.ndarray:
    return

def p_Flow(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: tuple, n_bus: int) -> np.ndarray:
    gij = get_line_values('g', bus[0], bus[1], network_values)
    bij = get_line_values('b', bus[0], bus[1], network_values)
    gsi = get_line_values('gs', bus[0], bus[1], network_values)
    tetai = state_vector[bus[0] - 2] if bus[0] > 1 else 0
    tetaj = state_vector[bus[1] - 2] if bus[1] > 1 else 0
    tetaij = tetai - tetaj
    vi = state_vector[bus[0] + (n_bus - 2)]
    vj = state_vector[bus[1] + (n_bus - 2)]
    pFlow = vi*vi*(gsi + gij) - vi*vj*(gij*np.cos(tetaij) + bij*np.sin(tetaij))
    return pFlow

def q_Flow(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: tuple, n_bus: int) -> np.ndarray:
    gij = get_line_values('g', bus[0], bus[1], network_values)
    bij = get_line_values('b', bus[0], bus[1], network_values)
    bsi = get_line_values('bs', bus[0], bus[1], network_values)
    tetai = state_vector[bus[0] - 2] if bus[0] > 1 else 0
    tetaj = state_vector[bus[1] - 2] if bus[1] > 1 else 0
    tetaij = tetai - tetaj
    vi = state_vector[bus[0] + (n_bus - 2)]
    vj = state_vector[bus[1] + (n_bus - 2)]
    qFlow = -vi*vi*(bsi + bij) - vi*vj*(gij*np.sin(tetaij) - bij*np.cos(tetaij))
    return qFlow

def p_Inj(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: int, n_bus: int) -> np.ndarray:
    vi = state_vector[bus + (n_bus - 2)]
    tetai = state_vector[bus - 2] if bus > 1 else 0
    pInj = 0
    for j in range(n_bus):
        tetaj = state_vector[j - 1] if j > 0 else 0
        vj = state_vector[j + (n_bus - 1)]
        Gij = y_bar[bus-1, j].real
        Bij = y_bar[bus-1, j].imag
        tetaij = tetai - tetaj
        pInj += vi*vj*(Gij*np.cos(tetaij) + Bij*np.sin(tetaij))
    return pInj

def q_Inj(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: int, n_bus: int) -> np.ndarray:
    vi = state_vector[bus + (n_bus - 2)]
    tetai = state_vector[bus - 2] if bus > 1 else 0
    qInj = 0
    for j in range(n_bus):
        tetaj = state_vector[j - 1] if j > 0 else 0
        vj = state_vector[j + (n_bus - 1)]
        Gij = y_bar[bus-1, j].real
        Bij = y_bar[bus-1, j].imag
        tetaij = tetai - tetaj
        qInj += vi*vj*(Gij*np.sin(tetaij) - Bij*np.cos(tetaij))
    return qInj

def voltage(y_bar: np.ndarray, network_values: dict, state_vector: np.ndarray, bus: int, n_bus: int) -> np.ndarray:
    return state_vector[bus + (n_bus - 2)]

def measurement_Function(order_meansured: list, meansured_network: dict, y_bar: np.ndarray, network_values: dict, state_vetctor: np.ndarray = None) -> np.ndarray:
    n_bus = y_bar.shape[0]
    if state_vetctor is None:
        states = [0]*(n_bus-1)
        states.extend([1]*n_bus)
        state_vetctor = np.array(states)
    line_amount = len(order_meansured)
    z_array = np.zeros(shape = (line_amount, ))
    meansured_estimated = np.zeros(shape = (line_amount, ))
    func_dict = {'P_inj': p_Inj,'P_flow': p_Flow, 'Q_inj': q_Inj, 'Q_flow': q_Flow, 'V': voltage, 'I_flow': derivada_current_Flow}
    for i, meansured in enumerate(order_meansured):
        meansured_type = list(meansured.keys())[0]
        bus = meansured.get(meansured_type)
        line_h = func_dict[meansured_type](y_bar, network_values, state_vetctor, bus, n_bus)
        meansured_estimated[i] = line_h
        z_array[i] = meansured_network[meansured_type[0]][bus][0] - line_h
    return z_array, meansured_estimated

def meansurement_jacobian(order_meansured: list, y_bar: np.ndarray, network_values: dict, state_vetctor: np.ndarray = None) -> np.ndarray:
    n_bus = y_bar.shape[0]
    if state_vetctor is None:
        states = [0]*(n_bus-1)
        states.extend([1]*n_bus)
        state_vetctor = np.array(states)
    line_amount = len(order_meansured)
    col_amount  = len(state_vetctor)
    h_matrix = np.zeros(shape = (line_amount, col_amount))
    func_dict = {'P_inj': derivada_p_Inj,'P_flow': derivada_p_Flow, 'Q_inj': derivada_q_Inj, 'Q_flow': derivada_q_Flow, 'V': derivada_voltage, 'I_flow': derivada_current_Flow}
    for i, meansured in enumerate(order_meansured):
        meansured_type = list(meansured.keys())[0]
        bus = meansured.get(meansured_type)
        line_h = func_dict[meansured_type](y_bar, network_values, state_vetctor, bus, n_bus)
        h_matrix[i,:] = line_h
    return h_matrix

def get_G_matrix(H: np.ndarray, R: np.ndarray) -> np.ndarray:
    R_inv = np.linalg.inv(R)
    H_T = np.transpose(H.copy())
    h_r_inv = H_T@R_inv
    g = h_r_inv@H
    return g

def read_meansured(filepath: str, filename: str, data: pd.core.frame.DataFrame = None):
    if data is None:
        path_file = os.path.join(filepath, filename)
        meansured = pd.read_excel(path_file)
    else:
        meansured = data
    data = {}
    R = np.identity(meansured.shape[0])
    order_meansured = []
    for i, line in enumerate(meansured.iterrows()):
        meansured_line = line[1]
        meansured_type = meansured_line['Tipo']
        bus_from_to = (meansured_line['De'], meansured_line['Para']) if meansured_line['Para'] != '-' else meansured_line['De']
        if meansured_type == "P" or meansured_type == "Q" or meansured_type == "I":
            meansured_type_specific = f'{meansured_type}_flow' if type(bus_from_to) == tuple else f'{meansured_type}_inj'
        else:
            meansured_type_specific = meansured_type
        order_meansured.append({meansured_type_specific: bus_from_to})
        R[i,i] = meansured_line['Desvio Padrão']**2
        med_caracteristic = (meansured_line['Valor'], meansured_line['Desvio Padrão'])
        data_med = {bus_from_to: med_caracteristic}
        if meansured_type not in list(data.keys()):
            data[meansured_type] = data_med
        else:
            data[meansured_type].update(data_med)
    return data, R, order_meansured


def mount_y_bar(filepath: str, filename: str, data: pd.core.frame.DataFrame = None):
    if data is None:
        path_file = os.path.join(filepath, filename)
        line_data = pd.read_excel(path_file)
    else:
        line_data = data
    total_lines = set(line_data['De'].to_list() + line_data['Para'].to_list())
    n = len(total_lines)
    y_bar_matriz = np.zeros((n, n), dtype=complex)
    connective_values = {}
    for lines in line_data.iterrows():
        data_lines = lines[1]
        bus_from = int(data_lines['De'] - 1)
        bus_to = int(data_lines['Para'] - 1)
        coord = (bus_from, bus_to)
        bshunt = float(1/data_lines['C']) if data_lines['C'] > 0 else 0
        diag_value, out_diag_value = line_params(data_lines['R'], data_lines['X'], bshunt, data_lines['Tap'])
        _, line_admitance = line_params(data_lines['R'], data_lines['X'], 0, 0)
        line_admitance_shunt = bshunt*0.5j if bshunt > 0 else 0
        connect = {('g', *coord): line_admitance.real, 
                   ('b', *coord): line_admitance.imag,
                   ('gs', *coord): line_admitance_shunt.real if type(line_admitance_shunt) == complex else 0, 
                   ('bs', *coord): line_admitance_shunt.imag if type(line_admitance_shunt) == complex else 0}
        if len(connective_values) == 0:
            connective_values = connect.copy()
        else:
            connective_values.update(connect)
        y_bar_matriz[bus_from, bus_from] += diag_value
        y_bar_matriz[bus_to, bus_to] += diag_value if data_lines['Tap'] == 0 else diag_value*(data_lines['Tap']**2)
        y_bar_matriz[bus_from, bus_to] -= out_diag_value
        y_bar_matriz[bus_to, bus_from] -= out_diag_value
    return y_bar_matriz, connective_values

def add_susceptance_shunt(filepath, filename, ybar) -> np.ndarray:
    path_file = os.path.join(filepath, filename)
    susceptance_data = pd.read_excel(path_file)
    for lines in susceptance_data.iterrows():
        shunt_data = lines[1]
        bus = int(shunt_data['Bus'] - 1)
        ybar[bus, bus] += float(shunt_data['Shunt'])*1j
    return ybar

def pot_inj(voltage: np.ndarray, angle: np.ndarray, y_bar: np.ndarray) -> np.ndarray:
    complex_volt = nprect(voltage, np.deg2rad(angle))
    current = np.dot(y_bar, complex_volt)
    return complex_volt.T*np.conjugate(current)

def monte_carlo_state_estimation():
    y_bar_matriz, network_values = mount_y_bar('.', 'Dados_linha.xlsx')
    meansured, R, order_meansured = read_meansured('.','Meansured_data.xlsx')
    tol = 1e-4
    error = tol+1
    nits = 0
    results = []
    for _ in range(10000):
        meansured_smc = {}
        for key, val in meansured.items():
            for second_key, params in val.items():
                sampling_data = {second_key: (np.random.normal(*params), params[1])}
                if key not in meansured_smc.keys():
                    meansured_smc[key] = sampling_data
                else:
                    meansured_smc[key].update(sampling_data)
        error = tol+1
        nits = 0
        while error > tol:
            nits += 1
            if nits == 1:
                n_bus = y_bar_matriz.shape[0]
                states = [0]*(n_bus-1)
                states.extend([1]*n_bus)
                state_array = np.array(states, dtype=float)
            zArray, _ = measurement_Function(order_meansured, meansured_smc, y_bar_matriz, network_values, state_array)
            h_matrix = meansurement_jacobian(order_meansured, y_bar_matriz, network_values, state_array)
            g_matrix = get_G_matrix(h_matrix, R)
            H_t = np.transpose(h_matrix)
            R_inv = np.linalg.inv(R)
            h_r = H_t@R_inv
            t = h_r@zArray
            x_delta = np.linalg.solve(g_matrix, t)
            state_array += x_delta
            error = np.max(np.abs(x_delta))
        _, final_med = measurement_Function(order_meansured, meansured_smc, y_bar_matriz, network_values, state_array)
        results.append(final_med)
    pd.DataFrame(results).to_csv('resultado_smc_all_error.csv', decimal=',', sep = ';')

def linear_state_estimation(order_meansured: list, y_bar_matriz: np.ndarray):
    med_data = pd.DataFrame(columns = ['Meansured_Type', 'Location'])
    line_amount = np.sum([1 if list(x.keys())[0][0] == 'P' else 0 for x in order_meansured ])
    col_amount = y_bar_matriz.shape[0] - 1
    H_linear = np.zeros((line_amount, col_amount))
    l = 0
    for meansured in order_meansured:
        meansured_type = list(meansured.keys())[0]
        meansured_loc = list(meansured.values())[0]
        if meansured_type[0] != 'P':
            pass
        else:
            med_data.loc[len(med_data)] = [meansured_type, meansured_loc]
            if meansured_type.split('_')[-1] == 'flow':
                if meansured_loc[0] - 2 >= 0:
                    H_linear[l][meansured_loc[0] - 2] = 1
                if meansured_loc[1] - 2 >= 0:
                    H_linear[l][meansured_loc[1] - 2] = -1
            else:
                aux = y_bar_matriz[meansured_loc - 1][1:]
                conected = aux == 0
                H_linear[l][~conected] = -1
                if meansured_loc - 2 >= 0:
                    H_linear[l][meansured_loc - 2] = np.sum(conected)
            l += 1
    R = np.identity(line_amount)
    G = H_linear.T@H_linear
    try:
        detG = np.linalg.det(G)
        G_1 = np.linalg.inv(G)
        E = R - (H_linear@(G_1))@H_linear.T
    except:
        detG = 0
        G_1 = np.zeros(G.shape)
        E = np.zeros(R.shape)
    is_observable=False if detG <= 1e-11 else True
    return H_linear, E, med_data,is_observable

def identify_critical(E: np.ndarray, med_data: pd.core.frame.DataFrame):
    med_data['Criticality'] = np.nan
    amount_meansured = E.shape[0]
    residual = np.sum(E, axis = 1)
    standart_dev = np.sqrt(np.diag(E))
    aux = standart_dev[:,None]*standart_dev
    aux = np.where(aux == 0, 0.00000001, aux)
    gamma = np.divide(np.abs(E), aux)
    normalized_residual = np.abs(np.where(standart_dev == 0, 0, residual/standart_dev))
    normalized_residual__ = np.where(normalized_residual == 0, 0.000001, normalized_residual)
    rho = normalized_residual__[:,None]/normalized_residual__
    critical_meansured = (standart_dev <= 1e-6)*(residual <= 1e-6)
    number_cmeans = list(np.arange(amount_meansured)[critical_meansured])
    med_data.loc[med_data.index.isin(number_cmeans), 'Criticality'] = 'Medida Crítica'
    critical_sets = []
    csets = []
    amount_csets = 0
    for i in range(0, amount_meansured):
        for j in range(i+1, amount_meansured):
            if (rho[i][j] >= 0.98) and (gamma[i][j] >= 0.98) and (i not in number_cmeans) and (j not in number_cmeans):
                csets.append(i)
                csets.append(j)
        if any([set(csets).issubset(x) for x in critical_sets]):
            csets = []
        if len(csets) > 0:
            amount_csets += 1
            critical_sets += [set(csets)]
            med_data.loc[med_data.index.isin(csets), 'Criticality'] = f'Conj.Crítico_{amount_csets}'
            csets = []
    return med_data

def observable_system(meansured_data_instante = None, line_data = None) -> tuple:
    y_bar_matriz, network_values = mount_y_bar('.', '.', data = line_data)
    meansured, R, order_meansured = read_meansured('.', '.', data= meansured_data_instante)
    _, E, med_data,is_observable = linear_state_estimation(order_meansured, y_bar_matriz)
    if is_observable:
        criticality_data = identify_critical(E, med_data)
        mapping = {criticality_data.columns[0]:'Tipo', criticality_data.columns[1]: 'Localização', criticality_data.columns[2]:'Criticalidades'}
        criticality_data = criticality_data.rename(columns=mapping)
        return is_observable, criticality_data#.rename(columns= {"Meansured_Type": "Tipo",  "Location": "Localização", "Criticality": "Criticalidades"})
    else:
        return is_observable, None


def state_estimation(path = '.', line_params = 'Dados_linha_XIV_barras.xlsx', meansured_file = 'Meansured_data_XIV_bus.xlsx', meansured_data_instante = None, line_data = None):
    y_bar_matriz, network_values = mount_y_bar(path, line_params, data = line_data)
    meansured, R, order_meansured = read_meansured(path, meansured_file, data= meansured_data_instante)
    _, E, med_data,is_observable = linear_state_estimation(order_meansured, y_bar_matriz)
    criticality_data = identify_critical(E, med_data)
    tol = 1e-6
    error = tol+1
    nits = 0
    J_list = []
    while error > tol and nits<50:
        nits += 1
        if nits == 1:
            n_bus = y_bar_matriz.shape[0]
            states = [0]*(n_bus-1)
            states.extend([1]*n_bus)
            state_array = np.array(states, dtype=float)
        zArray, _ = measurement_Function(order_meansured, meansured, y_bar_matriz, network_values, state_array)
        h_matrix = meansurement_jacobian(order_meansured, y_bar_matriz, network_values, state_array)
        g_matrix = get_G_matrix(h_matrix, R)
        H_t = np.transpose(h_matrix)
        R_inv = np.linalg.inv(R)
        zArray = np.where(np.abs(zArray) < 1e-6, 0, zArray)
        J = np.sum(np.dot(zArray**2, R_inv))
        J_list.append(J)
        h_r = H_t@R_inv
        t = h_r@zArray
        x_delta = np.linalg.solve(g_matrix, t)
        state_array += x_delta
        error = np.max(np.abs(x_delta))
    # print('-----------------------------------')
    # print(f'Quantidade de Iterações: {nits} para uma tolerância de : {tol: .2e}')
    # print('-----------------------------------')
    State_dataframe = pd.DataFrame(state_array[n_bus-1:], columns = ['Mag. de Tensão'], index = list(range(1,n_bus+1)))
    State_dataframe['Ang.(°)'] = np.degrees([0]+state_array[:n_bus-1].tolist())
    Error_SE, zArray = measurement_Function(order_meansured, meansured, y_bar_matriz, network_values, state_array)
    data_SE = pd.DataFrame([med.keys() for med in order_meansured], columns = ['Tipos'])
    data_SE['Localização'] = [list(loc.values())[0] for loc in order_meansured]
    data_SE['Valor Medido'] = [meansured[list(x.keys())[0].split('_')[0]][list(x.values())[0]][0] for x in order_meansured]
    data_SE['Valor Estimado'] = zArray
    data_SE['Desvio'] = np.where(np.abs(Error_SE) < 1e-6, 0, Error_SE)
    Sigma = np.linalg.inv(g_matrix)
    Erii = np.abs(R - h_matrix@Sigma@H_t)
    Erii = np.sqrt(np.diag(Erii))
    data_SE['Res. Normalizado'] = np.where(Erii > 10e-10, np.abs(data_SE['Desvio']/Erii), np.inf)
    # data_SE['Error_Normalize'] = np.where(Erii > 0, data_SE['Error']/Erii, 0)
    # print('-----------------------------------')
    # print('Valor Final da Função Objetivo (J)')
    # J = Error_SE@R_inv
    # J = J@Error_SE
    # print(J)
    # print('-----------------------------------')
    ddof = data_SE.shape[0] - 2*(State_dataframe.shape[0]) + 1
    J_critical = chi2.ppf(1-0.05, ddof)
    mapping = {criticality_data.columns[0]:'Tipo', criticality_data.columns[1]: 'Localização', criticality_data.columns[2]:'Criticalidades'}
    criticality_data = criticality_data.rename(columns=mapping)

    data_SE['Tipos'] = data_SE['Tipos'].map({"P_flow": "Fluxo Pot. Ativ.", "Q_flow": "Fluxo Pot. Reativ.", "P_inj": "Injeção Pot. Ativ.", "Q_inj": "Injeção Pot. Reativ.",'V':'Módulo da Tensão'})
    criticality_data['Tipo'] = criticality_data['Tipo'].map({"P_flow": "Fluxo Pot. Ativ.", "Q_flow": "Fluxo Pot. Reativ.", "P_inj": "Injeção Pot. Ativ.", "Q_inj": "Injeção Pot. Reativ.",'V':'Módulo da Tensão'})
    critical_measured = criticality_data[criticality_data['Criticalidades'] == 'Medida Crítica']
    data_SE.loc[(data_SE['Tipos'].isin(critical_measured['Tipo'])) & (data_SE['Localização'].isin(critical_measured['Localização'])), 'Res. Normalizado'] = np.inf
    return y_bar_matriz, criticality_data, J_list, J_critical, State_dataframe, data_SE,is_observable


if __name__ == "__main__":
    y_bar_matriz, criticality_data, J_list, J_critical, State_dataframe, data_SE = state_estimation(line_params = 'Dados_linha_XIV_barras.xlsx', meansured_file = 'Meansured_data_XIV_bus.xlsx')
    print(data_SE)
    #Pode salvar dessa forma tanto o State_dataframe quanto o data_SE
    filename = 'Estado_Estimado.csv'
    State_dataframe.to_csv(filename, sep = ';', decimal = ',')


    #Utilização para Amostras Múltiplas
    # medidas_dia = pd.read_excel('Meansured_data_XIV_bus_multi_instant.xlsx')
    # cols = medidas_dia.columns[:-1]
    # residual_df = []

    # for inst in tqdm(medidas_dia['Instante'].unique()):
    #     df = medidas_dia[medidas_dia['Instante'] == inst][cols]
    #     _, _, _, _, _, data_SE = state_estimation(line_params='Dados_linha_XIV_barras_corrompidos_not_all.xlsx',meansured_data_instante=df)
    #     data_SE['Instante'] = inst
    #     residual_df.append(data_SE)
    # residual_df = pd.concat(residual_df, axis = 0)
    # residual_df.to_excel('dados_residuos_dia_corromp_aleatorio_not_all.xlsx')



    




