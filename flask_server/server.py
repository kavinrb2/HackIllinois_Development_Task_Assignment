from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get-combined-text', methods=['GET'])
def get_combined_text():
    try:
        # Read the content of the "task_report.txt" file
        with open("task_report.txt", "r") as file:
            combined_text = file.read()

        # Return the content of the file as the response
        return jsonify({"combinedText": combined_text})
    
    except Exception as e:
        # Return an error message if the file cannot be read
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
