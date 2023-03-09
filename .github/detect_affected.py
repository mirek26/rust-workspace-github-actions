import json
import subprocess
import sys

# Get data about workspace
metadata = json.loads(subprocess.check_output(['cargo', 'metadata', '--format-version=1']).decode("utf-8"))
packages = [p['name'] for p in metadata['packages']]
deps = {p['name']: [dep['name'] for dep in p['dependencies']] for p in metadata['packages']}
print(f"::debug::all-packages={packages}")

# Get changed files
changed_files = subprocess.check_output(["git", "diff", "--name-only", sys.argv[1], sys.argv[2]]).decode("utf-8").split()
print(f"::debug::changed-files={packages}")

# Calculate transitive dependencies
affected = [p for p in packages if any(file.startswith(p + '/') for file in changed_files)]
while True: 
    new_affected = [p for p in packages if p in affected or any([dep in affected for dep in deps[p]])]
    if len(new_affected) == len(affected):
        break
    affected = new_affected
print(f"affected={json.dumps(affected)}", file=sys.stderr)
