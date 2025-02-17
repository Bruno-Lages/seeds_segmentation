import os

import numpy as np

import cv2
from ultralytics import YOLO
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

model_path = os.getenv('MODEL_PATH')

model = YOLO(model_path)

app = Flask(__name__)

CORS(app)

def get_instances(image: np.ndarray, model: YOLO) -> list:
    """
    Runs YOLO instance segmentation on an input image.

    Parameters
    ----------
    image : np.ndarray
        Input image (BGR format from OpenCV)
    model : YOLO
        Loaded YOLOv8 segmentation model

    Returns
    -------
    List of detected instance polygons in the format:
    [[{"x": float, "y": float}, ...], ...]
    """
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = model(image_rgb)

    instance_polygons = []
    for result in results:
        if result.masks:  
            for mask in result.masks.xy:  
                instance_polygons.append(
                    [{"x": point[0], "y": point[1]} for point in mask.tolist()]
                )

    return instance_polygons


@app.route('/infer', methods=['POST'])
def infer() -> tuple:
    """
    Accepts an image file via multipart/form-data and returns instance 
    segmentation coordinates.

    Returns
    -------
    tuple
        A tuple containing the JSON response and the HTTP status code.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files['file']
    
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    if image is None:
        return jsonify({"error": "Invalid image file"}), 400

    instances = get_instances(image, model)
    
    return jsonify({"instances": instances})


def calculate_polygon_area(polygon):
    """
    Calculate the area of a polygon using the Shoelace formula.

    Parameters
    ----------
    polygon : list of dict
        List of dictionaries, each containing 'x' and 'y' keys representing
        the coordinates of the polygon vertices.

    Returns
    -------
    float
        The calculated area of the polygon. Returns 0 if the polygon has
        less than 3 vertices, which does not form a valid polygon.
    """
    if len(polygon) < 3:
        return 0

    x = np.array([point["x"] for point in polygon])
    y = np.array([point["y"] for point in polygon])

    # Use the Shoelace formula to calculate the area
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))

@app.route('/area', methods=['POST'])
def calculate_area():
    """
    Accepts a JSON with instances' coordinates and returns the total segmented area.

    The request body should contain a JSON object with a single key, 'instances', which
    is a list of objects, each containing 'x' and 'y' keys representing the
    coordinates of the polygon vertices.

    Returns
    -------
    json
        A JSON object with a single key, 'total_area', containing the total segmented
        area.

    """
    data = request.get_json()
    if not data or 'instances' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        total_area = sum(calculate_polygon_area(instance) for instance in data['instances'])
        return jsonify({"total_area": total_area})
    except Exception as e:
        return jsonify({"error": f"Failed to calculate area: {str(e)}"}), 500

if __name__ == '__main__':
    app.run()
