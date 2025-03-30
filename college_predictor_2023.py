import pandas as pd

def load_data():
    # Load all rounds of data into a single DataFrame
    rounds = [1, 2, 3, 4, 5]
    data_frames = []
    for round_num in rounds:
        file_path = f"2023 round {round_num}.csv"
        try:
            df = pd.read_csv(file_path)
            df['Round'] = round_num  # Add a column to indicate the round

            # Convert 'Opening Rank' and 'Closing Rank' to numeric, coercing errors to NaN
            df['Opening Rank'] = pd.to_numeric(df['Opening Rank'], errors='coerce')
            df['Closing Rank'] = pd.to_numeric(df['Closing Rank'], errors='coerce')

            # Drop rows where 'Opening Rank' or 'Closing Rank' is NaN
            df = df.dropna(subset=['Opening Rank', 'Closing Rank'])

            data_frames.append(df)
        except FileNotFoundError:
            print(f"File {file_path} not found. Skipping...")
    return pd.concat(data_frames, ignore_index=True)

def predict_colleges(data, main_rank, advanced_rank, category, gender, is_jee_advanced):
    try:
        if is_jee_advanced:
            # Filter IITs using JEE Advanced rank
            iit_data = data[
                (data['Institute'].str.contains("Indian Institute of Technology")) &
                (data['Seat Type'] == category) &
                (data['Gender'] == gender) &
                (data['Closing Rank'] >= advanced_rank)
            ]
            # Filter other colleges using JEE Main rank
            other_colleges_data = data[
                (~data['Institute'].str.contains("Indian Institute of Technology")) &
                (data['Seat Type'] == category) &
                (data['Gender'] == gender) &
                (data['Closing Rank'] >= main_rank)
            ]
            return pd.concat([iit_data, other_colleges_data], ignore_index=True)
        else:
            # Only consider JEE Main rank for all colleges
            filtered_data = data[
                (data['Seat Type'] == category) &
                (data['Gender'] == gender) &
                (data['Closing Rank'] >= main_rank)
            ]
            return filtered_data[['Institute', 'Academic Program Name', 'Round', 'Opening Rank', 'Closing Rank']]
    except Exception as e:
        print(f"Error in predict_colleges: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error

def main_2023():
    print("Loading data...")
    data = load_data()
    print("Data loaded successfully!")

    # Ask if the user has taken JEE Advanced
    is_jee_advanced = input("Have you taken the JEE Advanced exam? (yes/no): ").strip().lower() == "yes"

    if is_jee_advanced:
        # Get both JEE Main and JEE Advanced ranks
        main_rank = int(input("Enter your JEE Main rank: "))
        advanced_rank = int(input("Enter your JEE Advanced rank: "))
    else:
        # Get only JEE Main rank
        main_rank = int(input("Enter your JEE Main rank: "))
        advanced_rank = None

    # Get other user inputs
    category = input("Enter your category (e.g., OPEN, EWS, OBC-NCL, SC, ST): ").strip()
    gender = input("Enter your gender (Gender-Neutral or Female-only (including Supernumerary)): ").strip()

    # Predict colleges
    print("\nPredicting colleges...")
    results = predict_colleges(data, main_rank, advanced_rank, category, gender, is_jee_advanced)

    if results.empty:
        print("No colleges found for the given rank and criteria.")
    else:
        print("\nPossible colleges and programs:")
        print(results.to_string(index=False))

        # Save results to a CSV file
        output_file = "predicted_colleges_2023.csv"
        results.to_csv(output_file, index=False)
        print(f"\nResults have been saved to {output_file}")

if __name__ == "__main__":
    main_2023()