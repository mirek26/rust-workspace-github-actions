import json
import subprocess
import os

# Get data about workspace
metadata = json.loads(subprocess.check_output(['cargo', 'metadata']).decode("utf-8"))
packages = [p['name'] for p in metadata['packages']]
deps = {p['name']: [dep['name'] for dep in p['dependencies']] for p in metadata['packages']}
print('packages', packages)

# Get changed files
changed_files = subprocess.check_output(["git", "diff", "--name-only", os.args[1], os.args[2]]).decode("utf-8").split()
print('changed files', changed_files)

# Calculate transitive dependencies
affected = [p for p in packages if changed_files.any(lambda file: file.startswith(p + '/'))]
while True: 
    new_affected = [p for p in packages if p in affected or any([dep in affected for dep in deps[p]])]
    if len(new_affected) == len(affected):
        break
    affected = new_affected
print('affected', affected)
