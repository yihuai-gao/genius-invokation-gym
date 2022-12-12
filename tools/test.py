import subprocess as sp

# Test using black and isort
sp.run(["black", "gisim", "tools", "--check"])
sp.run(["isort", "gisim", "tools", "--profile", "black", "--check-only"])

# Test using pytest
# sp.run(["pytest", "gisim"])

# Test typing using pyright
sp.run(["pyright", "gisim"])
