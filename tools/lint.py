import subprocess as sp

# Lint using black and isort
sp.run(["black", "gisim", "tools"])
sp.run(["isort", "gisim", "tools", "--profile", "black"])
