import os
import sys
import subprocess
from quart import Quart
from hypercorn.config import Config
from hypercorn.asyncio import serve

from src.routes.index import index_bp
from src.log_setup import get_logger

# Get the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Configure the app with the custom static folder
app = Quart(__name__, static_folder=os.path.join(project_root, 'assets'))
app.register_blueprint(index_bp)

logger = get_logger()

def compile_tailwind_css():
    """Compile Tailwind CSS synchronously."""
    input_css = os.path.join(project_root, 'assets', 'css', 'input.css')
    output_css = os.path.join(project_root, 'assets', 'css', 'output.css')
    
    logger.info(f"Compiling Tailwind CSS...")
    logger.info(f"Input CSS: {input_css}")
    logger.info(f"Output CSS: {output_css}")
    
    try:
        result = subprocess.run(
            ['npx', 'tailwindcss', '-i', input_css, '-o', output_css],
            check=True,
            cwd=project_root,
            capture_output=True,
            text=True
        )
        logger.info("Tailwind CSS compiled successfully.")
        logger.debug(f"Tailwind output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to compile Tailwind CSS: {e}")
        logger.error(f"Tailwind stderr: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred while compiling Tailwind CSS: {str(e)}")
        sys.exit(1)

async def run_app():
    """Run the Quart application using Hypercorn."""
    config = Config()
    config.bind = ["localhost:8000"]
    await serve(app, config)

if __name__ == "__main__":
    app.debug = True
    compile_tailwind_css()  # Compile Tailwind CSS before starting the app
    import asyncio
    asyncio.run(run_app())