import requests

# Recursive function to fetch dependents and build a tree structure
def fetch_dependents(package, version, current_depth, depth_limit):
    if current_depth > depth_limit:
        return {}  # Stop if depth limit is reached

    # Construct the API URL, handling scoped packages (starting with '@')
    if package.startswith('@'):
        parsed = package.split("/")
        url = f'https://deps.dev/_/s/npm/p/{parsed[0]}%2F{parsed[1]}/v/{version}/dependents'
    else:
        url = f'https://deps.dev/_/s/npm/p/{package}/v/{version}/dependents'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

    
    direct_sample = json_data.get('directSample', [])
    direct_count = json_data.get('directCount', [])
    # Initialize tree structure for the current package
    tree = {
        "package": package,  # Include the package name
        "version": version,  # Include the version of the current package
        "dep_nums" : direct_count,
        "dependents": [],
    }

    # Fetch the direct samples (dependents)

    # Recursively build the dependency tree for each dependent
    for sample in direct_sample:
        dep_name = sample['package']['name']
        dep_version = sample['version']
        
        # Recursive call to get the dependents of the current dependent
        dependent_tree = fetch_dependents(dep_name, dep_version, current_depth + 1, depth_limit)
        dependents = dependent_tree.get("dependents", {})
        # Add the dependent package information to the tree
        tree["dependents"].append({
            "package": dep_name,
            "version": dep_version,
            "dep_nums" : len(dependents),
            "dependents": dependents  # Attach the dependents subtree
        })
    
    return tree

# Initial parameters
root_package = "lodash.merge"
root_version = "4.6.2"
depth_limit = 1  # Set the maximum recursion depth

# Start fetching and building the dependency tree from the root package
dependency_tree = fetch_dependents(root_package, root_version, 1, depth_limit)

# Output the tree structure
import json
print(json.dumps(dependency_tree, indent=4))
