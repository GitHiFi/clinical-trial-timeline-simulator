import pandas as pd
import numpy as np
from scipy import stats
from .simulation import TimelineSimulator
from .config import AppConfig

class HistoricalDelaySimulator(TimelineSimulator):
    """Simulates delays based on historical trial data."""
    def __init__(self):
        self.historical_data = pd.read_csv('data/historical_delays.csv')
        self.base_delays = AppConfig.get_delays()

    def simulate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply historical delay distributions."""
        df['Duration'] = df['Duration'].astype(float)
        for phase in df['Phase']:
            if phase in self.base_delays:
                hist_delays = self.historical_data[self.historical_data['Phase'] == phase]['Delay']
                if not hist_delays.empty:
                    delay = np.random.choice(hist_delays)
                else:
                    delay = np.random.normal(self.base_delays[phase]['mean'], self.base_delays[phase]['std'])
                df.loc[df['Phase'] == phase, 'Duration'] += delay
        df['Duration'] = df['Duration'].clip(lower=1)
        return df