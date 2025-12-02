# Computer Use Preview

## Quick Start

This section will guide you through setting up and running the Computer Use Preview model, either the Gemini Developer API or Vertex AI. Follow these steps to get started.

### 1. Installation

**Clone the Repository**

```bash
git clone https://github.com/google/computer-use-preview.git
cd computer-use-preview
```

**Set up Python Virtual Environment and Install Dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Install Playwright and Browser Dependencies**

```bash
# Install system dependencies required by Playwright for Chrome
playwright install-deps chrome

# Install the Chrome browser for Playwright
playwright install chrome
```

### 2. Configuration
You can get started using either the Gemini Developer API or Vertex AI.

#### A. If using the Gemini Developer API:

You need a Gemini API key to use the agent:

```bash
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
```

Or to add this to your virtual environment:

```bash
echo 'export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"' >> .venv/bin/activate
# After editing, you'll need to deactivate and reactivate your virtual
# environment if it's already active:
deactivate
source .venv/bin/activate
```

Replace `YOUR_GEMINI_API_KEY` with your actual key.

#### B. If using the Vertex AI Client:

You need to explicitly use Vertex AI, then provide project and location to use the agent:

```bash
export USE_VERTEXAI=true
export VERTEXAI_PROJECT="YOUR_PROJECT_ID"
export VERTEXAI_LOCATION="YOUR_LOCATION"
```

Or to add this to your virtual environment:

```bash
echo 'export USE_VERTEXAI=true' >> .venv/bin/activate
echo 'export VERTEXAI_PROJECT="your-project-id"' >> .venv/bin/activate
echo 'export VERTEXAI_LOCATION="your-location"' >> .venv/bin/activate
# After editing, you'll need to deactivate and reactivate your virtual
# environment if it's already active:
deactivate
source .venv/bin/activate
```

Replace `YOUR_PROJECT_ID` and `YOUR_LOCATION` with your actual project and location.

### 3. Running the Tool

The primary way to use the tool is via the `main.py` script.

**General Command Structure:**

You can provide the query in multiple ways:

1. **As a positional argument (string):**
```bash
python main.py "Go to Google and type 'Hello World' into the search bar"
```

2. **As a positional argument (file):**
```bash
python main.py sample-query.md
```

3. **Using the --query flag (string):**
```bash
python main.py --query "Go to Google and type 'Hello World' into the search bar"
```

4. **Using the --query flag (file):**
```bash
python main.py --query sample-query.md
```

The query can be provided as a string directly or as a path to a text file (`.txt`, `.md`, or any extension). If a file path is detected, the contents of the file will be read and used as the query.

**Available Environments:**

You can specify a particular environment with the ```--env <environment>``` flag.  Available options:

- `playwright`: Runs the browser locally using Playwright.
- `browserbase`: Connects to a Browserbase instance.

**Local Playwright**

Runs the agent using a Chrome browser instance controlled locally by Playwright.

```bash
python main.py "Go to Google and type 'Hello World' into the search bar" --env="playwright"
```

Or using the --query flag:

```bash
python main.py --query="Go to Google and type 'Hello World' into the search bar" --env="playwright"
```

You can also specify an initial URL for the Playwright environment:

```bash
python main.py "Go to Google and type 'Hello World' into the search bar" --env="playwright" --initial_url="https://www.google.com/search?q=latest+AI+news"
```

**Browserbase**

Runs the agent using Browserbase as the browser backend. Ensure the proper Browserbase environment variables are set:`BROWSERBASE_API_KEY` and `BROWSERBASE_PROJECT_ID`.

```bash
python main.py "Go to Google and type 'Hello World' into the search bar" --env="browserbase"
```

Or using the --query flag:

```bash
python main.py --query="Go to Google and type 'Hello World' into the search bar" --env="browserbase"
```

**Saving Screenshots**

