import pandas as pd
from typing import List
from .config import AppConfig

class GCPComplianceChecker:
    """Class for GCP compliance checks, expandable for more rules."""
    def __init__(self):
        config = AppConfig.get_gcp()
        self.total_cap: int = config['total_cap_days']
        self.phase_ii_cap: int = config['phase_ii_cap_days']
        self.phase_ii_phases: List[str] = config['phase_ii_phases']
        self.phase_caps = {
            'Phase I': 180, 'Phase II': 540, 'Phase III': 1080  # Days, customizable in config
        }

    def check_flags(self, df: pd.DataFrame) -> str:
        """Perform detailed GCP checks and return formatted warnings."""
        total_days = (df['End'].max() - df['Start'].min()).days
        phase_ii_days = df[df['Phase'].isin(self.phase_ii_phases)]['Duration'].sum()
        warnings = []
        if total_days > self.total_cap:
            warnings.append(f"Warning: Total timeline exceeds {self.total_cap//30} months ({total_days} days).")
        if phase_ii_days > self.phase_ii_cap:
            warnings.append(f"Warning: Phase II exceeds cap ({phase_ii_days} days > {self.phase_ii_cap} days).")
        for phase, cap in self.phase_caps.items():
            phase_days = df[df['Phase'].str.contains(phase, na=False)]['Duration'].sum()
            if phase_days > cap:
                warnings.append(f"Warning: {phase} exceeds cap ({phase_days} days > {cap} days).")
        return "\n".join(warnings) or "No GCP flags."