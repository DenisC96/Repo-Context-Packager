import argparse
from pathlib import Path
from git import Repo
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
import time

def open_file(filename):
    f = Path(filename)
    f.write_text("# Repository Context\n\n")
    f = f.open("a")
    return f

def write_file_location(f, input_path):
    print("Writing file system location...")
    abs_path = Path(input_path).resolve()
    f.write("## File System Location\n\n")
    f.write(str(abs_path) + "\n\n")

def write_git_info(f, path):
    print("Writing Git info...")
    f.write("## Git Info\n\n")
    if (Path(path) / ".git").exists():
        repo = Repo(path)
        commit = repo.head.commit

        f.write(f"- Commit: {commit.hexsha}\n")
        f.write(f"- Branch: {repo.active_branch.name}\n")
        f.write(f"- Author: {commit.author.name} <{commit.author.email}>\n")
        f.write(f"- Date: {commit.committed_datetime.isoformat()}\n\n")
    else:
        f.write("Not a git repository\n\n")

def write_struct_tree(f, path, files):
    print("Writing Structure Tree...")

    def print_tree(f, path, root_path, prefix=""):
        f.write(f"{prefix}{path.name}/\n")
        for child in path.iterdir():
            if not child.name.startswith("."): #hidden files/directories are not shown for clarity
                if child.is_dir():
                    print_tree(f, child, root_path, prefix + "  ")
                else:
                    f.write(f"{prefix}  {child.name}\n")
                    files.append(child.relative_to(root_path)) #add to files list

    f.write("## Structure (hidden files/directories are not shown for clarity)\n\n```\n")
    path = Path(path).resolve()
    print_tree(f, path, path)
    f.write("```\n\n")

def write_file_contents(f_out, path, files):
    print("Writing file contents...")
    f_out.write("## File Contents\n\n")

    n_of_lines = 0
    n_of_recent = 0

    for file in files:
        abs_file_path = (Path(path) / file).resolve()
        if check_recent_changes(abs_file_path, args.recent):
            n_of_recent += 1
            days = int((time.time() - abs_file_path.stat().st_mtime) / 86400)
            f_out.write(f"### File: {file} (modified {days} days ago)\n")
            
            #determine any programming language used in the file
            try:
                lexer = guess_lexer_for_filename(abs_file_path.name, abs_file_path.read_text())
                f_out.write(f"```{lexer.name}\n")
            except ClassNotFound:
                f_out.write("```\n")

            with open(abs_file_path, "r") as f_in:
                for line in f_in:
                    f_out.write(line)
                    n_of_lines += 1
            f_out.write("\n```\n\n")
    return n_of_recent, n_of_lines

def write_summary(f, files, n_of_recent, n_of_lines):
    print("Writing summary...")
    f.write("## Summary\n\n")
    f.write(f"- Total files: {len(files)}\n")
    f.write(f"- Total recent files: {n_of_recent}\n")
    f.write(f"- Total lines: {n_of_lines}\n")

def check_recent_changes(file, days):
    now = time.time()
    cutoff = now - days * 86400

    return file.stat().st_mtime >= cutoff

if __name__ == "__main__":
    #set argument parser
    parser = argparse.ArgumentParser("Pack Git Repository into a text file for use in LLM.")
    parser.add_argument("path", help="Path to the repository / files in the same repository")
    parser.add_argument("--output", "-o", help="Output filename", default="repo-context.txt")
    parser.add_argument("--recent", "-r", nargs="?", help="Only include files modified within the last 7 days", const=7, type=int)
    
    args = parser.parse_args()

    #initialize variables
    path = args.path
    filename = args.output
    files = []
    n_of_lines = 0
    n_of_recent = 0

    #open file
    f = open_file(filename)
    print(f'File "{filename}" is created...')

    #write to file
    print("Writing file...")
    write_file_location(f, path)
    write_git_info(f, path)
    write_struct_tree(f, path, files)
    n_of_recent, n_of_lines = write_file_contents(f, path, files)
    write_summary(f, files, n_of_recent, n_of_lines)

    #program complete
    print(f'All information is saved in "{filename}"')