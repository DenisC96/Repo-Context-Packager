import sys
import time
from pathlib import Path
from git import Repo
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
from datetime import datetime, timedelta

class ContentWriter:
    def __init__(self):
        pass

    def open_file(self, filename):
        f = Path(filename)
        f.write_text("# Repository Context\n\n")
        f = f.open("a")
        return f

    def write_file_location(self, ostream, paths, path_is_dir):
        if ostream != sys.stdout:
            print("Writing file system location...")

        abs_path = None
        if path_is_dir:
            abs_path = Path(paths[0]).resolve()
        else:
            abs_path = Path(paths[0]).parent.resolve()
        
        ostream.write("## File System Location\n\n")
        ostream.write(str(abs_path) + "\n\n")

    def write_git_info(self, ostream, paths, path_is_dir):
        if ostream != sys.stdout:
            print("Writing Git info...")
        ostream.write("## Git Info\n\n")

        parent_path = None
        if path_is_dir:
            parent_path = Path(paths[0])
        else:
            parent_path = Path(paths[0]).parent

        if (parent_path / ".git").exists():
            repo = Repo(parent_path)
            commit = repo.head.commit

            ostream.write(f"- Commit: {commit.hexsha}\n")
            ostream.write(f"- Branch: {repo.active_branch.name}\n")
            ostream.write(f"- Author: {commit.author.name} <{commit.author.email}>\n")
            ostream.write(f"- Date: {commit.committed_datetime.isoformat()}\n\n")
        else:
            ostream.write("Not a git repository\n\n")

    def write_struct_tree(self, ostream, paths, files, path_is_dir, inc_exts, show_hidden):
        if ostream != sys.stdout:
            print("Writing Structure Tree...")

        def print_tree(ostream, path, root_path, prefix=""):
            ostream.write(f"{prefix}{path.name}/\n")
            child_paths = None
            if show_hidden:
                child_paths = [child for child in path.iterdir() if not child.name.startswith(".git")] #ignore only .git files
            else:
                child_paths = [child for child in path.iterdir() if not child.name.startswith(".")] #ignore all hidden files

            for child in child_paths:
                if child.is_dir():
                    print_tree(ostream, child, root_path, prefix + "  ")
                else:
                    if inc_exts == "all":
                        ostream.write(f"{prefix}  {child.name}\n")
                        files.append(child.relative_to(root_path)) #add to files list
                    else:
                        if child.suffix in inc_exts:
                            ostream.write(f"{prefix}  {child.name}\n")
                            files.append(child.relative_to(root_path)) #add to files list

        if show_hidden:
            ostream.write("## Structure\n\n```\n")
        else:
            ostream.write("## Structure (hidden files/directories are not shown for clarity)\n\n```\n")

        parent_path = None
        if path_is_dir:
            parent_path = Path(paths[0]).resolve()
        else:
            parent_path = Path(paths[0]).parent.resolve()

        print_tree(ostream, parent_path, parent_path)
        ostream.write("```\n\n")

    def write_file_contents(self, ostream, paths, files, path_is_dir, recent_day, show_line_number, empty_lines_removed):
        def remove_empty_lines(content):
            lines = content.split('\n')
            lines = [line for line in lines if line.strip() != ""]
            return '\n'.join(lines)
        
        if ostream != sys.stdout:
            print("Writing file contents...")

        ostream.write("## File Contents\n")
        if recent_day:
            ostream.write("[Only the recently modified files would be included here]\n\n")
        else:
            ostream.write("\n")

        n_of_lines = 0
        n_of_recent = 0

        parent_path = None
        if path_is_dir:
            parent_path = Path(paths[0])
        else:
            parent_path = Path(paths[0]).parent
            files.clear()
            for path in paths:
                path = Path(path).relative_to(parent_path)
                files.append(path)

        for file in files:
            abs_file_path = (parent_path / file).resolve()
            if self.is_recently_modified(abs_file_path, recent_day):
                n_of_recent += 1
                days = int((time.time() - abs_file_path.stat().st_mtime) / 86400)
                ostream.write(f"### File: {file} (modified {days} days ago)\n")
                
                #determine any programming language used in the file
                try:
                    lexer = guess_lexer_for_filename(abs_file_path.name, abs_file_path.read_text())
                    ostream.write(f"```{lexer.name}\n")
                except ClassNotFound:
                    ostream.write("```\n")
                    sys.stderr.write(f"**Unable to determine language used in file {file}**\n")
                except UnicodeDecodeError:
                    pass

                try:
                    with open(abs_file_path, "r") as f_in:
                        # empty_lines_removed flag to be checked, and logic to be changed
                        for line_number, line in enumerate(f_in, start=1):
                            if show_line_number:
                                ostream.write(f"{line_number}: ")
                            ostream.write(line)
                            n_of_lines += 1
                    ostream.write("\n```\n\n")
                except UnicodeDecodeError:
                    ostream.write("**Unable to read file**\n\n")
                    sys.stderr.write(f"**Unable to read file {file}**\n")
        return n_of_recent, n_of_lines

    def write_summary(self, ostream, files, n_of_recent, n_of_lines, show_recent_only, show_dirs_only):
        if ostream != sys.stdout:
            print("Writing summary...")
        ostream.write("## Summary\n\n")
        ostream.write(f"- Total files: {len(files)}\n")
        if not show_dirs_only:
            if show_recent_only:
                ostream.write(f"- Total recent files: {n_of_recent}\n")
            ostream.write(f"- Total lines: {n_of_lines}\n")

    # Lab2 - add --recent flag (Added by Steven Hur)
    def is_recently_modified(self, file_path, days=None):
        # check file if modified within recent days
        if not days:
            return True
        
        try:
            file_last_time = file_path.stat().st_mtime
            now = datetime.now().timestamp() # current time
            time_difference = now - file_last_time
            return time_difference <= timedelta(days=days).total_seconds()
        except FileNotFoundError:
            return False

    # added by Steven Hur
    # simple message printer for --recent flag
    def write_recent_changes_summary(self, ostream, num_files):
        if ostream != sys.stdout:
            print("Writing recent changes Summary...")
        ostream.write("## Recent Changes Summary (Past 7 days)\n\n")
        ostream.write(f"- Found {num_files} recently modified files.\n\n")