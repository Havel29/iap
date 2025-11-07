import subprocess
import re
import os

score_risky = 0
score_safe = 0
total = 0
episodes = 40
for i in range(episodes):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Progress: {i+1}/{episodes}")
    total += 1
    output_risky = subprocess.check_output("gridrunner --world WumpusWorld --entry solver:UserPlayerRisky --horizon=200", shell=True, text=True)
    output_safe = subprocess.check_output("gridrunner --world WumpusWorld --entry solver:UserPlayerSafe --horizon=200", shell=True, text=True)
    score_risky += int(re.search(r"Episode terminated with a reward of (-?\d+)", output_risky).group(1))
    score_safe += int(re.search(r"Episode terminated with a reward of (-?\d+)", output_safe).group(1))
    
print(f"Success for safe: {score_safe}")
print(f"Success for risky: {score_risky}")
