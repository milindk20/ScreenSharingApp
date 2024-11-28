from flask import Flask, Response, render_template_string
import pyautogui
import io
from PIL import Image

app = Flask(__name__)

# HTML template to render the video feed
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Screen Sharing</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #2c3e50;
            margin: 0;
            height: 100vh;
        }
        img {
            max-width: 100%;
            max-height: 100%;
            border: 5px solid #ecf0f1;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        }
    </style>
</head>
<body>
    <img src="{{ url_for('video_feed') }}" alt="Screen Sharing Feed">
</body>
</html>
"""

@app.route('/')
def index():
    """Render the HTML page."""
    return render_template_string(HTML_TEMPLATE)

def capture_screen():
    """Continuously capture the screen and yield as a JPEG image."""
    while True:
        # Capture the screen using pyautogui
        screenshot = pyautogui.screenshot()
        
        # Convert to JPEG
        buffer = io.BytesIO()
        screenshot.save(buffer, format='JPEG')
        buffer.seek(0)

        # Create a streaming response
        frame = buffer.read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route."""
    return Response(capture_screen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
