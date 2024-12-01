from src.cli import run_cli
from src.server import create_app
import logging
import argparse
import uvicorn
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)

def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    server_parser = subparsers.add_parser('serve', help='Start the server')
    server_parser.add_argument('--port', type=int, default=8080)
    server_parser.add_argument('--host', type=str, default='0.0.0.0')
    

    cli_parser = subparsers.add_parser('cli', help='Configure settings')
    cli_parser.add_argument('--extracted-data-path', type=str, required=True)
    cli_parser.add_argument('--unzip-path', type=str, required=True)
    cli_parser.add_argument('--zip-path', type=str, required=True)
    
    return parser



if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "serve":
        tqdm.disable = True
        app = create_app()
        uvicorn.run(app, host=args.host, port=args.port)
    elif args.command == "cli":
        run_cli(args)