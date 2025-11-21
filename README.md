# I Ching Web Application

A modern web application for consulting the I Ching (易經), the ancient Chinese Book of Changes. This Flask-based application combines traditional hexagram casting with AI-powered interpretations using Google's Gemini AI.

## Features

- **Traditional Hexagram Casting**: Authentic coin-toss method for generating hexagrams
- **AI-Powered Interpretations**: Personalized readings using Google Gemini AI
- **User Authentication**: Secure registration and login system
- **Consultation History**: Track and organize your readings by subject
- **Personal Notes**: Add reflections and notes to your consultations
- **Multilingual Support**: Get interpretations in your preferred language
- **Contextual Questions**: Provide situation details and personal assessments for deeper insights

## Technologies Used

- **Backend**: Python 3, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms validation
- **AI Integration**: Google Generative AI (Gemini)
- **Markdown Rendering**: Python-Markdown for formatted interpretations

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/adantra/iching-app.git
   cd iching-app
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```
   FLASK_SECRET_KEY=your-secret-key-here
   GEMINI_API_KEY=your-gemini-api-key-here
   ```
   
   > **Note**: Never commit your `.env` file to version control!

5. **Initialize the database**
   
   The database will be created automatically when you first run the application.

## Usage

1. **Start the development server**
   ```bash
   python app.py
   ```
   
   The application will be available at `http://localhost:5000`

2. **Create an account**
   - Navigate to the registration page
   - Create a username and password

3. **Consult the I Ching**
   - Enter your question
   - Optionally provide:
     - Subject category (for organizing readings)
     - Situation description
     - Personal assessment
   - Choose your preferred language for interpretation
   - Cast the hexagram and receive your AI-powered interpretation

4. **Review past consultations**
   - Access your consultation history organized by subject
   - Add personal notes and reflections to any reading

## Project Structure

```
iching-app/
├── app.py                 # Main Flask application
├── iching.py             # I Ching hexagram logic and data
├── llm_service.py        # Gemini AI integration
├── models.py             # Database models (User, Consultation)
├── forms.py              # WTForms definitions
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── .gitignore           # Git ignore rules
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── result.html
│   └── history.html
├── static/              # Static assets (CSS, JS)
└── instance/            # SQLite database (auto-generated)
```

## Database Schema

### User
- `id`: Primary key
- `username`: Unique username
- `email`: User email
- `password_hash`: Hashed password

### Consultation
- `id`: Primary key
- `user_id`: Foreign key to User
- `timestamp`: Reading timestamp
- `question`: User's question
- `subject`: Optional category
- `situation`: Optional context
- `assessment`: Optional personal assessment
- `hexagram_data`: JSON data of the cast
- `interpretation`: AI-generated interpretation
- `notes`: User's personal notes

## API Key Setup

To use the AI interpretation features, you need a Google Gemini API key:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- The I Ching hexagram data and traditional interpretations
- Google Gemini AI for powering the interpretations
- The Flask community for excellent documentation and tools

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/adantra/iching-app/issues) on GitHub.
