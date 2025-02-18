# Seed Segmentation 
This project aims to develop a web application for seed segmentation using a machine learning model. 
The application consists of a backend server that handles model inference and a frontend interface for user interaction.

The repository is organized into two main directories:

- backend: Contains the server-side code responsible for processing images and performing seed segmentation using a machine learning model.
- frontend: Contains the client-side code that provides a user-friendly interface for uploading images and viewing segmentation results.

## Backend
The backend is built with Flask and performs the seeds segmentation and area calculation.

### Setting Up the Backend
It is necessary write a `.env` in the backend folder containing the `MODEL_PATH` env, with the path for the .pt model weight.

1. Change to the backend folder
2. Execute command ```pip install -r requirements.txt```
3. Inicie o servidor com ```python3 app.py```

After this the server will start on the default port (e.g., http://localhost:5000).

## Frontend
The frontend is developed using Vue.js and provides an interface for upload seed images and view segmentation and area results.
### Setting Up the Frontend
First, is necessary create a .env in the `frontend/seeds-segmentation` folder with the VITE_API_URL env, containing the backend API url.

1. Run `npm install` to install
2. Execute command `npm run dev`

The application will be accessible at http://localhost:5173 by default.
