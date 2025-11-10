import unittest
import tempfile
import os
import time
from pathlib import Path
import util
from content_writer import ContentWriter

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

if __name__ == "__main__":
    unittest.main()