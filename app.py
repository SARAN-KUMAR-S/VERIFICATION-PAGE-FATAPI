from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import pandas as pd

# Load the dataset
file_path = "gct-int-students.csv"
students_data = pd.read_csv(file_path)

# Initialize FastAPI app
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, certificate_no: str = None):
    """
    Render the home page with a form to verify the certificate.
    """
    # HTML structure
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Certificate Verification</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
            }
            .container {
                max-width: 600px;
                margin: 50px auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #333;
            }
            form {
                margin-bottom: 20px;
            }
            label {
                font-weight: bold;
                display: block;
                margin-bottom: 8px;
            }
            input {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            button {
                background-color: #007BFF;
                color: #fff;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .error {
                color: red;
                font-weight: bold;
            }
            .result {
                margin-top: 20px;
                padding: 15px;
                background-color: #e6f7e6;
                border: 1px solid #b2d8b2;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Certificate Verification</h1>
            <form action="/" method="get">
                <label for="certificate-no">Enter Certificate Number:</label>
                <input type="text" id="certificate-no" name="certificate_no" placeholder="GCT-INT-XXX" required>
                <button type="submit">Verify</button>
            </form>
    """

    # Handle certificate verification
    if certificate_no:
        student = students_data[students_data["Certificate No"] == certificate_no]

        if student.empty:
            html_content += """
            <div class="error">
                <p>Certificate not found!</p>
            </div>
            """
        else:
            student_details = {
                "Student Name": student.iloc[0]["Student Name"],
                "Domain": student.iloc[0]["Domain"],
                "Duration": student.iloc[0]["Duration"],
                "Starting Date": student.iloc[0]["Starting Date"],
                "Award Date": student.iloc[0]["Award Date"],
            }

            html_content += f"""
            <div class="result">
                <h2>Certificate Details</h2>
                <p><strong>Student Name:</strong> {student_details["Student Name"]}</p>
                <p><strong>Domain:</strong> {student_details["Domain"]}</p>
                <p><strong>Duration:</strong> {student_details["Duration"]}</p>
                <p><strong>Starting Date:</strong> {student_details["Starting Date"]}</p>
                <p><strong>Award Date:</strong> {student_details["Award Date"]}</p>
            </div>
            """

    html_content += """
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
