import os

from dotenv import load_dotenv

from src.pipeline import run_automation


load_dotenv()


if __name__ == "__main__":
    print("Starting PHANTOMS Week 2 integrated pipeline")
    run_automation(
        cycles=int(os.getenv("PIPELINE_CYCLES", "3")),
        interval_seconds=int(os.getenv("PIPELINE_INTERVAL", "30")),
    )
