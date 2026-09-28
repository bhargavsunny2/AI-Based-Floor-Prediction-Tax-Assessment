# AI-Based Floor Prediction and Tax Assessment System

## Project Overview

The AI-Based Floor Prediction and Tax Assessment System is a Python-based machine learning application designed to predict the authorized number of floors for a building and estimate property tax based on property and location details.

The system uses Machine Learning for floor prediction and a rule-based calculation for property tax estimation. A Tkinter graphical user interface is provided for easy interaction, while SQLite is used to store assessment records.

---

## Objectives

The main objectives of this project are:

- Predict the number of floors using Machine Learning.
- Estimate property tax automatically.
- Provide a simple desktop-based graphical interface.
- Store property assessment records securely.
- Provide assessment history.
- Reduce manual property assessment work.
- Demonstrate the practical use of Artificial Intelligence and Machine Learning.

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Tkinter
- SQLite
- Machine Learning
- HTML/Markdown documentation

---

## Machine Learning

A Random Forest Classification model is used to predict the number of floors.

### Input Features

The model uses the following features:

1. Plot Area
2. Building Height
3. Road Width
4. Location Score

### Output

The model predicts:

- Number of Floors

---

## Property Tax Assessment

After predicting the number of floors, the system estimates property tax using:

- Plot area
- Predicted floors
- Location score

The tax calculation is performed automatically after the floor prediction.

---

## System Workflow

```text
User enters property details
            |
            v
     Input Validation
            |
            v
    Machine Learning Model
            |
            v
     Floor Prediction
            |
            v
      Tax Calculation
            |
            v
       Save Record
            |
            v
      Display Results