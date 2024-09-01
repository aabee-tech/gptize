import argparse
import os
import logging
from .gptizer import GPTizer
from .settings import Settings


def parse_arguments():
    default_output = Settings.default_output_file()
    parser = argparse.ArgumentParser(
        description="Gptize is a tool designed to concatenate the contents of project files into a single text file. It's specifically tailored for creating datasets that can be uploaded into ChatGPT for analysis or training.")
    parser.add_argument("target", nargs='?', type=str, default=os.getcwd(),
                        help="Target file or directory to process (default: current directory)")
    parser.add_argument("-o", "--output", type=str, default=default_output,
                        help=f"Output file path (default: {default_output})")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug logging (saves to gptize.log in the current directory)")
    return parser.parse_args()


def setup_logging(debug: bool):
    log_level = logging.DEBUG if debug else logging.INFO
    log_format = '%(asctime)s [%(levelname)s]: %(message)s'
    logging.basicConfig(level=log_level, format=log_format)
    if debug:
        logging.getLogger().addHandler(logging.FileHandler('gptize.log'))


def main():
    args = parse_arguments()
    setup_logging(args.debug)

    output_file_name = Settings.custom_output_file(
        args.target)
    if args.output == Settings.default_output_file():
        args.output = output_file_name

    try:
        gptizer = GPTizer()
        if os.path.isdir(args.target):
            gptizer.process_directory(args.target)
        elif os.path.isfile(args.target):
            gptizer.process_file(args.target)
        else:
            raise ValueError(f"Invalid target: {args.target}")

        combined_content = gptizer.combine_files()
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(combined_content)
            logging.info(f"Files were combined into {args.output}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
