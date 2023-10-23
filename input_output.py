import os
import subprocess
from pathlib import Path
import shutil


PROJECT_NAME = "garfield"
SOURCE_INPUT_PATH = f"/shared/{PROJECT_NAME}"
CRASH_INPUT_PATH = f"/shared/{PROJECT_NAME}"
OUTPUT_PATH = f"/shared/{PROJECT_NAME}"
EVALUATION_PATH = f"~/evaluation"
FUZZ_TARGET = f"{PROJECT_NAME}_fuzz"
TRACE_TARGET = f"{PROJECT_NAME}_trace"
FUZZ_TIMEOUT = "60"

def build_fuzz():
    base_path = Path(SOURCE_INPUT_PATH)
    full_path = base_path / "challenge_src"
    os.chdir(full_path)
    subprocess.run(["make","clean"])
    # Copy the current environment variables and modify CC
    env = os.environ.copy()
    env["CC"] = "afl-clang++"
    result = subprocess.run(['make'], env=env)

    source_file = base_path / "challeng_src" / "build" / "garfield.bin"
    destination_directory = Path(EVALUATION_PATH)
    shutil.move(source_file, destination_directory + FUZZ_TARGET)
    

def build_trace():
    base_path = Path(SOURCE_INPUT_PATH)
    full_path = base_path / "challenge_src"
    os.chdir(full_path)
    subprocess.run(["make","clean"])
    # Copy the current environment variables and modify CC
    env = os.environ.copy()
    env["CC"] = "clang++"
    result = subprocess.run(['make'], env=env)
    base_path = Path(SOURCE_INPUT_PATH)
    source_file = base_path / "challeng_src" / "build" / "garfield.bin"
    destination_directory = Path(EVALUATION_PATH)
    shutil.move(source_file, destination_directory + FUZZ_TARGET)
    

def run_fuzz():
    return_code = subprocess.call(['$AURORA_GIT_DIR/docker/02_tracing.sh', FUZZ_TIMEOUT , f'{EVALUATION_PATH}/{FUZZ_TARGET}'])

def run_trace():
    return_code = subprocess.call(['$AURORA_GIT_DIR/docker/02_tracing.sh',f'{EVALUATION_PATH}/{TRACE_TARGET}'])

def run_rca():
    return_code = subprocess.call(['$AURORA_GIT_DIR/docker/03_rca.sh'])

