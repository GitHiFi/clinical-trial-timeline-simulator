import pandas as pd
import argparse
from .simulation import ClinicalTrialSimulator
from .visualization import Visualizer
from .gcp import GCPChecker
from .config import AppConfig

def main():
    parser = argparse.ArgumentParser(description='Simulate clinical trial timeline (CLI).')
    parser.add_argument('--input', required=True, help='Path to input CSV')
    parser.add_argument('--theme', default=None, help='Visualization theme (dark/light)')
    args = parser.parse_args()

    AppConfig.load()  # Ensure config is loaded
    try:
        df = pd.read_csv(args.input)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    simulator = ClinicalTrialSimulator()
    df = simulator.simulate(df)
    df = simulator.calculate_end_dates(df)

    # Pass the theme argument to Visualizer
    visualizer = Visualizer(theme=args.theme)
    visualizer.generate_gantt(df)

    checker = GCPChecker()
    print(checker.check_flags(df))

if __name__ == '__main__':
    main()