from college_predictor_2023 import load_data as load_data_2023, predict_colleges as predict_colleges_2023
from college_predictor_2024 import load_data as load_data_2024, predict_colleges as predict_colleges_2024

def collect_inputs():
    """Collect user inputs for prediction."""
    print("Welcome to the College Predictor!")
    
    # Ask if the user has taken JEE Advanced
    is_jee_advanced = input("Have you taken the JEE Advanced exam? (yes/no): ").strip().lower() == "yes"

    # Get rank or percentile inputs
    main_rank = None
    if input("Do you know your JEE Main rank? (yes/no): ").strip().lower() == "yes":
        main_rank = int(input("Enter your JEE Main rank: "))
    else:
        percentile = float(input("Enter your percentile: "))
        #total_candidates = int(input("Enter the total number of candidates who appeared for JEE Main: "))
        main_rank = int((100-percentile)*13716)
        print(f"Your estimated JEE Main rank is: {main_rank}")

    advanced_rank = None
    if is_jee_advanced:
        advanced_rank = int(input("Enter your JEE Advanced rank: "))

    # Get other user inputs
    category = input("Enter your category (e.g., OPEN, EWS, OBC-NCL, SC, ST): ").strip()
    gender = input("Enter your gender (Gender-Neutral or Female-only (including Supernumerary)): ").strip()

    # Optional filters
    round_no = input("Enter round number (1-5, or leave blank for all): ").strip()
    # Convert round_no to integer if provided
    round_no = int(round_no) if round_no else None

    return {
        "is_jee_advanced": is_jee_advanced,
        "main_rank": main_rank,
        "advanced_rank": advanced_rank,
        "category": category,
        "gender": gender,
        "round_no": round_no,
    }

def apply_filters(results, institute_type, round_no, branch):
    """Apply additional filters to the results."""
    if institute_type:
        results = results[results['Institute'].str.contains(institute_type, case=False)]
    if round_no:
        results = results[results['Round'] == round_no]
    if branch:
        results = results[results['Academic Program Name'].str.contains(branch, case=False)]
    return results

def main():
    # Collect inputs
    inputs = collect_inputs()

    # Load data for 2023 and 2024
    print("\nLoading 2023 data...")
    data_2023 = load_data_2023()
    print("2023 data loaded successfully!")

    print("\nLoading 2024 data...")
    data_2024 = load_data_2024()
    print("2024 data loaded successfully!")

    # Run predictions for 2023
    print("\nRunning predictions for 2023...")
    results_2023 = predict_colleges_2023(
        data_2023,
        inputs["main_rank"],
        inputs["advanced_rank"],
        inputs["category"],
        inputs["gender"],
        inputs["is_jee_advanced"]
    )
    results_2023 = apply_filters(results_2023, inputs["institute_type"], inputs["round_no"], inputs["branch"])

    # Run predictions for 2024
    print("\nRunning predictions for 2024...")
    results_2024 = predict_colleges_2024(
        data_2024,
        inputs["main_rank"],
        inputs["advanced_rank"],
        inputs["category"],
        inputs["gender"],
        inputs["is_jee_advanced"]
    )
    results_2024 = apply_filters(results_2024, inputs["institute_type"], inputs["round_no"], inputs["branch"])

    # Display results
    if results_2023.empty and results_2024.empty:
        print("\nNo colleges found for the given rank and criteria.")
    else:
        print("\nPossible colleges and programs for 2023:")
        if not results_2023.empty:
            print(results_2023.to_string(index=False))
            results_2023.to_csv("predicted_colleges_2023_filtered.csv", index=False)
            print("\nFiltered results for 2023 have been saved to 'predicted_colleges_2023_filtered.csv'")
        else:
            print("No results for 2023.")

        print("\nPossible colleges and programs for 2024:")
        if not results_2024.empty:
            print(results_2024.to_string(index=False))
            results_2024.to_csv("predicted_colleges_2024_filtered.csv", index=False)
            print("\nFiltered results for 2024 have been saved to 'predicted_colleges_2024_filtered.csv'")
        else:
            print("No results for 2024.")

if __name__ == "__main__":
    main()