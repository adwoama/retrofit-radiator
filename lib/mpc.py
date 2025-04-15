import numpy as np
from scipy.optimize import minimize

# functions for model predictive control

def fit_arx_model(data, p, q):
    """
    Fits an ARX model to the given data.

    Parameters:
        data (list of tuples): [(room_temp, radiator_temp), ...]
        p (int): Number of past room temperatures to use.
        q (int): Number of past radiator temperatures to use.

    Returns:
        tuple: Coefficients for room_temp (ar_coeffs) and radiator_temp (exog_coeffs).
    """
    room_temps = np.array([d[0] for d in data])
    radiator_temps = np.array([d[1] for d in data])
    X = []
    y = room_temps[max(p, q):]

    for i in range(max(p, q), len(data)):
        X.append(
            np.concatenate(
                [room_temps[i - p:i][::-1], radiator_temps[i - q:i][::-1]]
            )
        )

    X = np.array(X)
    coeffs = np.linalg.lstsq(X, y, rcond=None)[0]
    ar_coeffs = coeffs[:p]
    exog_coeffs = coeffs[p:]
    return ar_coeffs, exog_coeffs

def predict_arx(room_temps, radiator_temps, ar_coeffs, exog_coeffs):
    """
    Predicts the next room temperature using the ARX model.

    Parameters:
        room_temps (list): Past room temperatures.
        radiator_temps (list): Past radiator temperatures.
        ar_coeffs (list): AR coefficients.
        exog_coeffs (list): Exogenous input coefficients.

    Returns:
        float: Predicted room temperature.
    """
    ar_part = np.dot(ar_coeffs, room_temps[::-1])
    exog_part = np.dot(exog_coeffs, radiator_temps[::-1])
    return ar_part + exog_part

def run_mpc(schedule, ar_coeffs, exog_coeffs, p, q, horizon=6):
    """
    Executes the MPC logic to optimize radiator control.

    Parameters:
        schedule (dict): Desired temperature goals {time: temperature}.
        ar_coeffs (list): AR coefficients.
        exog_coeffs (list): Exogenous input coefficients.
        p (int): Number of past room temperatures to use.
        q (int): Number of past radiator temperatures to use.
        horizon (int): Prediction horizon (number of steps).

    Returns:
        list: Optimal radiator states (0 for off, 1 for on) over the horizon.
    """
    def cost_function(radiator_states):
        predicted_temps = list(room_temps[-p:])
        radiator_temps = list(radiator_states[-q:])
        cost = 0

        for t in range(horizon):
            predicted_temp = predict_arx(
                predicted_temps[-p:], radiator_temps[-q:], ar_coeffs, exog_coeffs
            )
            predicted_temps.append(predicted_temp)
            radiator_temps.append(radiator_states[t])
            goal_temp = schedule.get(t, predicted_temp)
            cost += (predicted_temp - goal_temp) ** 2 + 0.1 * radiator_states[t]

        return cost

    room_temps = [22] * p  # Placeholder for past room temperatures
    radiator_temps = [0] * q  # Placeholder for past radiator states
    initial_guess = [0] * horizon
    bounds = [(0, 1)] * horizon

    result = minimize(cost_function, initial_guess, bounds=bounds, method="SLSQP")
    return [round(x) for x in result.x]