# Python Flask Calculator

A modern, responsive calculator built with Flask backend and Tailwind CSS frontend. Features a sleek dark theme with JetBrains Mono font, secure expression evaluation, and smooth animations.

![Calculator Screenshot](screenshot.png)
*(Add a screenshot of your calculator here)*

## ✨ Features

- **Full Calculator Functionality**: Supports +, -, *, /, parentheses, decimals
- **Modern UI**: Tailwind CSS with dark theme and hover animations
- **Secure Evaluation**: Regex validation + restricted `eval()` for safety
- **Responsive Design**: Works perfectly on desktop and mobile
- **Real-time Display**: Live input display with AC/DEL buttons
- **Error Handling**: Graceful error display with auto-clear
- **Integer Optimization**: Converts float results to integers when possible

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Font**: JetBrains Mono (monospace perfection)
- **Deployment**: Single file - no external dependencies beyond Flask

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Flask (`pip install flask`)

### Installation
```bash
# Clone or save the code as app.py
git clone <your-repo>  # or just save the single file
cd flask-calculator

# Install dependencies
pip install flask

# Run the app
python app.py
