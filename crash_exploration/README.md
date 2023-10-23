# Crash exploration

## Setup
git clone git@github.com:DeviRule/AFLplusplus.git
and apply afl_aurora.patch to afl++
## Usage
Run AFL with the desired options. Make sure to use a crashing input as seed and the -C flag to run AFL's crash exploration mode. Modified afl will then save crashing ('queue' folder) and non-crashing inputs ('non_crashes' folder) which are needed for tracing.

