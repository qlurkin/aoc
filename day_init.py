from datetime import date
import sys
import os
import subprocess as sp
import shutil

class OperationLogger:
    def __init__(self, msg):
        self.msg = msg

    def __enter__(self):
        print('{: <30}'.format(self.msg), end='')

    def __exit__(self, exc_type, exc_val, traceback):
        if exc_val is None:
            print('DONE')
        else:
            print('FAIL')
            print('   {}: {}'.format(exc_type.__name__, exc_val))
        return True

year = '{}'.format(date.today().year)
day = '{:0>2}'.format(date.today().day)

src_filename = 'puzzle.py'
root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
src_path = os.path.join(root_path, src_filename)
year_path = os.path.join(root_path, year)
day_path = os.path.join(year_path, 'day{}'.format(day))
dst_path = os.path.join(day_path, src_filename)
test_path = os.path.join(day_path, 'test')

if os.path.exists(day_path):
    print("{} already exists".format(day_path))
    sys.exit()

with OperationLogger("Create Day Folder"):
    os.makedirs(day_path)
    
with OperationLogger("Create Puzzle Script"):
    shutil.copy(src_path, dst_path)

with OperationLogger("Create Test Input File"):
    open(test_path, 'w').close()

os.chdir(day_path)

with OperationLogger("Download Puzzle Statement"):
    sp.run(['aoc', 'read'], capture_output=True).check_returncode()

with OperationLogger("Download Puzzle input"):
    sp.run(['aoc', 'download'], capture_output=True).check_returncode()

