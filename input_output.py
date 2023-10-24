import os
import subprocess
from pathlib import Path
import shutil


PROJECT_NAME = "garfield"
SOURCE_INPUT_PATH = f"/shared/{PROJECT_NAME}"
CRASH_INPUT_PATH = f"/shared/{PROJECT_NAME}"
OUTPUT_PATH = f"/shared/{PROJECT_NAME}"
HOME_PATH = "/home/user"
EVALUATION_PATH = f"{HOME_PATH}/evaluation"
FUZZ_TARGET = f"{PROJECT_NAME}_fuzz"
TRACE_TARGET = f"{PROJECT_NAME}_trace"
FUZZ_TIMEOUT = "20000"

def build_fuzz():
    base_path = Path(SOURCE_INPUT_PATH)
    full_path = base_path / "challenge_src"
    os.chdir(full_path)
    subprocess.run(["make","clean"])
    # Copy the current environment variables and modify CC
    env = os.environ.copy()
    env["CC"] = "afl-g++"
    result = subprocess.run(['make'], env=env)

    source_file = base_path / "challenge_src" / "build" / "garfield.bin"
    destination_directory = Path(EVALUATION_PATH)
    print(f"move {source_file} to {destination_directory} and rename it to {FUZZ_TARGET}")
    subprocess.run([
        "mv",
        f"{source_file}",
        f"{destination_directory}/{FUZZ_TARGET}"
    ])
    

def build_trace():
    base_path = Path(SOURCE_INPUT_PATH)
    full_path = base_path / "challenge_src"
    os.chdir(full_path)
    subprocess.run(["make","clean"])
    # Copy the current environment variables and modify CC
    env = os.environ.copy()
    env["CC"] = "g++"
    result = subprocess.run(['make'], env=env)
    base_path = Path(SOURCE_INPUT_PATH)
    source_file = base_path / "challenge_src" / "build" / "garfield.bin"
    destination_directory = Path(EVALUATION_PATH)
    print(f"move {source_file} to {destination_directory} and rename it to {TRACE_TARGET}")
    subprocess.run([
        "mv",
        f"{source_file}",
        f"{destination_directory}/{TRACE_TARGET}"
    ])
    
    

def run_fuzz():
    env = os.environ.copy()
    print(env)
    # for chess target 
    env["CHESS"] = "1"
    return_code = subprocess.run([f'{env["AURORA_GIT_DIR"]}/docker/01_afl.sh', FUZZ_TIMEOUT , f'{FUZZ_TARGET}'],env=env)

def run_trace():
    env = os.environ.copy()
    # for chess target 
    env["CHESS"] = "1"
    return_code = subprocess.run([f'{env["AURORA_GIT_DIR"]}/docker/02_tracing.sh', TRACE_TARGET],env=env)

def run_rca():
    env = os.environ.copy()
    # for chess target 
    env["CHESS"] = "1"
    return_code = subprocess.run([f'{env["AURORA_GIT_DIR"]}/docker/03_rca.sh'],env=env)

if __name__ == "__main__":

    build_fuzz()
    build_trace()
    run_fuzz()
    run_trace()
    run_rca()
