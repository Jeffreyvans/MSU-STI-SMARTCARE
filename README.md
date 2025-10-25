🧠 MSU-STI SmartCare — AI-Powered STI Prediction and Consultation System

MSU-STI SmartCare is an intelligent, web-based health application designed to assist university students in Zimbabwe with confidential, accessible, and data-driven screening for sexually transmitted infections (STIs).

💡 Overview

Rising STI rates among university students are often linked to stigma, limited health resources, and fear of exposure, causing many to delay seeking help. This project addresses these challenges by combining machine learning and digital health to provide an anonymous and secure STI prediction and consultation platform.

⚙️ Key Features

🤖 STI Prediction Model — Uses Logistic Regression for accurate and interpretable predictions based on self-reported symptoms.

🔐 Confidential Consultations — Enables secure, anonymous interaction between students and healthcare professionals.

🧑‍⚕️ Role-Based Access — Custom dashboards for students, doctors, and administrators.

💬 Multi-Language Support — Designed to support English and Shona (local language integration in progress).

🧱 Data Privacy & Security — Encrypted data storage and compliance with national data protection laws.

🧩 Technical Stack

Backend: Django (Python)

Frontend: HTML, CSS, JavaScript, Bootstrap

Model Training: Python (Jupyter Notebook, Pandas, Scikit-learn)

Database: SQLite

Machine Learning: Logistic Regression (selected for accuracy, interpretability, and efficiency)

📊 Dataset

The dataset consists of open-source, synthetic, and mock student data due to ethical and regulatory restrictions on real medical datasets. All data were cleaned, encoded, and normalized before training.

🔍 Results

Achieved high prediction accuracy with minimal false alarms.

Demonstrated effective early STI detection and symptom-based analysis.

Showed potential to support university healthcare systems with AI-assisted insights.

🔒 Ethics & Compliance

Fully anonymized user inputs.

Aligned with Zimbabwe’s Data Protection Act and ethical research standards.

Future versions aim for clinical validation and expanded mobile integration.

🚀 Future Improvements

Incorporate verified clinical datasets.

Develop mobile app compatibility.

Expand multilingual functionality (e.g., full Shona translation).

Integrate with national health information systems (HIS).

🎓 Impact

This project aligns with Zimbabwe’s Education 5.0 vision, promoting innovation in local healthcare through ethical AI. It serves as both a working prototype and a research demonstration of how data science can improve early STI diagnosis and empower student health management.
### General Disease Prediction based on symptoms provided by patient- powered by Django & Machine Learning


# How To Use This
First make sure PostgreSQL and pgadmin is install in your system. 
then you have to manually create a DB instance on PostgreSQL named "predico", better use PgAdmin for that.
make a new environment(recommended) and run...

- Run pip install -r requirements.txt to install dependencies
- Run python manage.py makemigrations
- Run python manage.py migrate
- Run python manage.py runserver
- Navigate to http://127.0.0.1:8000/ in your browser

### Dataset used - 
https://www.kaggle.com/neelima98/disease-prediction-using-machine-learning

