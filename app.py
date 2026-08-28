import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado persistentes en la sesión de Streamlit
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media'])

st.header('Lanzar una moneda')

# Contenedor dinámico reservado para redibujar el gráfico iterativamente
chart_placeholder = st.empty()
chart_placeholder.line_chart([0.5])

def toss_coin(n):
    # Ensayos independientes de Bernoulli con p = 0.5
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
        
        # Redibujamos la secuencia en el contenedor dinámico
        chart_placeholder.line_chart(means_history)
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    
    # Registro del ensayo en el DataFrame acumulativo de la sesión
    new_row = pd.DataFrame(
        data=[[st.session_state['experiment_no'], number_of_trials, mean]],
        columns=['no', 'iteraciones', 'media']
    )
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_row],
        axis=0
    ).reset_index(drop=True)

# Visualización de la tabla histórica de experimentos
st.write(st.session_state['df_experiment_results'])