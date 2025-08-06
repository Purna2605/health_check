# Health Check App

A comprehensive web application for health monitoring and assessment built with Flask and HTML/JavaScript.

## Features

- **Personal Info & BMI Calculator**: Calculate BMI based on height and weight
- **Symptom Analysis**: Select symptoms and get AI-powered diagnosis and risk assessment
- **Mental Wellness Tracker**: Monitor mood and sleep patterns
- **General Health Check-Up**: Track vital signs like blood pressure, sugar levels, and heart rate
- **PDF Report Generation**: Download comprehensive health reports
- **Hospital Locator**: Find nearby hospitals based on location
- **Medicine Reminders**: Set time-based medication reminders

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd health-check-app
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python3 app.py
# or use the startup script
python3 run.py
```

4. Open your browser and navigate to `http://localhost:5000`

5. (Optional) Test the API endpoints:
```bash
# Install requests for testing
pip install --break-system-packages requests
# Run the test script
python3 test_app.py
```

## Project Structure

```
health-check-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── logic/                # Backend logic modules
│   ├── __init__.py
│   ├── risk_classifier.py    # Risk assessment logic
│   ├── pdf_generator.py      # PDF report generation
│   └── hospital_finder.py    # Hospital location services
├── templates/            # HTML templates
│   └── index.html       # Main application interface
└── static/              # Static files (CSS, JS, images)
```

## API Endpoints

### Health Assessment
- `POST /bmi` - Calculate BMI
- `POST /diagnose` - Symptom diagnosis
- `POST /classify-risk` - Risk classification

### Reports & Services
- `POST /generate-report` - Generate PDF health report
- `POST /find-hospitals` - Find nearby hospitals
- `POST /set_reminder` - Set medicine reminders
- `GET /get_reminders` - Get due reminders

### Chat & Support
- `POST /chat` - Health chatbot interaction

## Usage

1. **Fill Personal Information**: Enter your name, age, height, and weight to calculate BMI
2. **Select Symptoms**: Choose from 26 different symptoms for analysis
3. **Mental Wellness**: Track your mood and sleep duration
4. **Health Check-up**: Enter vital signs for assessment
5. **Generate Report**: Download a PDF report with all your health data
6. **Find Hospitals**: Locate nearby medical facilities
7. **Set Reminders**: Create medication reminders

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **PDF Generation**: fpdf2
- **Scheduling**: APScheduler
- **Cross-Origin Requests**: Flask-CORS

## Features in Detail

### Risk Classification
The app uses an intelligent risk classifier that categorizes health risks as:
- **Low**: Minimal symptoms or common conditions
- **Medium**: Multiple symptoms or concerning patterns
- **High**: Serious symptoms requiring immediate medical attention

### Medicine Reminders
Set up automated reminders for medications with:
- Custom medicine names
- Specific times
- Background scheduling system

### Hospital Locator
Integration with Google Maps to find:
- Hospitals near your location
- Emergency services
- Medical facilities

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Disclaimer

This application is for educational and informational purposes only. It is not intended to replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support, please open an issue in the GitHub repository or contact the development team.