import argparse
import os
import logging
from .gptizer import GPTizer
from .settings import Settings


def parse_arguments():
    default_output = Settings.default_output_file()
    parser = argparse.ArgumentParser(
        )
    parser.add_argument("target", nargs='?', type=str, default=os.getcwd(),
                        )
    parser.add_argument("-o", "--output", type=str, default=default_output,
                        )
    parser.add_argument("--ignore", type=str, default='.gptignore',
                        )
    parser.add_argument("--repo-root", type=str, default=os.getcwd(),
                        )
    parser.add_argument("--debug", action="store_true",
                        )
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

    try:
        gptizer = GPTizer()
        if os.path.isdir(args.target):
            gptizer.process_directory(args.target, args.repo_root, args.ignore)
        elif os.path.isfile(args.target):
            gptizer.process_file(args.target, args.repo_root, args.ignore)
        else:
            raise ValueError(f"Invalid target: {args.target}")
        output_file_name = Settings.custom_output_file(gptizer.project.name, args.target)
        if args.output == Settings.default_output_file():
            args.output = output_file_name
        combined_content = gptizer.combine_files()
        with open(args.output, 'w', encoding='utf-8') as file:
            file.write(combined_content)
            logging.info(f"Files were combined into {args.output}")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
    except ValueError as e:
        logging.error(f"ValueError occurred: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
