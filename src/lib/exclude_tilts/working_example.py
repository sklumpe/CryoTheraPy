# automatically exclude tilts based on parameters determined in motioncorr and ctffind (before ML)
import os

class Main:
    def __init__(self, in_tilts, out_dir):
        self.out_dir = out_dir
        self.write_done_file()

    def write_done_file(self):
        done_file_path = os.path.join(self.out_dir, "done.txt")
        with open(done_file_path, "w") as f:
            f.write("still works")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 5:
        print("Usage: {} --i <input_tilts_file> --o <output_directory>".format(sys.argv[0]))
        sys.exit(1)

    in_tilts = sys.argv[2]
    out_dir = sys.argv[4]

    main_instance = Main(in_tilts, out_dir)
