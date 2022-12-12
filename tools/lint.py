import subprocess as sp

# Lint using black and isort
sp.run(["black", "gisim"])
sp.run(["isort", "gisim", "--profile", "black"])
