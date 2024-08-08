from quart import Blueprint, render_template, redirect, url_for
from src.log_setup import get_logger

index_bp = Blueprint('index', __name__)
logger = get_logger()

counter = 0

@index_bp.route('/')
async def index():
    """Render the main page with the current counter value."""
    logger.info("Rendering index page")
    return await render_template('index.html', title='Counter App', counter=counter)

@index_bp.route('/increment', methods=['POST'])
async def increment():
    """Increment the counter and redirect to the index page."""
    global counter
    counter += 1
    logger.debug(f"Counter incremented to {counter}")
    return redirect(url_for('index.index'))

@index_bp.route('/decrement', methods=['POST'])
async def decrement():
    """Decrement the counter and redirect to the index page."""
    global counter
    counter -= 1
    logger.debug(f"Counter decremented to {counter}")
    return redirect(url_for('index.index'))