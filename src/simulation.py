import pandas as pd
import numpy as np
from typing import Dict
from datetime import timedelta  # Added import
from abc import ABC, abstractmethod
from .config import AppConfig

class TimelineSimulator(ABC):
    """Abstract base class for timeline simulators, allowing extensions."""
    @abstractmethod
    def simulate(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

class ClinicalTrialSimulator(TimelineSimulator):
    """Concrete simulator for clinical trials with realistic delays."""
    def __init__(self):
        self.delay_params: Dict[str, Dict[str, float]] = AppConfig.get_delays()

    def simulate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply phase-specific delays."""
        # Ensure Duration is float to avoid dtype warnings
        df['Duration'] = df['Duration'].astype(float)
        for phase in df['Phase']:
            if phase in self.delay_params:
                delay = np.random.normal(
                    self.delay_params[phase]['mean'],
                    self.delay_params[phase]['std'],
                    1
                )[0]
                df.loc[df['Phase'] == phase, 'Duration'] += delay
        df['Duration'] = df['Duration'].clip(lower=1)
        return df

    def calculate_end_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute end dates."""
        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = df['Start'] + pd.to_timedelta(df['Duration'], unit='D')
        return df