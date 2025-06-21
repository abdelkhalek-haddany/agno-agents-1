# AI Agents Project

A collection of intelligent AI agents built with Python, featuring specialized agents for different domains including finance, books, movies, recipes, research, travel, and YouTube content.

## 🚀 Project Structure

```
TEST1AGNO/
├── agents/                          # Main agents directory
│   ├── books_recommender/           # Book recommendation agent
│   ├── finance_agent/               # Financial analysis agent
│   ├── movie_recommender/           # Movie recommendation agent
│   ├── my_first_agents/             # Beginner/test agents
│   ├── recipe_creator/              # Recipe creation agent
│   ├── research_agent/              # Research and information gathering agent
│   ├── research_agent_exa/          # Enhanced research agent
│   ├── travel_agent/                # Travel planning agent
│   └── youtube_agent/               # YouTube content agent
├── config/                          # Configuration files
│   ├── gemini_llm.py               # Google Gemini LLM configuration
│   └── logging_config.py           # Logging setup
├── utils/                           # Utility functions and helpers
├── .env                            # Environment variables
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── main.py                         # Main application entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🛠️ Setup and Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd TEST1AGNO
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_google_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🤖 Available Agents

### 📚 Books Recommender
Provides personalized book recommendations based on user preferences, reading history, and genres.

### 💰 Finance Agent
Analyzes financial data, provides market insights, stock information, and investment recommendations.

### 🎬 Movie Recommender
Suggests movies based on user preferences, genres, ratings, and viewing history.

### 🍳 Recipe Creator
Creates custom recipes based on available ingredients, dietary restrictions, and cuisine preferences.

### 🔍 Research Agent
Conducts comprehensive research on various topics, gathering and synthesizing information from multiple sources.

### ✈️ Travel Agent
Plans trips, suggests destinations, finds flights and accommodations, and provides travel recommendations.

### 📺 YouTube Agent
Analyzes YouTube content, provides video recommendations, and helps with content strategy.

## 🚀 Usage

### Running Individual Agents
Each agent can be run independently. Navigate to the specific agent directory and run:

```bash
cd agents/finance_agent
python agent.py
```

### Running the Main Application
```bash
python main.py
```

## 🔧 Configuration

### LLM Configuration
The project supports multiple LLM providers:
- **Google Gemini**: Configure in `config/gemini_llm.py`
- **OpenAI**: Set `OPENAI_API_KEY` in `.env`

### Logging
Logging configuration is managed in `config/logging_config.py`. You can adjust log levels and output formats as needed.

## 📦 Dependencies

Key dependencies include:
- `agno` - Agent framework
- `openai` - OpenAI API client
- `google-generativeai` - Google Gemini API
- `textwrap` - Text formatting utilities
- Additional agent-specific dependencies

See `requirements.txt` for the complete list.

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_GENAI_USE_VERTEXAI` | Use Vertex AI for Google services | No |
| `GOOGLE_API_KEY` | Google API key for Gemini | No |
| `OPENAI_API_KEY` | OpenAI API key | Yes* |

*At least one LLM provider API key is required.

## 🧪 Development

### Adding New Agents
1. Create a new directory under `agents/`
2. Implement your agent logic in `agent.py`
3. Add any agent-specific configuration
4. Update requirements if needed

### Code Structure
Each agent typically follows this structure:
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config.settings import Settings

# Agent configuration
agent = Agent(
    model=OpenAIChat(id="gpt-4o"),
    tools=[...],  # Agent-specific tools
    ...
)
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the project root and have installed all dependencies.

2. **API Key Errors**: Verify your API keys are correctly set in the `.env` file.

3. **Module Not Found**: Make sure you've activated your virtual environment and installed requirements.

### Getting Help
- Check the logs in the console output
- Verify your environment configuration
- Ensure all API keys are valid and have sufficient credits


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with the [Agno](https://github.com/agno-ai/agno) agent framework
- Powered by OpenAI
- Thanks to all contributors and the open-source community

---

**Note**: This is an AI agents project designed for educational and development purposes. Always ensure you comply with the terms of service of the AI providers you're using.