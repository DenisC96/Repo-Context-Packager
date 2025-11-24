import pytest
import os
import tomli
import argparse
import sys
from io import BytesIO

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'repo_context_packager'))
sys.path.insert(0, src_dir)

from arg_parser import ArgParser

class TestArgParser:
    def test_init_creates_parser(self):
        arg_parser = ArgParser("Test Description")
        assert isinstance(arg_parser.parser, argparse.ArgumentParser)

    def test_load_config_updates_defaults(self, tmp_path):
        config_content = b'output = "custom_output.txt"\nline-number = true'
        config_file = tmp_path / "test_config.toml"
        
        with open(config_file, "wb") as f:
            f.write(config_content)

        arg_parser = ArgParser("Test Description")
        arg_parser.load_config(str(config_file))

        assert arg_parser.parser.get_default("output") == "custom_output.txt"
        assert arg_parser.parser.get_default("line_number") is True

    def test_load_config_handles_nonexistent_file(self):
        arg_parser = ArgParser("Test Description")
        arg_parser.load_config("non_existent_file.toml")
        assert arg_parser.parser.get_default("output") is None

    def test_load_config_raises_error_on_bad_toml(self, tmp_path):
        bad_content = b'this is not valid toml'
        bad_file = tmp_path / "bad_config.toml"
        
        with open(bad_file, "wb") as f:
            f.write(bad_content)

        arg_parser = ArgParser("Test Description")

        with pytest.raises(tomli.TOMLDecodeError):
            arg_parser.load_config(str(bad_file))