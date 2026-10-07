import argparse


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sla", description="Self-Learning AI Agent")
    parser.add_argument("command", nargs="?", help="train | evaluate | reflect | dashboard | pipeline")
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
    else:
        print(f"'{args.command}' is not implemented yet.")


if __name__ == "__main__":
    main()
