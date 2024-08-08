# Quart + Tailwind Template
.
├── assets
│   ├── css
│   │   └── styles.css - Other styles go here
        └── input.css - Base Tailwind declarations go here
│   └── LICENSE
├── docs
│   ├── LICENSE.md
│   └── PLAN.md
├── LICENSE
├── pyproject.toml
├── README.md
└── src
    ├── app.py - Base setup for app goes here
    ├── logging.py
    ├── routes - Py files for different routes go here
    └── templates - Different .html template files go here.

I want to make a basic Quart application which is a Counter application where the number can count up and down with buttons.

I want the index.py in the routes folder, and setup everything in the app.py, and use hypercorn as the ASGI server programatically run it.

We need a `base.html` in templates which is the base template and every other template like `index.html` extends it. We have the Title Configurable by the templates as well as the `body`.

We need the tailwind cli installed through npm.

this is an example, it does not work, but its a similar thing to get tailwind working:
```python
from quart import Quart, render_template
import subprocess

app = Quart(__name__)
app.debug = True

tailwind_process = None

async def start_tailwind_cli():
    global tailwind_process
    if app.debug:
        try:
            subprocess.check_output(['pgrep', '-f', './tailwindcss'])
        except subprocess.CalledProcessError:
            print('Starting Tailwind CLI...')
            tailwind_process = subprocess.Popen([
                    './tailwindcss',
                    '-i',
                    'assets/css/input.css',
                    '-o',
                    'assets/css/output.css',
                    '--watch',
                ])
            print(tailwind_process)


@app.before_serving
async def before_serving():
    await start_tailwind_cli()


@app.route('/')
async def hello():
    return await render_template('blog/index.html', title='Hello! 👋')

app.run(debug=True)
```

## Logging
We need logging throughout the app, luckily we have code already for this in the `src/logging.py`:
```python
import os
import sys
import logging
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from appdirs import user_log_dir
import coloredlogs

def setup_logging(app_name: str = "QuartTailwind") -> logging.Logger:
    load_dotenv()
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LOG_DIR = user_log_dir(app_name)
    os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, f"{app_name.lower()}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger = logging.getLogger(app_name)
    coloredlogs.install(level=LOG_LEVEL, logger=logger)

    # Add TRACE log level
    TRACE = 5
    logging.addLevelName(TRACE, "TRACE")
    setattr(logger, "trace", lambda message, *args: logger.log(TRACE, message, *args))

    return logger

# Global logger instance
logger: Optional[logging.Logger] = None

def get_logger() -> logging.Logger:
    global logger
    if logger is None:
        logger = setup_logging()
    return logger
```

Please write me the templates and the route, for the counter application, and also write me the `app.py` with hypercorn running programatically.