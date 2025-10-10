import re
from pathlib import Path

#check file extensions to include in the output
def check_exts_to_include(exts):
    if exts is None:
        return "all"
    
    exts = exts.split(",")
    for i in range(len(exts)):
        exts[i] = exts[i].strip()
        exts[i] = exts[i].lstrip("*")
        if not bool(re.match(r"^\.[a-zA-Z0-9]+$", exts[i])):
            raise ValueError('Invalid extensions, please check your input. Valid extension e.g. "*.js,*.txt"')
    return exts

#ensure that the paths input are either one directory/file, or multiple files in the same directory
def check_path_is_dir(paths):
    if len(paths) == 1:
        return Path(paths[0]).is_dir()

    #more than one paths are entered
    parent_path = Path(paths[0]).parent.resolve()
    for path in paths:
        path = Path(path)
        if not path.is_file() or path.parent.resolve() != parent_path:
            raise ValueError("Either one file/directory, or multiple files in the same directory can be entered.")
    return False