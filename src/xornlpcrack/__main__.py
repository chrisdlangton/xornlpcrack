import logging, argparse, sys, os, getpass, json

from pathlib import Path
from rich.logging import RichHandler
import nltk
from xornlpcrack import derive_key, xor

logger = logging.getLogger(__name__)

def main():
    cli = argparse.ArgumentParser()
    cli.add_argument(
        "-d",
        "--download-dir",
        help="set location to store NLP data downloaded",
        dest="download_dir",
        default=None,
    )
    cli.add_argument(
        "-s",
        "--skip-download",
        help="skip the NLP data downloaded (assumes data was downloaded already)",
        dest="skip_download",
        action="store_true",
    )
    group = cli.add_mutually_exclusive_group()
    group.add_argument(
        "-v",
        "--verbose",
        help="set logging level to INFO",
        dest="log_verbose",
        action="store_true",
    )
    group.add_argument(
        "-vv",
        "--debug",
        help="set logging level to DEBUG",
        dest="log_debug",
        action="store_true",
    )
    group.add_argument(
        "-q",
        "--no-logging",
        help="disable logging (except for results)",
        dest="quiet",
        action="store_true",
    )
    cli.add_argument(
        choices=["crack", "gen"],
        nargs="?",
        dest="action",
        default="crack"
    )
    cli.add_argument(
        "-x",
        "--exact-key-len",
        help="set a known key length, this will be ignored if not provided and a length will be derived from --upper-key-len and --lower-key-len",
        dest="exact_key_length",
        type=int,
        default=None,
    )
    cli.add_argument(
        "-l",
        "--lower-key-len",
        help="set a minimum key length to start cracking from",
        dest="min_key_length",
        type=int,
        default=1,
    )
    cli.add_argument(
        "-u",
        "--upper-key-len",
        help="set a max key length to stop trying to derive the secret key",
        dest="max_key_length",
        type=int,
        default=4,
    )
    cli.add_argument(
        "-f",
        "--dump-enc-file",
        help="when using the generate action, set the filename to output the generated ciphertext value (default: stdout)",
        dest="output_file",
        default=None,
    )
    cli.add_argument(
        "-o",
        "--result-file",
        help="json file to store results",
        dest="result_file",
        default=None,
    )
    cli.add_argument(
        "-t",
        "--nlp-threshold",
        help="set a percentage of detected english words in the deciphered text, only guesses above this will be in the results",
        dest="nlp_threshold",
        type=lambda x: (int(x) < 100 and int(x) > 1) and int(x) or sys.exit("threshold between 1 and 100"),
        default=50,
    )
    args, input_refs = cli.parse_known_args()
    log_level = logging.WARNING
    if args.log_verbose:
        log_level = logging.INFO
    if args.log_debug:
        log_level = logging.DEBUG

    handlers = []
    log_format = "%(asctime)s - %(name)s - [%(levelname)s] %(message)s"
    if not args.quiet and sys.stdout.isatty():
        log_format = "%(message)s"
        handlers.append(RichHandler(rich_tracebacks=True))
    logging.basicConfig(format=log_format, level=log_level, handlers=handlers)

    if args.action == "crack":
        ciphertext = ''
        if check_stdin := sys.stdin:
            ciphertext = check_stdin
        for input_ref in input_refs:
            input_path = Path(input_ref)
            if input_path.exists():
                ciphertext = input_path.read_text()
                break
        if not ciphertext:
            logger.critical("ciphertext file was not provided or piped as input")
            sys.exit(1)

        # Download the words dataset from nltk
        if not args.download_dir:
            dirname, basename = os.path.split(os.path.curdir)
            download_dir = os.path.join(basename, dirname, '.nltk/')
        else:
            download_dir = args.download_dir
        if not args.skip_download:
            os.makedirs(download_dir, exist_ok=True)
            nltk.download('words', quiet=args.quiet, raise_on_error=True, download_dir=download_dir)
            nltk.download('punkt', quiet=args.quiet, download_dir=download_dir)

        results = derive_key(
            ciphertext,
            with_length=args.exact_key_length,
            max_length=args.max_key_length,
            min_length=args.min_key_length,
            threshold=args.nlp_threshold,
        )
        if args.result_file:
            dirname, _ = os.path.split(args.result_file)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            output_path = Path(args.result_file)
            fields = ['flag', 'key', 'threshold']
            output_path.write_text(json.dumps([dict(zip(fields, d)) for d in results], default=str))

    elif args.action == "gen":
        # Generate from vars for testing
        secret_key = getpass.getpass('Enter secret key:')
        flag = ''
        if check_stdin := sys.stdin:
            flag = check_stdin
        if input_refs:
            flag = ' '.join(input_refs)
        if not flag:
            logger.critical("A flag was not provided at the end of the arguments, or piped as input")
            sys.exit(1)
        generated_ciphertext: str = xor(flag, secret_key)
        if args.output_file:
            dirname, _ = os.path.split(args.output_file)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            output_path = Path(args.output_file)
            output_path.write_text(generated_ciphertext)
        print(generated_ciphertext)
        sys.exit(0)

    else:
        logger.critical("use `xornlp gen` to generate a ciphertext for testing or `xornlp crack` to use the tool")
        sys.exit(1)

if __name__ == "__main__":
    main()
