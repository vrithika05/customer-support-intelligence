# SupportIQ — Customer Support Analytics & Ticket Intelligence

SupportIQ is a portfolio-ready customer-support analytics platform built with **Python, Flask, SQLAlchemy, Pandas, scikit-learn, HTML/CSS/JavaScript and Chart.js**.

It combines operational ticket management with analytics and lightweight NLP to help support teams understand ticket volume, customer sentiment, priority, CSAT and response performance.

## Highlights

- Secure session-based login flow for the demo application
- Ticket creation and status management
- Automatic sentiment prediction using TF-IDF + Logistic Regression
- AI-assisted priority suggestion
- KPI dashboard for ticket volume, resolution rate, CSAT and response time
- Category and sentiment visualizations
- CSV/Excel data import with validation and cleaning
- Search and status filtering
- CSV export
- REST API for KPI and sentiment prediction
- SQLite database by default
- Docker and Render deployment configuration
- Automated tests with pytest
- Sample dataset included

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite, SQLAlchemy |
| Analytics | Pandas, NumPy |
| Machine Learning | scikit-learn, TF-IDF, Logistic Regression |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Testing | pytest |
| Deployment | Gunicorn, Docker, Render |
| Version Control | Git / GitHub |

## Project Structure

```text
customer-support-intelligence/
├── app/
│   ├── services/
│   │   ├── analytics.py
│   │   └── ml.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   ├── templates/
│   ├── models.py
│   ├── routes.py
│   └── __init__.py
├── data/sample_tickets.csv
├── models/                 # generated ML model is stored here locally
├── tests/test_app.py
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── Procfile
├── render.yaml
├── requirements.txt
├── run.py
└── README.md
```

## Run Locally — Windows

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/customer-support-intelligence.git
cd customer-support-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

```bash
copy .env.example .env
```

For production, replace the demo secret with a long random value.

### 5. Start the application

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

### Demo credentials

```text
Email: admin@example.com
Password: admin123
```

## Run Tests

```bash
pytest -q
```

## API Examples

### KPI API

```http
GET /api/kpis
```

Example response:

```json
{
  "total": 8,
  "resolved": 4,
  "resolution_rate": 50.0,
  "avg_csat": 2.38,
  "avg_response": 3.2
}
```

### Sentiment Prediction

```http
POST /api/predict
Content-Type: application/json

{
  "text": "I am very frustrated because the issue is still not fixed"
}
```

Example response:

```json
{
  "sentiment": "Negative",
  "suggested_priority": "High"
}
```

## Data Import

The importer accepts `.csv` and `.xlsx` files.

Required columns:

```text
customer_name
customer_email
subject
description
category
sentiment
priority
status
csat
response_time_hours
resolution_time_hours
```

A ready-to-use dataset is available at `data/sample_tickets.csv`.

## Docker

Build and run:

```bash
docker compose up --build
```

Then open:

```text
http://localhost:5000
```

## Deploy on Render

1. Push this repository to GitHub.
2. Create a new Web Service on Render.
3. Connect the GitHub repository.
4. Use:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn run:app`
5. Add a `SECRET_KEY` environment variable.
6. Deploy.

> Note: SQLite is excellent for this portfolio/demo deployment, but a production multi-instance application should use a managed PostgreSQL database and persistent storage.

## Machine Learning Approach

The project uses a simple, explainable text-classification pipeline:

1. Convert ticket descriptions into TF-IDF features.
2. Use unigrams and bigrams to capture short phrases.
3. Train Logistic Regression for three-class sentiment classification.
4. Save the fitted pipeline with joblib.
5. Load the model when the application starts and use it for new ticket predictions.

The bundled training set is intentionally small so the project remains self-contained. For a production system, replace it with a larger labeled customer-support dataset and evaluate precision, recall, F1-score and confusion matrix before deployment.

## Interview Explanation

**Problem:** Support teams receive many tickets and need to quickly identify urgent or negative customer issues.

**Solution:** SupportIQ combines ticket management, operational analytics and NLP-based sentiment prediction in one web application.

**Why TF-IDF?** It converts text into numerical features while keeping the model lightweight and interpretable.

**Why Logistic Regression?** It is fast, strong for sparse text features and easy to evaluate and explain.

**How is priority suggested?** Negative sentiment is mapped to High, Neutral to Medium and Positive to Low as a transparent demo rule. This can later be replaced with a trained priority model.

## Future Enhancements

- PostgreSQL for production persistence
- Role-based admin/agent/customer accounts
- Email notifications
- SLA breach prediction
- Advanced priority prediction model
- Transformer-based sentiment analysis
- Agent performance analytics
- Monthly trend forecasting
- Power BI integration
- CI/CD with GitHub Actions

## Resume Description

**AI-Powered Customer Support Analytics & Ticket Intelligence Platform** — Python, Flask, NLP, scikit-learn, Pandas, SQL, JavaScript, Chart.js, Docker

- Developed a Flask-based customer-support platform to manage tickets and analyze support performance using operational and customer-satisfaction data.
- Implemented TF-IDF and Logistic Regression for NLP-based sentiment classification and automated priority recommendations.
- Built interactive KPI dashboards for ticket volume, resolution rate, CSAT and response-time analysis using Chart.js.
- Added validated CSV/Excel ingestion, search/filter workflows, REST APIs and CSV reporting to support data-driven ticket operations.
- Containerized the application with Docker and added Gunicorn/Render deployment configuration and pytest-based automated tests.

## License

MIT License.
