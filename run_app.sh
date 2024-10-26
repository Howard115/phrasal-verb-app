#!/bin/bash

# Start the backend
cd backend
uvicorn main:app --reload &

# Start the frontend (assuming it's a React app)
cd ../frontend
streamlit run app.py 

# Wait for both processes
wait
