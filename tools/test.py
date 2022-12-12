import subprocess as sp

# Test using black and isort
sp.run(["black", ".", "--check"])
sp.run(["isort", ".", "--profile", "black", "--check-only"])

# Test using pytest
sp.run(["pytest", "."])

# Test typing using pyright
sp.run(["pyright", "."])
