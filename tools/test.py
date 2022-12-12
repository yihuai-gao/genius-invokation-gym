import subprocess as sp

# Test using black and isort
sp.run(["black", ".", "--check"])
sp.run(["isort", ".", "--profile", "black", "--check-only"])

# Test typing using pyright
sp.run(["pyright", "."])

# Test using pytest
sp.run(["pytest", "--cov", ".", "--cov-report", "xml"])
