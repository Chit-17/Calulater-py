from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

# Your complete HTML template as a string (embedded in Flask)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Python Flask Calculator</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        /* Custom nice-to-have font */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        body { font-family: 'JetBrains Mono', monospace; }
    </style>
</head>
<body class="bg-gray-900 text-white min-h-screen flex items-center justify-center p-4">

    <!-- Calculator Container -->
    <div class="bg-gray-800 p-6 rounded-2xl shadow-2xl w-full max-w-sm border border-gray-700">
        
        <!-- Display Screen -->
        <div class="mb-5">
            <input type="text" id="display" readonly 
                class="w-full bg-gray-900 text-right text-3xl p-4 rounded-lg focus:outline-none text-green-400 font-bold shadow-inner placeholder-gray-600" 
                placeholder="0">
        </div>

        <!-- Buttons Grid -->
        <div class="grid grid-cols-4 gap-3">
            <!-- First Row -->
            <button onclick="clearDisplay()" class="col-span-2 bg-red-500 hover:bg-red-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">AC</button>
            <button onclick="deleteChar()" class="bg-gray-600 hover:bg-gray-500 p-4 rounded-lg font-bold text-xl transition shadow-lg">DEL</button>
            <button onclick="appendChar('/')" class="bg-orange-500 hover:bg-orange-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">/</button>

            <!-- Second Row -->
            <button onclick="appendChar('7')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">7</button>
            <button onclick="appendChar('8')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">8</button>
            <button onclick="appendChar('9')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">9</button>
            <button onclick="appendChar('*')" class="bg-orange-500 hover:bg-orange-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">*</button>

            <!-- Third Row -->
            <button onclick="appendChar('4')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">4</button>
            <button onclick="appendChar('5')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">5</button>
            <button onclick="appendChar('6')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">6</button>
            <button onclick="appendChar('-')" class="bg-orange-500 hover:bg-orange-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">-</button>

            <!-- Fourth Row -->
            <button onclick="appendChar('1')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">1</button>
            <button onclick="appendChar('2')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">2</button>
            <button onclick="appendChar('3')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">3</button>
            <button onclick="appendChar('+')" class="bg-orange-500 hover:bg-orange-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">+</button>

            <!-- Fifth Row -->
            <button onclick="appendChar('0')" class="col-span-2 bg-gray-700 hover:bg-gray-600 p-4 rounded-lg text-xl transition shadow-lg">0</button>
            <button onclick="appendChar('.')" class="bg-gray-700 hover:bg-gray-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">.</button>
            <button onclick="calculateResult()" class="bg-green-500 hover:bg-green-600 p-4 rounded-lg font-bold text-xl transition shadow-lg">=</button>
        </div>
    </div>

    <script>
        const display = document.getElementById('display');

        function appendChar(char) {
            display.value += char;
        }

        function clearDisplay() {
            display.value = '';
        }

        function deleteChar() {
            display.value = display.value.toString().slice(0, -1);
        }

        async function calculateResult() {
            const expression = display.value;
            if (!expression) return;

            try {
                // Send data to Python Backend via AJAX (Fetch API)
                const response = await fetch('/calculate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ expression: expression })
                });

                const data = await response.json();
                
                if (data.result === 'Error') {
                    display.value = 'Error';
                    setTimeout(() => display.value = '', 1500);
                } else {
                    display.value = data.result;
                }

            } catch (error) {
                console.error('Error:', error);
                display.value = 'Error';
            }
        }
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    """Serve the calculator UI"""
    return render_template_string(HTML_TEMPLATE)

@app.route("/calculate", methods=["POST"])
def calculate():
    """Calculate the mathematical expression safely"""
    try:
        data = request.get_json()
        if not data or "expression" not in data:
            return jsonify({"result": "Error"}), 400

        expression = data["expression"].strip()
        
        # Only allow safe operations: numbers, ., +, -, *, /, ()
        if not re.match(r'^[0-9+\-*/().\s]+$', expression):
            return jsonify({"result": "Error"}), 400

        # Replace JS-style division with Python division
        expression = expression.replace('/', '//') if '/' in expression else expression
        
        # Safe evaluation using restricted globals
        allowed_names = {
            'abs': abs, 'max': max, 'min': min, 'round': round,
            'sum': sum
        }
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        
        # Format result nicely
        if isinstance(result, float) and result.is_integer():
            result = int(result)
            
        return jsonify({"result": str(result)})
        
    except Exception:
        return jsonify({"result": "Error"}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
