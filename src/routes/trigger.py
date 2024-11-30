from flask import Blueprint, request
import logging
from src.pipeline.config import ConfigModel
from src.pipeline.run import run_pipeline

bp = Blueprint('pipeline', __name__, url_prefix='/api')

@bp.route('/trigger', methods=['POST'])
def trigger_processing():
    # Get parameters from request body
    json_body = request.get_json()
    config = ConfigModel(**json_body)
    run_pipeline(config)
    json = config.model_dump_json()
    logging.info(json)
    return json, 200