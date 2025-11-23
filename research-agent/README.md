# Research Agent

A conversational AI research assistant powered by Google's Gemini 2.0 Flash model and built with Pydantic AI. This agent provides clear, concise, and deeply helpful answers while maintaining conversation context.

## Features

- **Conversational Interface**: Interactive chat loop for natural conversations
- **Google Gemini Integration**: Powered by Gemini 2.0 Flash for high-quality responses
- **Logfire Monitoring**: Complete observability and tracing of agent interactions
- **Web Search Capabilities**: Built-in tools for web research (via tools.py)
- **Session Management**: Maintains conversation context until user exits

## Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Google API key for Gemini
- Logfire account for monitoring (optional)

## Installation

1. **Clone the repository and navigate to research-agent directory:**
   ```bash
   cd ai-assessment/research-agent
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install pydantic-ai google-generativeai python-dotenv logfire
   ```

4. **Set up environment variables:**
   Create a `.env` file in the research-agent directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   LOGFIRE_PROJECT_URL=your_logfire_project_url_here
   ```

## Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Your Google AI API key for Gemini model access
- `LOGFIRE_PROJECT_URL`: Your Logfire project URL for monitoring (optional)

### Model Configuration

The agent uses Google's Gemini 2.0 Flash model by default. You can modify the model in `main.py`:

```python
model = GoogleModel(model_name="gemini-2.0-flash")
```

## Usage

### Basic Usage

1. **Start the agent:**
   ```bash
   python main.py
   ```

2. **Interact with the agent:**
   ```
   Research Agent is running. Type 'exit' or 'quit' to stop.
   
   You: What is quantum computing?
   Agent: [Detailed explanation about quantum computing...]
   
   You: How does it compare to classical computing?
   Agent: [Comparison between quantum and classical computing...]
   
   You: exit
   Shutting down the agent. Goodbye!
   ```

### Available Commands

- **Regular questions**: Ask any research question
- **exit** or **quit**: Terminate the agent session

## Project Structure

```
research-agent/
├── main.py           # Main application entry point
├── tools.py          # Web search and research tools
├── README.md         # This file
├── logs/             # Log files (created automatically)
└── __pycache__/      # Python cache files
```

## Files Description

### `main.py`
- Main application entry point
- Configures the Gemini model and Pydantic AI agent
- Implements the chat loop interface
- Handles Logfire integration and monitoring
- Provides graceful shutdown on exit commands

### `tools.py`
- Contains web search tools and utilities
- Defines research capabilities for the agent
- Implements tool decorators for Pydantic AI integration

## Features in Detail

### Logfire Integration
- Automatic tracing of all agent interactions
- Performance monitoring and debugging
- Project URL displayed on startup
- Spans created for each user query

### Error Handling
- Graceful error handling for API failures
- Conversation continues even if individual queries fail
- Clear error messages displayed to users

### Session Management
- Maintains conversation context
- Memory of previous exchanges in the session
- Clean startup and shutdown process

## Monitoring and Debugging

When Logfire is configured, you can:
- View real-time agent performance
- Track conversation flows
- Debug issues with model responses
- Monitor API usage and costs

Access your Logfire dashboard using the URL displayed at startup.

## Troubleshooting

### Common Issues

1. **Import Error: 'tool' not defined**
   ```
   Solution: Ensure tools.py imports Tool (capitalized) from pydantic_ai
   ```

2. **Google API Key Error**
   ```
   Solution: Verify GOOGLE_API_KEY is set correctly in .env file
   ```

3. **Rate Limiting**
   ```
   Solution: Wait for quota to reset or upgrade your Google AI API plan
   ```

### Debug Mode

To enable verbose logging, modify the logfire configuration in `main.py`.

## API Limits

- **Free Tier**: 15 requests per minute for Gemini 2.0 Flash
- **Rate Limiting**: Automatic backoff on quota exceeded
- **Usage Monitoring**: Available through Logfire dashboard

## Contributing

1. Ensure code follows the existing structure
2. Add appropriate error handling
3. Update documentation for new features
4. Test with various question types

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Logfire logs for error details
3. Ensure all environment variables are properly set
