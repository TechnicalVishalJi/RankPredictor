from flask import Flask, render_template, request, jsonify
import pandas as pd
from college_predictor_2023 import load_data as load_data_2023, predict_colleges as predict_colleges_2023
from college_predictor_2024 import load_data as load_data_2024, predict_colleges as predict_colleges_2024
from combined_predictor import percentile_to_rank

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Collect data from json
        is_jee_advanced = data.get("is_jee_advanced") == "yes"
        main_perc = float(data.get("percentile")) if data.get("percentile") else None
        main_rank = int(data.get("main_rank")) if data.get("main_rank") else None
        advanced_rank = int(data.get("advanced_rank")) if data.get("advanced_rank") else None
        category = data.get("category") if data.get("category") else None
        gender = data.get("gender") if data.get("gender") else None
        
        if main_perc and not main_rank:
            main_rank = percentile_to_rank(main_perc)

        # Predict colleges for 2023
        results_2023 = predict_colleges_2023(
            load_data_2023(), main_rank, advanced_rank, category, gender, is_jee_advanced
        )

        # Predict colleges for 2024
        results_2024 = predict_colleges_2024(
            load_data_2024(), main_rank, advanced_rank, category, gender, is_jee_advanced
        )

        # Convert to HTML tables
        results_2023_html = results_2023.to_html(classes='table table-bordered') if not results_2023.empty else "No results for 2023."
        results_2024_html = results_2024.to_html(classes='table table-bordered') if not results_2024.empty else "No results for 2024."

        return jsonify({
            "results_2023": results_2023_html,
            "results_2024": results_2024_html,
            "main_rank": main_rank,
            "advanced_rank": advanced_rank,
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)