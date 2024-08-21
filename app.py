import streamlit as st
import requests
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle

def preprocess_data(df):
    df_processed = df.copy()
    bool_columns = ['Olympiad_Participation', 'Scholarship', 'School', 'Projects', 'Medals', 'Career_sprt', 'Act_sprt', 'Fant_arts']
    for col in bool_columns:
        df_processed[col] = df_processed[col].map({'Yes': 1, 'No': 0})
    df_processed['Won_arts'] = df_processed['Won_arts'].map({'Yes': 1, 'No': 0, 'Maybe': 0.5})
    le = LabelEncoder()
    df_processed['Fav_sub'] = le.fit_transform(df_processed['Fav_sub'])
    scaler = StandardScaler()
    numerical_columns = ['Grasp_pow', 'Time_sprt', 'Time_art']
    df_processed[numerical_columns] = scaler.fit_transform(df_processed[numerical_columns])
    return df_processed

with open('./models/knn_model.pkl', 'rb') as file:
    loaded_knn = pickle.load(file)

# Custom CSS for styling
st.markdown(
    """
    <style>
    /* Increase font size of labels and input elements */
    .stSelectbox label, .stSlider label {
        font-size: 18px;
    }
    
    .stSelectbox div[data-baseweb="select"] > div {
        font-size: 18px;
    }

    .stSlider > div > div {
        font-size: 18px;
    }

    /* Increase size of input elements */
    .stSelectbox div[data-baseweb="select"] {
        min-height: 45px;
    }

    .stSlider > div > div > div {
        height: 36px;
    }

    /* Adjust spacing between columns */
    div[data-testid="column"] {
        padding: 0 20px;
    }

    /* Add spacing within column boundaries */
    .stSelectbox, .stSlider {
        margin-bottom: 25px;
    }

    /* Change slider value color to blue */
    .stSlider > div > div > div > div > div {
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Hobby Recommendation System")
st.divider()

# Create three columns with adjusted width and spacing for input fields
col1, col2, col3 = st.columns(3)

with col1:
    st.selectbox('Olympiad Participation', ['Yes', 'No'], key='Olympiad_Participation')
    st.selectbox('Scholarship', ['Yes', 'No'], key='Scholarship')
    st.selectbox('School', ['Yes', 'No'], key='School')
    st.selectbox('Favorite Subject', ['Mathematics', 'Science', 'Arts', 'Literature', 'History'], key='Fav_sub')

with col2:
    st.selectbox('Projects', ['Yes', 'No'], key='Projects')
    st.slider('Grasp Power (1-6)', 1, 6, 5, key='Grasp_pow')
    st.slider('Time spent on Sports (hours)', 0, 6, 2, key='Time_sprt')
    st.selectbox('Medals', ['Yes', 'No'], key='Medals')

with col3:
    st.selectbox('Interested in Sports as Career', ['Yes', 'No'], key='Career_sprt')
    st.selectbox('Actively participates in Sports', ['Yes', 'No'], key='Act_sprt')
    st.selectbox('Fantasize about Arts', ['Yes', 'No'], key='Fant_arts')
    st.selectbox('Has Won in Arts Competitions', ['Yes', 'No', 'Maybe'], key='Won_arts')
    st.slider('Time spent on Arts (hours)', 0, 6, 3, key='Time_art')

# Create a sidebar for the result
with st.sidebar:
    st.header("Results")

    # Define the button and results display in the sidebar
    if st.button('Predict Hobby'):
        input_data = {
            'Olympiad_Participation': st.session_state.Olympiad_Participation,
            'Scholarship': st.session_state.Scholarship,
            'School': st.session_state.School,
            'Fav_sub': st.session_state.Fav_sub,
            'Projects': st.session_state.Projects,
            'Grasp_pow': st.session_state.Grasp_pow,
            'Time_sprt': st.session_state.Time_sprt,
            'Medals': st.session_state.Medals,
            'Career_sprt': st.session_state.Career_sprt,
            'Act_sprt': st.session_state.Act_sprt,
            'Fant_arts': st.session_state.Fant_arts,
            'Won_arts': st.session_state.Won_arts,
            'Time_art': st.session_state.Time_art
        }
        
        input_df = pd.DataFrame([input_data])
        input_processed = preprocess_data(input_df)
        hobby = loaded_knn.predict(input_processed)[0]

        if hobby:
            st.write(f"Recommended hobby: {hobby}")
        else:
            st.write("An error occurred during the prediction process.")
