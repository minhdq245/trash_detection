# Trash Detection Web Application

## Overview

Real-time waste detection web application using YOLOv8 and Flask. The application can detect and classify 6 types of waste:

- Bottle
- Paper
- Cardboard
- Detergent
- Can/Canister
- Glass

## Project Structure

```
detect-rac-web
├── src
│   ├── app.py
│   ├── model
│   │   └── yolo.py
│   ├── static
│   │   └── js
│   │       └── camera.js
│   └── templates
│       └── index.html
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository:

```bash
git clone https://github.com/minhdq245/trash_detection.git
cd trash_detection
```

2. Create and activate virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python src/app.py
```

5. Open browser and navigate to `http://localhost:5000` to access the application.

## Usage

- Allow the application to access your camera when prompted.
- The application will start streaming video from your camera and detect waste in real-time.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
