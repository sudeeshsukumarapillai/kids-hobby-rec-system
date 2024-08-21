from flask import Flask, request, jsonify
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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

@app.route('/predict', methods=['POST'])
def predict_hobby():
    data = request.json
    input_df = pd.DataFrame([data])
    input_processed = preprocess_data(input_df)
    hobby = loaded_knn.predict(input_processed)[0]
    return jsonify({'recommended_hobby': hobby})

if __name__ == '__main__':
    app.run(debug=True)
