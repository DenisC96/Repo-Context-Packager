import argparse
import os
import tomli

class ArgParser:
    def __init__(self, desc):
        self.parser = self._init_parser(desc)

    def _init_parser(self, desc):
        parser = argparse.ArgumentParser(desc)

        parser.add_argument("paths", nargs="+", help="Path to the repository / files in the same repository")
        parser.add_argument("--version", "-v", action="version", version="repo-context-packager v0.1")
        parser.add_argument("--output", "-o", nargs="?", help="Output filename", default=None, const="repo-context.txt")
        parser.add_argument("--include", "-i", help='Extensions to be included, separated by ",", e.g. "*.js,*.txt"')
        parser.add_argument("--all", "-a", action="store_true", help='Show all files including hidden files (files that start with ".")')
        parser.add_argument("--recent", "-r", nargs="?", help="Only include files modified within the last 7 days", const=7, type=int)
        parser.add_argument("--line-number", "-l", action="store_true", help="Include line number when displaying file content output")
        parser.add_argument("--dirs-only", "-d", action="store_true", help="Show only directory structure tree without file contents")

        return parser

    def load_config(self, config_file):
        config = {}

        if os.path.exists(config_file):
            try:
                with open(config_file, "rb") as f:
                    config_from_file = tomli.load(f)
                    config = {k.replace('-', '_'): v for k, v in config_from_file.items()}
            except tomli.TOMLDecodeError:
                print(f"Error: Could not parse {config_file}. Please check its format.")
                raise
        
        # merge config file options with argparse
        if config:
            self.parser.set_defaults(**config)
    
    def get_args(self):
        return self.parser.parse_args()