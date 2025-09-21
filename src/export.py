from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from plotly.io import to_image
import pandas as pd
from .visualization import Visualizer
from .config import AppConfig

def export_pdf(df: pd.DataFrame, filename: str = 'timeline_report.pdf'):
    """Export a PDF report with Gantt chart image and data."""
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    elements.append(Paragraph("Clinical Trial Timeline Report", style={'fontSize': 18, 'alignment': 1}))
    elements.append(Spacer(1, 12))
    visualizer = Visualizer(theme=AppConfig.get_visualization()['theme'])
    fig = visualizer.generate_gantt(df, output_file=None)
    fig.write_image('temp_gantt.png', format='png', scale=2)
    elements.append(Paragraph(f"<img src='temp_gantt.png' width='600'/>", style={'alignment': 1}))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total Duration: {(df['End'].max() - df['Start'].min()).days} days", style={}))
    doc.build(elements)
    print(f"PDF report saved to {filename}")

def export_csv(df: pd.DataFrame, filename: str = 'timeline_data.csv'):
    """Export simulated data to CSV."""
    df.to_csv(filename, index=False)
    print(f"CSV data saved to {filename}")