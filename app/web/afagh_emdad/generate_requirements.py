import toml


def convert_version(version):
    # If the version starts with ^, convert it to >= and < next major version
    if version.startswith("^"):
        version_number = version[1:]
        major_version = int(version_number.split(".")[0])
        next_major_version = major_version + 1
        return f">={version_number},<{next_major_version}.0.0"
    return version


# Load the pyproject.toml file
with open("pyproject.toml", "r") as f:
    pyproject = toml.load(f)

# Extract dependencies
dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dependencies", {})
dev_dependencies = pyproject.get("tool", {}).get("poetry", {}).get("dev-dependencies", {})

# Write to requirements.txt
with open("requirements.txt", "w") as f:
    for package, version in dependencies.items():
        if package != "python":
            if isinstance(version, dict):
                version = version["version"]
            f.write(f"{package}{convert_version(version)}\n")
    for package, version in dev_dependencies.items():
        if isinstance(version, dict):
            version = version["version"]
        f.write(f"{package}{convert_version(version)}\n")
