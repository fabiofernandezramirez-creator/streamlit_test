import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado que persisten entre ejecuciones reactivas
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Contenedor dinámico mutable para el gráfico en tiempo real
chart_placeholder = st.empty()
chart_placeholder.line_chart([0.5])

def toss_coin(n):
    # Generación de la muestra aleatoria de Bernoulli (p = 0.5)
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0
    means_history = [0.5]

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        means_history.append(mean)
        
        # Actualización reactiva sobre el contenedor
        chart_placeholder.line_chart(means_history)
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    mean = toss_coin(number_of_trials)
    st.write(f'Media final obtenida: {mean:.4f}')

st.write('Esta aplicación aún no es funcional. En construcción.')