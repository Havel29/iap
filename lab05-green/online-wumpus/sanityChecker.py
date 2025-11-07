import subprocess
import re

while True:
    output_risky = subprocess.check_output("gridrunner --world WumpusWorld --entry solver:UserPlayerRisky --horizon=200", shell=True, text=True)
    print(output_risky)
    print(re.search(r"Exception", output_risky))
    if 'index' in output_risky:
        print("Problem still present")
        exit()
    else:
        print("No problem found")
