
import itertools
import json
import os
import pickle
import timeit
from abc import ABC, abstractmethod
from multiprocessing import cpu_count
from pathlib import Path

import numpy as np

def get_from_config():
    """Get benchmarks configuration from the config.json file"""
    current_path = Path(__file__).resolve().parent

    config_path = current_path / "config.json"
    with open(config_path, "r") as config_file:
        config_file = "".join(line for line in config_file if line and "//" not in line)
        config = json.loads(config_file)

    profile = os.getenv("SKLBENCH_PROFILE", config["profile"])

    n_jobs_vals_env = os.getenv("SKLBENCH_NJOBS")
    if n_jobs_vals_env:
        n_jobs_vals = json.loads(n_jobs_vals_env)
    else:
        n_jobs_vals = config["n_jobs_vals"]
    if not n_jobs_vals:
        n_jobs_vals = list(range(1, 1 + cpu_count()))

    cache_path = current_path / "cache"
    cache_path.mkdir(exist_ok=True)
    (cache_path / "estimators").mkdir(exist_ok=True)
    (cache_path / "tmp").mkdir(exist_ok=True)

    save_estimators = os.getenv("SKLBENCH_SAVE_ESTIMATORS", config["save_estimators"])
    save_dir = os.getenv("ASV_COMMIT", "new")[:8]
    if save_estimators:
        (cache_path / "estimators" / save_dir).mkdir(exist_ok=True)

    base_commit = os.getenv("SKLBENCH_BASE_COMMIT", config["base_commit"])

    bench_predict = os.getenv("SKLBENCH_PREDICT", config["bench_predict"])
    bench_transform = os.getenv("SKLBENCH_TRANSFORM", config["bench_transform"])

    return (
        profile,
        n_jobs_vals,
        save_estimators,
        save_dir,
        base_commit,
        bench_predict,
        bench_transform,
    )
