import google.generativeai as genai
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure the Gemini API with your key
genai.configure(api_key="AIzaSyC2Rb7z7HTqOjmPWCN7ZmyVW3HQ1TOtPqQ")

def analyze_ocr_data(ocr_list, prompt):
    try:
        # Initialize the model - using gemini-1.5-pro for better capabilities
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # Prepare contents with prompt and OCR data
        contents = [prompt]
        for ocr in ocr_list:
            # Wrap each OCR object in a 'text' key to ensure it's treated as a text part
            contents.append({"text": str(ocr)})
        
        # Generate content with the OCR data
        response = model.generate_content(contents)
        return response.text
    except Exception as e:
        return f"Error generating content: {e}"

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    if not data or 'ocr_list' not in data or 'prompt' not in data:
        return jsonify({"error": "Missing 'ocr_list' or 'prompt' in request body"}), 400
    
    ocr_list = data['ocr_list']
    prompt = data['prompt']
    
    if not isinstance(ocr_list, list):
        return jsonify({"error": "'ocr_list' must be a list"}), 400
    
    result = analyze_ocr_data(ocr_list, prompt)
    return jsonify({"analysis": result})

if __name__ == '__main__':
    app.run(debug=True) 
