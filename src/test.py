import unittest
import tempfile
import os
import time
import io
from pathlib import Path
from content_writer import ContentWriter
import util as util

class TestUtil(unittest.TestCase):
    #Tests for check_exts_to_include
    def test_check_exts_to_include_valid(self):
        # valid case
        valid = util.check_exts_to_include("*.py,*.txt")
        self.assertEqual(valid, [".py", ".txt"])

    def test_check_exts_to_include_invalid(self):
        # invalid case
        with self.assertRaises(ValueError):
            util.check_exts_to_include("py,txt")

    def test_check_exts_to_include_none(self):
        # return "all" if no extensions are provided 
        result = util.check_exts_to_include(None)
        self.assertEqual(result, "all")

    #Tests for check_path_is_dir
    def test_check_path_is_dir_tempdir(self):
        # path is a dir
        with tempfile.TemporaryDirectory() as tmpdir:
            result = util.check_path_is_dir([tmpdir])
            self.assertTrue(result)
            
    def test_check_path_is_dir_tempfile(self):
        # paths are not dir
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "file1.txt"
            file2 = Path(tmpdir) / "file2.txt"

            file1.write_text("test")
            file2.write_text("test")

            result = util.check_path_is_dir([file1, file2])
            self.assertFalse(result)

class TestContentWriter(unittest.TestCase):
    #Tests for is_recently_modified
    def test_is_recently_modified_within_range(self):
        writer = ContentWriter()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)

        # tmp should be recent
        self.assertTrue(writer.is_recently_modified(tmp_path, 7))

        os.remove(tmp_path)
    
    def test_is_recently_modified_out_of_range(self):
        writer = ContentWriter()
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = Path(tmp.name)

        # set access and modification time of tmp to 8 days ago
        old_time = time.time() - (8 * 86400)
        os.utime(tmp_path, (old_time, old_time))
        self.assertFalse(writer.is_recently_modified(tmp_path, 7))

        os.remove(tmp_path)
    
    # Tests for write_summary
    def test_write_summary_dirs_only(self):
        writer = ContentWriter()
        ostream = io.StringIO()
        files = ["file1.txt", "file2.txt"]

        writer.write_summary(
            ostream=ostream,
            files=files,
            n_of_recent=0,
            n_of_lines=0,
            show_recent_only=False,
            show_dirs_only=True
        )

        output = ostream.getvalue()
        self.assertIn("## Summary", output)
        self.assertIn("- Total files: 2", output)
        self.assertNotIn("Total lines", output)

    def test_write_summary_with_recent_files(self):
        writer = ContentWriter()
        ostream = io.StringIO()
        files = ["file1.txt", "file2.txt", "file3.txt"]

        writer.write_summary(
            ostream=ostream,
            files=files,
            n_of_recent=2,
            n_of_lines=50,
            show_recent_only=True,
            show_dirs_only=False
        )

        output = ostream.getvalue()
        self.assertIn("## Summary", output)
        self.assertIn("- Total files: 3", output)
        self.assertIn("- Total recent files: 2", output)
        self.assertIn("- Total lines: 50", output)

if __name__ == "__main__":
    unittest.main()