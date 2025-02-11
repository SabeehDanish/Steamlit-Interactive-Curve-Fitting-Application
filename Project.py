# Sabeeh Danish
# 2024-12-02
# Project

import streamlit as st

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

session = st.session_state
st.title("Curve Fitting Application")

def expand_data_array():
    session.dataset = np.vstack([session.dataset, ["", ""]])

def calculate_r_squared(y_true, y_pred):
    return 1 - np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2)

def calculate_errors(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred)), np.sqrt(np.mean((y_true - y_pred) ** 2))

def fit_linear(x_data, y_data):
    
    coeffs = np.polyfit(x_data, y_data, 1)
    y_pred = coeffs[0] * x_data + coeffs[1]
    r2 = calculate_r_squared(y_data, y_pred)
    mae, rmse = calculate_errors(y_data, y_pred)
    x_line = np.linspace(min(x_data), max(x_data), 500)
    
    return {"formula": f"y = {coeffs[0]:.2f}x + {coeffs[1]:.2f}", "r2": r2, "mae": mae, "rmse": rmse, "x_line": x_line, "y_line": coeffs[0] * x_line + coeffs[1]}

def fit_polynomial(x_data, y_data, degree):
    
    coeffs = np.polyfit(x_data, y_data, degree)
    poly_func = np.poly1d(coeffs)
    y_pred = poly_func(x_data)
    r2 = calculate_r_squared(y_data, y_pred)
    mae, rmse = calculate_errors(y_data, y_pred)
    x_line = np.linspace(min(x_data), max(x_data), 500)
    
    return {"formula": f"y = {' + '.join([f'{coeffs[i]:.2f}x^{len(coeffs) - i - 1}' for i in range(len(coeffs))]).replace('x^1', 'x').replace('x^0', '')}", "r2": r2, "mae": mae, "rmse": rmse, "x_line": x_line, "y_line": poly_func(x_line)}

def fit_exponential(x_data, y_data):
    
    def exp_model(x, a, b): return a * np.exp(b * x)
    params, _ = curve_fit(exp_model, x_data, y_data)
    y_pred = exp_model(x_data, *params)
    r2 = calculate_r_squared(y_data, y_pred)
    mae, rmse = calculate_errors(y_data, y_pred)
    x_line = np.linspace(min(x_data), max(x_data), 500)
    
    return {"formula": f"y = {params[0]:.2f}e^({params[1]:.2f}x)", "r2": r2, "mae": mae, "rmse": rmse, "x_line": x_line, "y_line": exp_model(x_line, *params)}

def fit_logarithmic(x_data, y_data):
    
    def log_model(x, a, b): return a + b * np.log(x)
    params, _ = curve_fit(log_model, x_data, y_data)
    y_pred = log_model(x_data, *params)
    r2 = calculate_r_squared(y_data, y_pred)
    mae, rmse = calculate_errors(y_data, y_pred)
    x_line = np.linspace(min(x_data), max(x_data), 500)
    
    return {"formula": f"y = {params[0]:.2f} + {params[1]:.2f}ln(x)", "r2": r2, "mae": mae, "rmse": rmse, "x_line": x_line, "y_line": log_model(x_line, *params)}

def fit_power_law(x_data, y_data):
    
    def power_model(x, a, b): return a * x**b
    params, _ = curve_fit(power_model, x_data, y_data)
    y_pred = power_model(x_data, *params)
    r2 = calculate_r_squared(y_data, y_pred)
    mae, rmse = calculate_errors(y_data, y_pred)
    x_line = np.linspace(min(x_data), max(x_data), 500)
    
    return {"formula": f"y = {params[0]:.2f}x^{params[1]:.2f}", "r2": r2, "mae": mae, "rmse": rmse, "x_line": x_line, "y_line": power_model(x_line, *params)}

def visualize_fit(x_data, y_data, x_line, y_line, title):
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(x_data, y_data, color="blue", label="Data Points")
    ax.plot(x_line, y_line, color="red", label=title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    ax.grid(True, color="#B0B0B0", linestyle='-', linewidth=0.5)
    ax.set_xticks(np.linspace(min(x_data), max(x_data), 5))
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)

def perform_curve_fitting(x_data, y_data):
    fit_type = st.selectbox("Select a fitting method:", ["", "Linear Regression", "Polynomial Fit", "Exponential Fit", "Logarithmic Fit", "Power Law Fit"])
    poly_degree = None
    
    if fit_type == "Polynomial Fit":
        poly_degree = st.number_input("Specify polynomial degree:", min_value=2, max_value=10, value=2)

    if fit_type and len(x_data) > 0 and len(y_data) > 0:
        
        try:
            if fit_type == "Linear Regression":
                result = fit_linear(x_data, y_data)
            elif fit_type == "Polynomial Fit":
                result = fit_polynomial(x_data, y_data, poly_degree)
            elif fit_type == "Exponential Fit":
                result = fit_exponential(x_data, y_data)
            elif fit_type == "Logarithmic Fit":
                result = fit_logarithmic(x_data, y_data)
            elif fit_type == "Power Law Fit":
                result = fit_power_law(x_data, y_data)
                
            st.write(f"**Formula:** {result['formula']}")
            st.write(f"**R² Value:** {result['r2']:.2f}")
            st.write(f"**Mean Absolute Error:** {result['mae']:.2f}")
            st.write(f"**Root Mean Square Error:** {result['rmse']:.2f}")
            
            visualize_fit(x_data, y_data, result["x_line"], result["y_line"], fit_type)
            
        except Exception as e:
            st.error(f"An error occurred during fitting: {e}")
    else:
        st.error("Please choose a fitting method and ensure data is available.")

if "dataset" not in session:
    session.dataset = np.array([["", ""]])

input_method = st.sidebar.radio("Choose Input Method", ("Manual Data Entry", "CSV File Upload"))

if input_method == "Manual Data Entry":
    
    st.write("Input your X and Y data. Use only numeric values.")

    input_data = []
    input_error = False
    
    for idx in range(session.dataset.shape[0]):
        col1, col2 = st.columns(2)
        x_val = col1.text_input(f"X[{idx+1}]", value=session.dataset[idx, 0], key=f"x_input_{idx}")
        y_val = col2.text_input(f"Y[{idx+1}]", value=session.dataset[idx, 1], key=f"y_input_{idx}")
        
        try:
            
            if x_val.strip(): float(x_val)
            if y_val.strip(): float(y_val)
        except ValueError:
            
            input_error = True
            st.error(f"Invalid entry in row {idx+1}. Please use only numeric values.")
            
        input_data.append([x_val, y_val])

    session.dataset = np.array(input_data)

    if not input_error and (session.dataset[-1, 0] != "" or session.dataset[-1, 1] != ""): expand_data_array()

    x_values = np.array([float(i) for i in session.dataset[:, 0] if i.strip()])
    y_values = np.array([float(i) for i in session.dataset[:, 1] if i.strip()])
    
    if len(x_values) > 0 and len(y_values) > 0:
        
        perform_curve_fitting(x_values, y_values)

elif input_method == "CSV File Upload":
    st.write("Upload a CSV file containing X and Y data. The file should have two columns without a header.")

    uploaded_file = st.file_uploader("Select a CSV file", type="csv")
    
    if uploaded_file:
        
        try:
            data_frame = pd.read_csv(uploaded_file, header=None)
            
            if data_frame.shape[1] == 2:
                x_values, y_values = data_frame[0].values, data_frame[1].values
                perform_curve_fitting(x_values, y_values)
            else:
                st.error("The CSV file must contain exactly two columns.")
                
        except Exception as e:
            st.error(f"Error while processing the CSV file: {e}")