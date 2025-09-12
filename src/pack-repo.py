import argparse
from pathlib import Path
from git import Repo

def open_file(filename):
    f = Path(filename)
    f.write_text("# Repository Context\n\n")
    return f

def write_file_location(f, input_path):
    print("Writing file system location...")
    abs_path = Path(input_path).resolve()
    with f.open("a") as f:
        f.write("## File System Location\n\n")
        f.write(str(abs_path) + "\n\n")

def write_git_info(f, path):
    print("Writing Git info...")
    with f.open("a") as f:
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
            
def write_struct_tree(f):
    print("***Codes for writing Project Structure Tree to be implemented***")
    with f.open("a") as f:
        f.write("## Structure\n\n")
        f.write("***To be implemented***\n\n")

def write_file_contents(f):
    print("***Codes for writing File Content to be implemented***")
    with f.open("a") as f:
        f.write("## File Contents\n\n")
        f.write("***To be implemented***\n\n")

def write_summary(f):
    print("***Codes for writing Summary Statistics to be implemented***")
    with f.open("a") as f:
        f.write("## Summary\n\n")
        f.write("***To be implemented***\n\n")

if __name__ == "__main__":
    #set argument parser
    parser = argparse.ArgumentParser("Pack Git Repository into a text file for use in LLM.")
    parser.add_argument("path", help="Path to the repository / files in the same repository")
    parser.add_argument("--output", "-o", help="Output filename", default="repo-context.txt")
    
    args = parser.parse_args()

    #initialize variables
    path = args.path
    filename = args.output

    #open file
    f = open_file(filename)
    print(f'File "{filename}" is created...')

    #write to file
    print("Writing file...")
    write_file_location(f, path)
    write_git_info(f, path)
    write_struct_tree(f)
    write_file_contents(f)
    write_summary(f)

    #program complete
    print(f'All information is saved in "{args.output}"')