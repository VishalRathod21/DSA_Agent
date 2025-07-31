# 🧠 DSA Solver Pro

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

DSA Solver Pro is an intelligent platform that helps you master Data Structures and Algorithms through AI-powered problem solving. It provides step-by-step solutions, code execution in a secure Docker environment, and detailed complexity analysis using Google's Gemini AI.

## ✨ Features

- **AI-Powered Solutions**: Get detailed, step-by-step solutions to DSA problems
- **Safe Code Execution**: Run and test code in an isolated Docker container
- **Interactive Interface**: User-friendly web interface built with Streamlit
- **Code Editor**: Built-in editor for writing and testing solutions
- **Solution History**: Track and revisit your previous solutions
- **Complexity Analysis**: Understand time and space complexity of algorithms

## 🛠️ Prerequisites

- Python 3.8 or higher
- Docker (for code execution sandbox)
- Google Gemini API key (Get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/dsasolverpro.git
   cd dsasolverpro
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Start Docker**
   Make sure Docker is running on your system.

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🏗️ Project Structure

```
dsasolverpro/
├── agents/                  # AI agent implementations
│   ├── code_executor_agent.py  # Handles code execution in Docker
│   └── problem_solver.py      # Generates DSA solutions using AI
├── config/                  # Configuration files
│   ├── constant.py          # Application constants
│   ├── docker_executor.py   # Docker execution setup
│   ├── docker_utils.py      # Docker utilities
│   └── settings.py          # Application settings
├── team/                    # Team configuration
│   └── dsa_team.py          # Team setup for agents
├── app.py                   # Main Streamlit application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🤖 How It Works

1. **Problem Input**: Users enter a DSA problem or question
2. **AI Processing**: The Problem Solver Agent processes the problem using Google's Gemini AI
3. **Solution Generation**: The agent generates a step-by-step solution with code
4. **Code Execution**: The Code Executor Agent runs the code in a secure Docker container
5. **Result Display**: The solution, code, and execution results are displayed to the user

## 🛠️ Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Settings
- Model: `gemini-1.5-flash` (configurable in `config/constant.py`)
- Maximum turns: 15 (configurable in `config/constant.py`)
- Timeout: 120 seconds (configurable in `config/constant.py`)

## 📚 Usage

1. Enter your DSA problem in the text area
2. Click "Generate Solution" to get an AI-powered solution
3. Use the built-in code editor to modify and test the solution
4. View the execution results and complexity analysis
5. Save your solutions for future reference

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) for the powerful AI capabilities
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [Docker](https://www.docker.com/) for containerization
- The open-source community for various libraries and tools
