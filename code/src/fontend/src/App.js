import React, { useState } from 'react';
import axios from 'axios';
import * as constants from "./constants"


const App = () => {
    // State to manage file and category
    const [selectedFile, setSelectedFile] = useState(null);
    const [category, setCategory] = useState('');
    const [csvUrl, setCsvUrl] = useState(null);
    const [loading, setLoading] = useState(true);
    const [fetchComplete, setFetchComplete] = useState(false);

    // Handle file selection
    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
            console.log(`📂 Selected file: ${file.name}`);
            setSelectedFile(file);
        }
    };

    // Handle dropdown change
    const handleCategoryChange = (event) => {
        setCategory(event.target.value);
    };

    // Handle form submission
    const handleSubmit = async (event) => {
        var file_path
        event.preventDefault();

        if (!selectedFile || !category) {
            alert('❗️ Please select a file and choose a category.');
            return;
        }
        var dict
        if(category.toLowerCase().match("ihub")) {
            dict = constants.ihub
        }else{
            dict=constants.catalyst
        }

        // Prepare form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('category', category);
        // Object.keys(dict).forEach(key => {
        //     formData.append(key, dict[key]);
        // })

        try {
            // Send file and category to backend API
            const response = await axios.post('http://localhost:8000/api/fileupload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                reponseType: 'application/json',
            });


            const upload_loaction = response.data["file_path"]
            file_path = upload_loaction
            alert(`✅ File uploaded successfully! Saved at ${upload_loaction}`);
        } catch (error) {
            console.error('❌ Error uploading file:', error);
            alert('❌ Error uploading file. Please try again.');
        }

        const formData_predict = new FormData();
        formData_predict.append('file_path', file_path);
        formData_predict.append('usecase_id',category);
        Object.keys(dict).forEach((key) => {
            const value = dict[key];

            // Check if value is a list/array
            if (Array.isArray(value)) {
                value.forEach((item) => {
                    formData.append(`${key}[]`, item); // Append as key[]
                });
            } else {
                formData.append(key, value); // Append single values
            }
        });
        try {
            // Send file and category to backend API
            const response = await axios.post('http://localhost:8000/api/predict', formData_predict, {
                headers: { 'Content-Type': 'application/json' },
                reponseType: 'text/csv',
            });
            const response_blob = new Blob([response.data],{type: 'text/csv'});
            const url = window.URL.createObjectURL(response_blob);
            setCsvUrl(url);
            setFetchComplete(true);
            setLoading(false);

            // alert(``);
        } catch (error) {
            console.error('❌ Error uploading file:', error);
            alert('File ready for download');
        }

    };
    const downloadCSV = () => {
        console.log("Downloading CSV...");
        if (csvUrl) {
            const link = document.createElement("a");
            link.href = csvUrl;

            // Set a dynamic file name
            link.setAttribute("download", `data_${Date.now()}.csv`);
            document.body.appendChild(link);
            link.click();

            // Clean up and revoke URL after download
            link.parentNode.removeChild(link);
            window.URL.revokeObjectURL(csvUrl);
        }
    };

    return (
        <div className="container">
            <h2 className="title">Anomaly Detection UI</h2>
            <br/>
            <form onSubmit={handleSubmit}>
                {/* File Upload */}
                <div className="form-group">
                    <label>Upload File:</label>
                    <input type="file" className="form-control" onChange={handleFileChange} />
                    {selectedFile && <p>📂 Selected File: {selectedFile.name}</p>}
                </div>

                {/* Dropdown for Category */}
                <div className="form-group">
                    <label>Select Category:</label>
                    <select className="form-control" value={category} onChange={handleCategoryChange}>
                        <option value="">-- Choose a Category --</option>
                        <option value="ihub">iHub</option>
                        <option value="catalyst">Catalyst</option>
                    </select>
                </div>

                {/* Submit Button */}
                <button type="submit" className="btn btn-primary">
                    Upload
                </button>
                <br/>
                <br/>
            </form>
            {csvUrl && (
                <button
                    disabled={loading || !fetchComplete}
                    onClick={downloadCSV}
                    style={{
                        backgroundColor: "green",
                        color: "white",
                        padding: "10px 20px",
                        border: "none",
                        borderRadius: "5px",
                        cursor: "pointer",
                    }}
                >
                    Download CSV ⬇️
                </button>
            )}
        </div>
    );
};

export default App;