To save screenshots locally for debugging or documentation purposes, use the `--save_screenshots` flag. Screenshots will be saved in a `screenshots/` directory, with each session creating a timestamped subdirectory:

```bash
python main.py "Go to Google and search for Python" --save_screenshots
```

Or using the --query flag:

```bash
python main.py --query="Go to Google and search for Python" --save_screenshots
```

Screenshots are saved with descriptive filenames including the action name, timestamp, and URL, making it easy to review the agent's behavior step by step.

**Mobile Device Emulation**

To simulate a mobile device environment (mobile resolution and behavior), use the `--mobile` flag. This enables mobile device emulation with a mobile viewport size (390x844), touch events, and a mobile user agent:

```bash
python main.py "Go to Google and search for mobile apps" --mobile
```

Or using the --query flag:

```bash
python main.py --query="Go to Google and search for mobile apps" --mobile
```

You can combine the `--mobile` flag with other options:

```bash
python main.py "Test mobile website" --mobile --env="playwright" --save_screenshots
```

## Agent CLI

The `main.py` script is the command-line interface (CLI) for running the browser agent.

### Command-Line Arguments

| Argument | Description | Required | Default | Supported Environment(s) |
|-|-|-|-|-|
| `query` (positional) | The natural language query for the browser agent to execute. Can be a string or a file path. | Yes* | N/A | All |
| `--query` | The natural language query for the browser agent to execute. Can be a string or a file path. Alternative to positional argument. | Yes* | N/A | All |

\* Either the positional `query` argument or the `--query` flag must be provided. If a file path is provided, the file contents will be read and used as the query.
| `--env` | The computer use environment to use. Must be one of the following: `playwright`, or `browserbase` | No | N/A | All |
| `--initial_url` | The initial URL to load when the browser starts. | No | https://www.google.com | All |
| `--highlight_mouse` | If specified, the agent will attempt to highlight the mouse cursor's position in the screenshots. This is useful for visual debugging. | No | False (not highlighted) | `playwright` |
| `--save_screenshots` | If specified, screenshots will be saved locally to a `screenshots` directory. Each session creates a timestamped subdirectory containing all screenshots from that run. | No | False (not saved) | All |
| `--mobile` | If specified, enables mobile device emulation with mobile screen resolution (390x844), touch events, and mobile user agent. | No | False (desktop mode) | All |

### Environment Variables

| Variable | Description | Required |
|-|-|-|
| GEMINI_API_KEY | Your API key for the Gemini model. | Yes |
| BROWSERBASE_API_KEY | Your API key for Browserbase. | Yes (when using the browserbase environment) |
| BROWSERBASE_PROJECT_ID | Your Project ID for Browserbase. | Yes (when using the browserbase environment) |

## Known Issues

### Playwright Dropdown Menu

On certain operating systems, the Playwright browser is unable to capture `<select>` elements because they are rendered by the operating system. As a result, the agent is unable to send the correct screenshot to the model.

There are several ways to mitigate this.

1. Use the Browserbase option instead of Playwright.
2. Inject a script like [proxy-select](https://github.com/amitamb/proxy-select) to render a custom `<select>` element. You must inject `proxy-select.css` and `proxy-select.js` into each page that has a non-custom `<select>` element. You can do this in the [`Playwright.__enter__`](https://github.com/google-gemini/computer-use-preview/blob/main/computers/playwright/playwright.py#L100) method by adding a few lines of code, like the following (replacing `PROXY_SELECT_JS` and `PROXY_SELECT_CSS` with the appropriate variables):

```python
self._page.add_init_script(PROXY_SELECT_JS)
def inject_style(page):
    try:
        page.add_style_tag(content=PROXY_SELECT_CSS)
    except Exception as e:
        print(f"Error injecting style: {e}")

self._page.on('domcontentloaded', inject_style)
```

Note, option 2 does not work 100% of the time, but is a temporary workaround for certain websites. The better option is to use Browserbase.
