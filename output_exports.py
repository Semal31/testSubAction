import os
import sys
import json
import argparse

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process to mark .env files as run in the json.')
    parser.add_argument('mark_as_run', type=bool, nargs='?', const=True, default=False,
                        help='Whether to mark the .env file as run in the status file (default: False)')
    args = parser.parse_args()

    env_runs_file_path = "./env_runs.json"
    
    # Load status file or create a new status dictionary if it doesn't exist
    if os.path.isfile(env_runs_file_path):
        with open(env_runs_file_path, 'r') as env_run:
            runs = json.load(env_run)

    # Find the first unprocessed .env file
    env_dir = "./env-files/"
    env_files = [v for v in os.listdir(env_dir) if v.endswith('.env')]
    env_name = None
    for file in env_files:
        if file not in runs or runs[file] != 'run':
            env_name = file
            break

    if not env_name:
        print("No unprocessed .env files found.")
        sys.exit(0)

    env_file_path = os.path.join(env_dir, env_name)

    # Check if the env file exists
    if not os.path.isfile(env_file_path):
        print(f"Error: .env file does not exist at specified path: {env_file_path}")
        sys.exit(1)

    # Print environment variables from the .env file
    if args.mark_as_run == False:
        with open(env_file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    print(f"TF_VAR_{key}='{value}'")  # Output the export command

    # Mark the file as processed in the status file
    if args.mark_as_run:
        runs[env_name] = 'run'
        with open(env_runs_file_path, 'w') as env_run:
            json.dump(runs, env_run, indent=2)

if __name__ == "__main__":
    main()