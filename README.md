# LogAi

Final project of Data Engineering with AI from XP Educação.

---

## 📖 About the Project

**LogAi** is an application that leverages artificial intelligence to analyze logs, detect anomalies, and generate detailed reports. It processes large volumes of logs, extracts relevant features, and uses machine learning models to identify anomalous patterns.

---

## 🛠️ Setting Up the Environment

### 1. Install Dependencies

Make sure you have [Poetry](https://python-poetry.org/) installed. Then, run the following command:

```bash
poetry install
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following content:

```bash
OPENAI_API_KEY=your_openai_api_key
```

> **Note**: Replace `your_openai_api_key` with your OpenAI API key.

---

## 🚀 How to Run

### 1. Process and Analyze Logs

To process logs and generate anomaly reports, run:

```bash
poetry run python src/main.py
```

### 2. Generate Simulated Logs

If you need to generate a log file for testing, run:

```bash
poetry run python src/log_generator.py
```

---

## 📂 Project Structure

Below is the main structure of the project:

```
LogAi/
├── data/
│   ├── app.log                 # Input log file
│   └── output/
│       ├── anomalies.csv       # Logs classified as anomalies
│       └── processed_logs.csv  # Processed logs with extracted features
├── export/
│   └── analysis.md             # Detailed anomaly analysis report
├── src/
│   ├── main.py                 # Main script for log processing and analysis
│   └── log_generator.py        # Script for generating simulated logs
├── .env_example                # Example environment configuration
├── pyproject.toml              # Project configuration and dependencies
├── README.md                   # Project documentation
└── .gitignore                  # Ignored files in the repository
```

---

## 📊 Reports and Results

### Anomaly Analysis Report

The anomaly analysis report is available in the file [`export/analysis.md`](export/analysis.md). It includes:

- **Log Type Distribution**:
  - WARN: 26,226
  - INFO: 12,132
  - ERROR: 7,440
  - DEBUG: 4,080
- **Identified Patterns**:
  - Slow queries (`slow_query`) account for **68%** of anomalies.
  - Most anomalies occur between **12 AM - 3 AM** and **9 PM - 11 PM**.
- **Hypotheses**:
  - Slow queries may trigger other performance issues.
  - Database failures are directly linked to critical events.

---

## 🧰 Tools and Technologies

- **Language**: Python 3.10+
- **Libraries**:
  - `openai`: Integration with OpenAI API.
  - `python-dotenv`: Environment variable management.
  - `pandas`: Data manipulation and analysis.
  - `numpy`: Mathematical and numerical operations.
  - `matplotlib` and `seaborn`: Data visualization.
  - `scikit-learn`: Machine learning modeling (Isolation Forest).

---

## 📝 License

This project is for educational purposes only and does not have a specific license.

---

## 📧 Contact

Created by **Arthur Gonzaga**  
📧 Email: [arthursgonzaga@gmail.com](mailto:arthursgonzaga@gmail.com)