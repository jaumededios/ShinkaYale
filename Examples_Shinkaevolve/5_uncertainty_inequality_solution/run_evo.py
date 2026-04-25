#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

import yaml

from shinka.core import EvolutionConfig, ShinkaEvolveRunner
from shinka.database import DatabaseConfig
from shinka.launch import LocalJobConfig


def main(config_fname: str):
    here = Path(__file__).resolve().parent
    os.chdir(here)

    cfg = yaml.safe_load((here / config_fname).read_text())
    cfg["evo"]["task_sys_msg"] = (here / "prompt.txt").read_text().strip()

    ShinkaEvolveRunner(
        evo_config=EvolutionConfig(**cfg["evo"]),
        job_config=LocalJobConfig(**cfg["job"]),
        db_config=DatabaseConfig(**cfg["db"]),
        max_evaluation_jobs=cfg["max_evaluation_jobs"],
        max_proposal_jobs=cfg["max_proposal_jobs"],
        max_db_workers=cfg["max_db_workers"],
        verbose=cfg.get("verbose", True),
    ).run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config-fname", default="shinka.yaml")
    args = parser.parse_args()
    main(args.config_fname)
