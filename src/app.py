import os
import sys
import subprocess
import asyncio
from quart import Quart
from watchfiles import awatch

from src.routes.index import index_bp
from src.log_setup import get_logger

# Get the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

logger = get_logger()

def create_app():
    """Create and configure the Quart application."""
    app = Quart(__name__, static_folder=os.path.join(project_root, 'assets'))
    app.register_blueprint(index_bp)
    return app

async def compile_tailwind_css():
    """Compile Tailwind CSS asynchronously."""
    input_css = os.path.join(project_root, 'assets', 'css', 'input.css')
    output_css = os.path.join(project_root, 'assets', 'css', 'output.css')
    
    logger.info(f"Compiling Tailwind CSS...")
    logger.info(f"Input CSS: {input_css}")
    logger.info(f"Output CSS: {output_css}")
    
    try:
        process = await asyncio.create_subprocess_exec(
            'npx', 'tailwindcss', 
            '-i', input_css, 
            '-o', output_css,
            cwd=project_root,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            logger.info("Tailwind CSS compiled successfully.")
            logger.debug(f"Tailwind output: {stdout.decode()}")
        else:
            logger.error(f"Failed to compile Tailwind CSS: {stderr.decode()}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while compiling Tailwind CSS: {str(e)}")

app = create_app()

async def watch_files():
    """Watch for file changes and trigger appropriate actions."""
    dirs_to_watch = [
        os.path.join(project_root, 'src'),
        os.path.join(project_root, 'assets', 'css'),
        os.path.join(project_root, 'assets', 'js'),
    ]
    files_to_watch = [
        os.path.join(project_root, 'tailwind.config.js'),
    ]
    
    async for changes in awatch(*dirs_to_watch, *files_to_watch):
        for change in changes:
            _, file_path = change
            relative_path = os.path.relpath(file_path, project_root)
            
            if relative_path.startswith('src'):
                logger.info(f"Python file changed: {relative_path}")
                # Quart's debug mode will handle reloading for Python files
            elif relative_path.startswith('assets/css') and not relative_path.endswith('output.css'):
                logger.info(f"CSS file changed: {relative_path}")
                await compile_tailwind_css()
            elif relative_path.startswith('assets/js'):
                logger.info(f"JS file changed: {relative_path}")
                # Add any specific actions for JS file changes if needed
            elif relative_path == 'tailwind.config.js':
                logger.info(f"Tailwind config changed: {relative_path}")
                await compile_tailwind_css()

@app.before_serving
async def startup():
    """Run tasks before serving the app."""
    # Start Tailwind compilation in the background
    asyncio.create_task(compile_tailwind_css())
    # Start file watching
    asyncio.create_task(watch_files())

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True, host="localhost", port=8000)