import argparse
from src.config import get_settings
from src.utils.logger import logger, get_logger
from src.services.comic_service import ComicService

cli_logger = get_logger("cli")


def main():
    parser = argparse.ArgumentParser(description="Comic Generation Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    generate_parser = subparsers.add_parser("generate", help="Generate a comic from text")
    generate_parser.add_argument("text", help="Input story text")
    generate_parser.add_argument("-o", "--output", help="Output file path", default=None)
    generate_parser.add_argument("-f", "--format", help="Output format (png/pdf)", default="png")

    subparsers.add_parser("version", help="Show version information")

    args = parser.parse_args()

    if args.command == "generate":
        cli_logger.info(f"Generating comic from text...")
        service = ComicService()
        result = service.generate_comic(
            text=args.text,
            output_format=args.format,
            output_path=args.output
        )
        cli_logger.info(f"Comic generated successfully: {result['output_path']}")
    elif args.command == "version":
        settings = get_settings()
        print(f"Comic Generation Agent v1.0.0")
        print(f"Backend: {settings.BACKEND_HOST}:{settings.BACKEND_PORT}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()