import os
from flask import Flask
from src.cli import run_cli
from src.routes import trigger
import logging
import argparse

logging.basicConfig(level=logging.INFO)

def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    server_parser = subparsers.add_parser('serve', help='Start the server')
    server_parser.add_argument('--port', type=int, default=8000)
    server_parser.add_argument('--host', type=str, default='0.0.0.0')
    

    cli_parser = subparsers.add_parser('cli', help='Configure settings')
    cli_parser.add_argument('--extracted-data-path', type=str, required=True)
    cli_parser.add_argument('--unzip-path', type=str, required=True)
    cli_parser.add_argument('--zip-path', type=str, required=True)
    
    return parser

def create_app():
    app = Flask(__name__)
    app.register_blueprint(trigger.bp)
    
    return app

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "serve":
        app = create_app()
        app.run(host=args.host, port=args.port)
    elif args.command == "cli":
        run_cli(args)