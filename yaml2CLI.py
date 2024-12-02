import argparse
import os

import yaml

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--config", default="rcp-runai-job.yaml")

    args = parser.parse_args()

    # Read the YAML file
    with open(args.config, "r") as file:
        runai_job = yaml.load(file, Loader=yaml.FullLoader)
    command = "runai submit"

    # Iterate over the keys and values of the dictionary
    for key, value in runai_job.items():
        command += f" --{key} {value}"

    print(command)

    # Run the command
    os.system(command)
