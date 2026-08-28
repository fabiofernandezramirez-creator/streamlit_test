import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado que se conservan entre re-ejecuciones de Streamlit
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Contenedor dinámico reservado para el gráfico interactivo
chart_placeholder = st.empty()
# Inicializamos el gráfico con la probabilidad teórica inicial p = 0.5
chart_placeholder.line_chart([0.5])

def toss_coin(n):
    # Generación de la muestra de Bernoulli con p = 0.5
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)
    
    means_history = [0.5]
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        current_mean = outcome_1_count / outcome_no
        means_history.append(current_mean)
        
        # Redibujar la serie temporal completa en el contenedor
        chart_placeholder.line_chart(means_history)
        time.sleep(0.05)

    return current_mean

# Controles de interfaz de usuario
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    mean = toss_coin(number_of_trials)
    st.write(f'Media final calculada: {mean:.4f}')
    
    # Actualización del historial en session_state
    st.session_state['experiment_no'] += 1
    new_record = pd.DataFrame([{
        'no': st.session_state['experiment_no'],
        'iteraciones': number_of_trials,
        'media': mean
    }])
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_record], 
        ignore_index=True
    )

st.write('Esta aplicación aún no es funcional. En construcción.')

# Mostrar tabla acumulada si hay registros
if not st.session_state['df_experiment_results'].empty:
    st.subheader('Historial de experimentos')
    st.dataframe(st.session_state['df_experiment_results'])