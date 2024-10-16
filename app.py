from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model
model = joblib.load('decision_tree_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    protein = data['protein']
    carbs = data['carbs']
    fat = data['fat']

    # Create input data
    input_data = pd.DataFrame([[protein, carbs, fat]], columns=['Protein(g)', 'Carbs(g)', 'Fat(g)'])

    # Use the trained model to predict the diet type and cuisine type
    predicted_labels = model.predict(input_data)
    predicted_diet, predicted_cuisine = predicted_labels[0]

    # Define the tolerance range
    tolerance = 0.1
    protein_min, protein_max = protein * (1 - tolerance), protein * (1 + tolerance)
    carbs_min, carbs_max = carbs * (1 - tolerance), carbs * (1 + tolerance)
    fat_min, fat_max = fat * (1 - tolerance), fat * (1 + tolerance)

    # Load the dataset
    all_diets = pd.read_csv('combined_diets.csv')  # Update with the correct path

    # Filter the dataset for the given nutritional details within the tolerance range
    filtered_data = all_diets[(all_diets['Protein(g)'] >= protein_min) & (all_diets['Protein(g)'] <= protein_max) &
                              (all_diets['Carbs(g)'] >= carbs_min) & (all_diets['Carbs(g)'] <= carbs_max) &
                              (all_diets['Fat(g)'] >= fat_min) & (all_diets['Fat(g)'] <= fat_max)]

    # Decode the labels
    le_diet = joblib.load('le_diet.pkl')  # Load the label encoder for diet
    le_cuisine = joblib.load('le_cuisine.pkl')  # Load the label encoder for cuisine
    filtered_data['Diet_type'] = le_diet.inverse_transform(filtered_data['Diet_type'])
    filtered_data['Cuisine_type'] = le_cuisine.inverse_transform(filtered_data['Cuisine_type'])

    # Sort by Euclidean distance to the input values and select the top recipes
    filtered_data['distance'] = ((filtered_data['Protein(g)'] - protein)**2 + 
                                 (filtered_data['Carbs(g)'] - carbs)**2 + 
                                 (filtered_data['Fat(g)'] - fat)**2)**0.5
    selected_recipes = filtered_data.nsmallest(5, 'distance')

    # Convert the selected recipes to a list of dictionaries
    results = selected_recipes[['Recipe_name', 'Diet_type', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']].to_dict(orient='records')

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
