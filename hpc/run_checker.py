import glob
import pandas as pd
import itertools
import json
import os
from dotenv import load_dotenv
import re


def complete_run_check(param_sample):
    # Empty dataframe for completed runs
    completed_runs = pd.DataFrame(
        {"start": [0], "alpha": [0], "lamda": [0], "run": [0]}
    )

    # Which runs were completed
    for param in param_sample:
        sample = re.split("[\\\\/]", param)[-1]
        # "\\" to run locally, "/" on HPC or with multiprocess
        start = sample.split("year")[1].split("_")[0]
        alpha = sample.split("alpha")[1].split("_")[0]
        lamda = sample.split("lamda")[1].split("_")[0]
        run_outputs = glob.glob(f"{param}/run*/origin_destination.csv")
        runs = []
        for output in run_outputs:
            indiv = re.split("[\\\\/]", output.split("run_")[1])[0]
            # "\\" to run locally, "/" on HPC or with multiprocess
            runs.append(int(indiv))
        for run in runs:
            completed_runs = completed_runs.append(
                pd.Series({
                    "start": start,
                    "alpha": alpha,
                    "lamda": lamda,
                    "run": run
                }),
                ignore_index=True,
            )
    # Write it to a .csv for safe keeping
    completed_runs.drop(index=0, inplace=True)
    completed_runs.to_csv("completed_runs.csv")
    return completed_runs


# Extract the missingness to a list
def pending_run_check(completed_runs, param_sets, full_set):
    results = []
    for param_set in param_sets:
        alpha, lamda, start = param_set
        complete_runs = set(
            completed_runs.loc[
                (completed_runs["start"] == start)
                & (completed_runs["lamda"] == lamda)
                & (completed_runs["alpha"] == alpha)
            ]["run"]
        )
        missing_runs = full_set - complete_runs
        if len(missing_runs) > 0:
            results.append([param_set, missing_runs])
    return results


def run_checker(param_sample):
    # Global parameters from config
    with open("config.json") as json_file:
        config = json.load(json_file)
    alphas = config["alphas"]
    lamdas = config["lamdas"]
    start_years = config["start_years"]
    start_run = config["start_run"]
    end_run = config["end_run"]

    # Recreate the full parameter set used for the runs
    param_list = [alphas, lamdas, start_years]
    param_sets = list(itertools.product(*param_list))

    # Create the range of runs expected, as a set
    full_set = set(range(start_run, end_run + 1))

    complete_run_check(param_sample)
    completed_runs = pd.read_csv("completed_runs.csv")
    pending_runs = pending_run_check(completed_runs, param_sets, full_set)
    return pending_runs


if __name__ == "__main__":
    # Data paths from env
    load_dotenv(os.path.join(".env"))
    data_dir = os.getenv("DATA_PATH")
    input_dir = os.getenv("INPUT_PATH")
    out_dir = os.getenv("OUTPUT_PATH")

    with open("config.json") as json_file:
        config = json.load(json_file)
    sim_name = config["sim_name"]
    #commodity = f"{config['commodidty_list']}"
    commodity = "0702-120991-070960"
    # Call the folders
    param_sample = glob.glob(f"{out_dir}/{sim_name}/*{commodity}*")
    pending_runs = run_checker(param_sample)

    file1 = open("pending_runs.txt", "w")
    for sample in pending_runs:
        alpha, lamda, start = sample[0]
        missing_runs = sample[1]
        output = (
            " ".join(
                [
                    "python",
                    "model_run_args.py",
                    str(alpha),
                    str(lamda),
                    str(start),
                    str(min(missing_runs)),
                    str(max(missing_runs)),
                ]
            )
            + "\n"
        )
        file1.write(output)
    file1.close()
