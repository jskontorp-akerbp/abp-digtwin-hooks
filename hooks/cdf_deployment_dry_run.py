import shutil
import subprocess
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

def error_exit(message: str):
    """Log an error message and exit the program."""
    logging.error(message)
    sys.exit(1)

def check_prerequisites():
    """Step 0: Check prerequisites."""
    logging.info("Checking prerequisites")
    try:
        subprocess.run(["cdf", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        error_exit("Missing prerequisite: cognite-toolkit not found. Install it first by running 'pip install cognite-toolkit' in your preferred python environment.")

    if not Path("./config.dev.yaml").exists():
        error_exit("Missing prerequisite: Config file config.dev.yaml does not exist. "
                   "Set up your cdf module with 'cdf modules init'. Exiting deployment dry run.")

    if not Path("./modules").is_dir():
        error_exit("Missing prerequisite: No modules/ directory found. It should be initialized with 'cdf modules init'. Exiting deployment dry run.")

    logging.info("Prerequisites met")

def synchronize_directories(src_dir: str, dest_dir: str):
    """Step 1: Synchronize source with destination directory."""
    if not Path(src_dir).is_dir():
        error_exit(f"Source directory '{src_dir}' does not exist. Exiting deployment dry run.")

    logging.info(f"Synchronizing '{src_dir}/' with '{dest_dir}/'")
    subprocess.run(["rsync", "-a", "--delete", f"{src_dir}/", dest_dir], check=True)
    logging.info(f"Synchronized '{dest_dir}/' with '{src_dir}/'")

def prefix_directories_with_fn(base_dir: str):
    """Step 2: Prefix all directories in a given path with 'fn_'."""
    functions_dir = Path(base_dir)
    if not functions_dir.is_dir():
        error_exit(f"Directory '{base_dir}' not found. Exiting deployment dry run.")
    
    logging.info(f"Prefixing directories in '{base_dir}' with 'fn_'")
    for dir_path in functions_dir.iterdir():
        if dir_path.is_dir() and not dir_path.name.startswith("fn_"):
            new_name = dir_path.parent / f"fn_{dir_path.name}"
            dir_path.rename(new_name)
            logging.debug(f"Renaming '{dir_path}' to '{new_name}'")
    logging.info(f"Prefixed directories in '{base_dir}' with 'fn_'")

def run_cdf_build():
    """Step 3: Run 'cdf build' after cleaning up build directory."""
    build_dir = Path("./build")
    if build_dir.exists() and build_dir.is_dir():
        logging.info("Deleting existing build directory './build'")
        shutil.rmtree(build_dir)

    logging.info("Running 'cdf build'")
    subprocess.run(["cdf", "build"], check=True)

def run_cdf_deploy_dry_run():
    """Step 4: Run 'cdf deploy --dry-run'."""
    logging.info("Running 'cdf deploy --dry-run'")
    subprocess.run(["cdf", "deploy", "--dry-run"], check=True)

def main():
    try:
        # Step 0: Check prerequisites
        check_prerequisites()

        # Step 1: Synchronize directories
        synchronize_directories("./CogniteDataFusion", "modules/CogniteDataFusion")

        # Step 2: Prefix directories with 'fn_'
        prefix_directories_with_fn("modules/CogniteDataFusion/functions")

        # Step 3: Run 'cdf build'
        run_cdf_build()

        # Step 4: Run 'cdf deploy --dry-run'
        run_cdf_deploy_dry_run()

        logging.info("All steps completed successfully!")
    except Exception as e:
        error_exit(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
