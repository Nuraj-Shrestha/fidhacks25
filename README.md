# HerWay - Women's Career Development Platform

HerWay is a supportive platform designed to help women in their career development journey. It provides goal setting, resource sharing, community support, and personalized guidance to help users achieve their professional aspirations.

## Features

- **Personalized Goal Setting**: Set and track up to three main career goals
- **Resource Library**: Access curated resources for networking, resume building, and job applications
- **Community Forum**: Connect with other users and share experiences
- **AI-Powered Guidance**: Get personalized steps and affirmations for your goals
- **Progress Tracking**: Monitor your achievements and milestones
- **Mood-Based Support**: Receive personalized affirmations based on your current mood

## Tech Stack

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **AI Integration**: OpenAI GPT-3.5
- **Data Storage**: JSON files for user data and resources
- **Styling**: Custom CSS with modern design principles

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd herway
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with your OpenAI API key:
```
_API_KEY=your_openai_api_key_here
SECRET_KEY=your_flask_secret_key_here
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
herway/
├── app.py              # Main Flask application
├── data/              # JSON data files
│   ├── goals.json     # User goals
│   ├── forum.json     # Forum posts
│   └── resources.json # Resource library
├── templates/         # HTML templates
│   ├── landing.html   # Landing page
│   ├── goals.html     # Goal setting page
│   ├── main.html      # Main dashboard
│   ├── forum.html     # Community forum
│   └── resources.html # Resource library
├── static/           # Static files (CSS, JS, images)
├── venv/             # Virtual environment
└── requirements.txt  # Python dependencies
```

## Features in Detail

### Goal Setting
- Set up to three main career goals
- Receive AI-generated actionable steps for each goal
- Track progress and achievements

### Resource Library
- Curated resources for career development
- Categories include networking, resume building, and applications
- Interactive expandable sections for easy navigation

### Community Forum
- Share experiences and insights
- Connect with other users
- Get support and advice

### AI Integration
- Personalized goal steps
- Mood-based affirmations
- Motivational summaries

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for providing the GPT-3.5 API
- The Flask community for their excellent documentation
- All contributors who have helped shape this project

## Contact

For any questions or suggestions, please open an issue in the repository. 