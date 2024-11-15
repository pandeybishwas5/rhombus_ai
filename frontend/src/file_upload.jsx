import axios from 'axios';
import React, { useState } from 'react';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState(null);
  const [updatedDataTypes, setUpdatedDataTypes] = useState({}); // Track overridden categories

  // Mapping backend data types to user-friendly names
  const mapDataType = (dataType) => {
    const typeMapping = {
      object: 'Text',
      'datetime64[ns]': 'Date',
      datetime64: 'Date',
      category: 'Category',
      float32: 'Number',
      float64: 'Number',
      int32: 'Number',
      int8: 'Number',
      int16: 'Number',
      int64: 'Number',
      bool: 'Boolean',
      number: 'Number',
      date: 'Date',
      boolean: 'Boolean',
    };

    return typeMapping[dataType?.toLowerCase()] || 'Text'; // Default to 'Text' if no mapping found
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setResponseData(null); // Clear the previous response data
      setUpdatedDataTypes({}); // Reset the data type overrides
      setErrorMessage(null); // Clear error messages
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    setLoading(true);
    setErrorMessage(null); // Reset any previous error message

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      // Log raw data types received from the backend
      console.log('Raw data types from backend:', response.data);

      setResponseData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error uploading file:', error);

      if (error.response?.data?.error) {
        setErrorMessage(error.response.data.error);
      } else {
        setErrorMessage('An unknown error occurred.');
      }
      setLoading(false);
    }
  };

  // Handle changes to the data type selection
  const handleDataTypeChange = (column, newDataType) => {
    setUpdatedDataTypes((prevState) => ({
      ...prevState,
      [column]: newDataType,
    }));
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Upload CSV File</h1>
      <input
        type="file"
        onChange={handleFileChange}
        style={{ padding: '10px', fontSize: '16px' }}
      />
      <button
        onClick={handleUpload}
        disabled={loading}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          cursor: 'pointer',
          marginLeft: '10px',
        }}
      >
        {loading ? 'Uploading...' : 'Upload'}
      </button>

      {/* Display error message if there's an error */}
      {errorMessage && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          <strong>{errorMessage}</strong>
        </div>
      )}

      {/* Display the processed data if available */}
      {responseData && (
        <div>
          <h2>Processed Data</h2>
          <table
            border="1"
            cellPadding="10"
            style={{
              marginTop: '10px',
              width: '100%',
              textAlign: 'left',
              overflowX: 'scroll', // Make the table scrollable
            }}
          >
            <thead>
              <tr>
                {Object.keys(responseData.data[0]).map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {responseData.data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {Object.keys(row).map((col, colIndex) => (
                    <td key={colIndex}>{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>

          <h2>Data Types Before Inference</h2>
          <table
            border="1"
            cellPadding="10"
            style={{
              marginTop: '10px',
              width: '100%',
              textAlign: 'left',
              overflowX: 'auto', // Make the table scrollable
            }}
          >
            <thead>
              <tr>
                {Object.keys(responseData.data_types_before).map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              <tr>
                {Object.values(responseData.data_types_before).map((type, index) => (
                  <td key={index}>{type}</td>
                ))}
              </tr>
            </tbody>
          </table>

          <h2>Data Types After Inference</h2>
          <table
            border="1"
            cellPadding="10"
            style={{
              marginTop: '10px',
              width: '100%',
              textAlign: 'left',
              overflowX: 'auto', // Make the table scrollable
            }}
          >
            <thead>
              <tr>
                <th>Column</th>
                <th>Data Type After</th>
                <th>Update Data Type</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(responseData.data_types_after).map(([column, type]) => (
                <tr key={column}>
                  <td>{column}</td>
                  <td>{mapDataType(updatedDataTypes[column] || type)}</td>
                  <td>
                    <select
                      value={updatedDataTypes[column] || mapDataType(type)}
                      onChange={(e) => handleDataTypeChange(column, e.target.value)}
                      style={{ padding: '5px', fontSize: '14px' }}
                    >
                      <option value="Text">Text</option>
                      <option value="Number">Number</option>
                      <option value="Boolean">Boolean</option>
                      <option value="Date">Date</option>
                      <option value="Category">Category</option>
                    </select>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
