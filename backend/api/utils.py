import pandas as pd
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV or Excel file into a DataFrame.
    """
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("File format not supported. Please provide a CSV or Excel file.")
        logging.info(f"File loaded successfully: {file_path}")
        return df
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {e}")
        raise

def handle_object_column_conversion(df: pd.DataFrame, col: str, unique_ratio_threshold: float) -> pd.DataFrame:
    """
    Attempt to convert object column to numeric, datetime, or categorical.
    """
    try:
        # Try converting to numeric
        converted_numeric = pd.to_numeric(df[col], errors='coerce')
        if converted_numeric.notna().sum() > 0:
            df[col] = converted_numeric
            logging.info(f"Converted column '{col}' to numeric.")
            return df
        
        # Try converting to datetime
        converted_datetime = pd.to_datetime(df[col], errors='coerce', format='%d/%m/%Y')
        if converted_datetime.notna().sum() > 0:
            df[col] = converted_datetime
            logging.info(f"Converted column '{col}' to datetime.")
            return df
        
        # Convert to Categorical if unique ratio is below threshold
        unique_ratio = len(df[col].unique()) / len(df[col])
        if unique_ratio < unique_ratio_threshold:
            df[col] = pd.Categorical(df[col])
            logging.info(f"Converted column '{col}' to categorical.")
        else:
            df[col] = df[col].astype(str)  # Keep as string if no better conversion
            logging.info(f"Column '{col}' remains as string due to high unique ratio.")
        return df
    except Exception as e:
        logging.error(f"Error converting column '{col}': {e}")
        raise

def infer_and_convert_data_types(df: pd.DataFrame, unique_ratio_threshold: float = 0.5) -> pd.DataFrame:
    """
    Infers and converts data types of each column in a DataFrame.
    """
    for col in df.columns:
        original_dtype = df[col].dtype
        logging.info(f"Processing column '{col}' with original dtype {original_dtype}")
        
        # Handle object columns and try to convert them to appropriate types
        if pd.api.types.is_object_dtype(df[col]):
            df = handle_object_column_conversion(df, col, unique_ratio_threshold)
        
    # Downcast numeric columns for memory optimization
    for col in df.select_dtypes(include=['int64', 'float64']).columns:
        df[col] = pd.to_numeric(df[col], downcast='integer' if pd.api.types.is_integer_dtype(df[col]) else 'float')
        logging.info(f"Downcasted column '{col}' to smaller numeric type.")

    return df

def main(file_path: str):
    """
    Main function to load data, infer data types, and display results.
    """
    try:
        df = load_data(file_path)
        logging.info("Data loaded successfully.")
        
        # Data types before inference
        logging.info("Data types before inference:")
        logging.info(df.dtypes)
        
        # Infer and convert data types
        df = infer_and_convert_data_types(df)
        
        # Data types after inference
        logging.info("Data types after inference:")
        logging.info(df.dtypes)
        
        # Display a sample of the DataFrame
        logging.info("Sample DataFrame:")
        logging.info(df.head())
    except Exception as e:
        logging.error(f"An error occurred during the data processing: {e}")

# Example usage
if __name__ == "__main__":
    file_path = "sample_data.csv"  # Replace with your file path
    main(file_path)
