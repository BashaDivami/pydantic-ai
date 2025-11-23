
# E-Commerce Chat Assistant

A beautiful, animated, and modern e-commerce chatbot UI built with Starlette and Python. This project features:

- Glassmorphism and gradient UI
- Animated chat bubbles and cart (with @keyframes pop animation)
- Typing indicator for the bot
- In-memory cart and chat state
- Emoji and pricing helpers
- Responsive and mobile-friendly design
- Public logo image URL (edit `LOGO_1` in `starlette_ui.py` to change the logo)

## Features
- Add, remove, and update items in the cart via chat
- Animated, modern UI with smooth transitions
- Real-time cart updates
- Logfire integration for logging

## Getting Started

### Prerequisites
- Python 3.8+
- [pip](https://pip.pypa.io/en/stable/)

### Installation
1. Clone the repository or copy the project files.
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App
```bash
python3 starlette_ui.py
```
The app will start on `http://localhost:8020`.

## Project Structure
- `starlette_ui.py` - Main Starlette app with all UI and logic
- `requirements.txt` - Python dependencies

## Customization
- Edit `starlette_ui.py` to change UI, logic, or add new features
- To change the logo, update the `LOGO_1` variable to any public image URL
- To change chat bubble animation, edit the `@keyframes pop` rule in the `<style>` block

