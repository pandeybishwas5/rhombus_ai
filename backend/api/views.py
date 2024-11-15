import os
import pandas as pd
import io
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import FileUploadSerializer
from api.utils import infer_and_convert_data_types
from concurrent.futures import ThreadPoolExecutor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_chunk(df_chunk: pd.DataFrame) -> pd.DataFrame:
    """
    Process a chunk of data, including data type inference, NaN handling, and memory optimization.
    """
    # Capture data types before transformation
    data_types_before = df_chunk.dtypes.astype(str).to_dict()

    # Infer and convert data types
    df_chunk = infer_and_convert_data_types(df_chunk)

    # Capture data types after transformation
    data_types_after = df_chunk.dtypes.astype(str).to_dict()

    # Clean up NaN, Infinity, and -Infinity values
    df_chunk = df_chunk.applymap(lambda x: None if isinstance(x, float) and (pd.isna(x) or x == float('inf') or x == float('-inf')) else x)

    # Handle categorical columns (ensure empty string is a valid category)
    for column in df_chunk.columns:
        if pd.api.types.is_categorical_dtype(df_chunk[column]):
            # Add 'NA' as a category to categorical columns before filling missing values
            if 'NA' not in df_chunk[column].cat.categories:
                df_chunk[column] = df_chunk[column].cat.add_categories('NA')
        df_chunk[column] = df_chunk[column].fillna('NA')

    # Replace NaN and None with 'NA' across the DataFrame
    df_chunk = df_chunk.fillna('NA')

    return df_chunk, data_types_before, data_types_after

@api_view(['POST'])
def upload_file(request):
    if request.method == 'POST':
        # Validate file type (check for .csv or .xlsx)
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            logging.error("No file uploaded.")
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the file extension
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        file_extension = file_extension.lower()

        # Check if the file is a CSV or Excel file
        if file_extension not in ['.csv', '.xlsx']:
            logging.error(f"Invalid file type: {file_extension}. Only .csv and .xlsx files are allowed.")
            return Response({"error": "Invalid file type. Only .csv and .xlsx files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Read the file content
            file_content = uploaded_file.read()

            # Handle CSV and Excel files differently
            if file_extension == '.csv':
                # Read CSV in chunks to avoid memory overload
                chunk_size = 10000  # You can adjust this based on the memory constraints
                chunked_df = pd.read_csv(io.BytesIO(file_content), chunksize=chunk_size)

                # Process each chunk in parallel
                with ThreadPoolExecutor(max_workers=4) as executor:
                    results = list(executor.map(process_chunk, chunked_df))
                
                # Concatenate all processed chunks into a single DataFrame
                final_df = pd.concat([result[0] for result in results], ignore_index=True)
                data_types_before = results[0][1]  # Get from the first chunk
                data_types_after = results[0][2]  # Get from the first chunk

                logging.info(f"CSV file '{uploaded_file.name}' processed successfully.")

            elif file_extension == '.xlsx':
                # Handle Excel file similarly, but you might consider limiting the number of rows read at a time
                df = pd.read_excel(io.BytesIO(file_content))
                final_df, data_types_before, data_types_after = process_chunk(df)
                logging.info(f"Excel file '{uploaded_file.name}' processed successfully.")

            # Return the data as JSON with before and after data types
            response_data = {
                'data': final_df.to_dict(orient='records'),
                'data_types_before': data_types_before,
                'data_types_after': data_types_after
            }

            logging.info(f"Processed file '{uploaded_file.name}' successfully.")
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logging.error(f"Error processing file '{uploaded_file.name}': {e}")
            return Response({"error": f"An error occurred while processing the file: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
