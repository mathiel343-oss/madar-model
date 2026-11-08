# MADAR V2 Backend

Backend prototype for MADAR predictive waste management.

## Requirements
Python 3.10 or newer.

## Installation

pip install -r requirements.txt

## Run

uvicorn main:app --host 127.0.0.1 --port 8000

Run the command from the MADAR_V2_Backend folder.

## API Documentation

http://127.0.0.1:8000/docs

## Available Endpoints

GET /
GET /api/health
GET /api/bins
GET /api/bins/{bin_id}
GET /api/map
GET /api/priorities
GET /api/simulation
GET /api/routes

## Important Notes

- Data is synthetic, not live sensor data.
- Prediction endpoints currently return saved model outputs.
- The .pkl models are included but are not yet
  used for on-demand inference by this API.
- Routes use straight-line distances, not road networks.
- CORS is open for development and must be restricted
  before production deployment.
- Hosting is required for access from an external website.
- Load model files only from trusted sources.
