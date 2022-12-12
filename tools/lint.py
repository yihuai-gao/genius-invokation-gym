import subprocess as sp

# Lint using black and isort
sp.run(["black", ".", "tests"])
sp.run(["isort", ".", "tests", "--profile", "black"])
