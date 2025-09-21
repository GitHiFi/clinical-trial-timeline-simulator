from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from .simulation import TimelineSimulator
from .config import AppConfig

class DelayPredictor:
    """Predicts delays using a machine learning model."""
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.historical_data = pd.read_csv('data/historical_delays.csv')
        self.train_model()

    def train_model(self):
        X = self.historical_data[['Phase']]  # One-hot encode phases
        y = self.historical_data['Delay']
        X = pd.get_dummies(X)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_delay(self, phase: str) -> float:
        X = pd.get_dummies(pd.DataFrame({'Phase': [phase]}))
        X = X.reindex(columns=self.model.feature_names_in_, fill_value=0)
        return self.model.predict(X)[0]

class MLDelaySimulator(TimelineSimulator):
    """Simulates delays using ML predictions."""
    def __init__(self):
        self.predictor = DelayPredictor()
        self.base_delays = AppConfig.get_delays()

    def simulate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply ML-predicted delays."""
        df['Duration'] = df['Duration'].astype(float)
        for phase in df['Phase']:
            if phase in self.base_delays:
                delay = self.predictor.predict_delay(phase)
                df.loc[df['Phase'] == phase, 'Duration'] += delay
        df['Duration'] = df['Duration'].clip(lower=1)
        return df