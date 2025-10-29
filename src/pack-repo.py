import sys
import tomli
import util
from arg_parser import ArgParser
from content_writer import ContentWriter

if __name__ == "__main__":
    #set argument parser
    parser = ArgParser("Pack Git Repository into a text file for use in LLM.")

    # Load configuration from .pack-repo.toml if it exists
    try:
        parser.load_config(".pack-repo.toml")
    except tomli.TOMLDecodeError:
        sys.exit(1)

    args = parser.get_args()
                
    #initialize variables
    paths = args.paths
    filename = args.output
    files = []
    n_of_lines = 0
    n_of_recent = 0
    show_hidden = args.all
    show_line_number = args.line_number
    show_dirs_only = args.dirs_only
    empty_lines_removed = args.remove_empty_lines
    writer = ContentWriter()
    
    #check file extensions to include in the output
    try:
        inc_exts = util.check_exts_to_include(args.include)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)

    #ensure that the paths input are either one directory/file, or multiple files in the same directory
    try:
        path_is_dir = util.check_path_is_dir(paths)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

    #set output stream
    ostream = sys.stdout
    if filename:
        ostream = writer.open_file(filename)
        print(f'File "{filename}" is created...')

    #write to output stream
    if filename:
        print("Writing file...")
    writer.write_file_location(ostream, paths, path_is_dir)
    writer.write_git_info(ostream, paths, path_is_dir)
    writer.write_struct_tree(ostream, paths, files, path_is_dir, inc_exts, show_hidden)
    if not show_dirs_only:
        n_of_recent, n_of_lines = writer.write_file_contents(ostream, paths, files, path_is_dir, args.recent, show_line_number, empty_lines_removed)
        if args.recent:
            writer.write_recent_changes_summary(ostream, n_of_recent)
    writer.write_summary(ostream, files, n_of_recent, n_of_lines, args.recent, show_dirs_only)

    #program complete
    if filename:
        ostream.close()
        print(f'All information is saved in "{filename}"')