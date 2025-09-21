import plotly.express as px
import pandas as pd
from typing import Dict, Optional
from plotly.graph_objects import Figure
from datetime import timedelta
from .config import AppConfig

class Visualizer:
    """Class for generating visualizations with theme support."""
    def __init__(self, theme: str = None):
        config = AppConfig.get_visualization()
        self.theme = theme or config['theme']
        print(f"Applied theme: {self.theme}")  # Debug line
        self.colors: Dict[str, str] = config['colors']
        self.template = 'plotly_dark' if self.theme == 'dark' else 'plotly_white'

    def generate_gantt(self, df: pd.DataFrame, output_file: Optional[str] = 'timeline.html') -> Figure:
        """Create a professional, interactive Gantt chart and return the figure.
        
        Args:
            df (pd.DataFrame): DataFrame with 'Start', 'End', 'Phase', and 'Duration' columns.
            output_file (Optional[str]): Path to save the HTML file; if None, only return figure.
        
        Returns:
            Figure: The Plotly figure object.
        """
        # Optimized color palette for dark mode contrast
        colors = {
            'Protocol Design': '#6BAED6',    # Light blue for visibility
            'Recruitment': '#FF9F55',       # Orange with good contrast
            'Treatment': '#A1D99B',         # Light green
            'Follow-Up': '#FDB462',         # Light orange
            'Analysis': '#DADAEB'           # Light purple
        } if self.theme == 'dark' else {
            'Protocol Design': '#4C78A8',    # Original darker blue
            'Recruitment': '#FF6F61',       # Original red
            'Treatment': '#6BAED6',         # Original light blue
            'Follow-Up': '#98D8C6',         # Original teal
            'Analysis': '#D9A6B9'           # Original pink
        }
        
        fig = px.timeline(
            df, x_start='Start', x_end='End', y='Phase',
            title='Simulated Clinical Trial Timeline',
            hover_data={'Duration': ':.2f days'},
            color='Phase', color_discrete_map=colors
        )
        # Aesthetic enhancements with dark mode adjustments
        fig.update_traces(
            marker=dict(
                line=dict(width=2, color='#444' if self.theme == 'dark' else 'DarkSlateGrey')
            ),
            opacity=0.8  # Slight transparency for layering
        )
        fig.update_yaxes(
            autorange='reversed', title_text='', 
            tickfont=dict(size=14, family='Arial', color='#e0e0e0' if self.theme == 'dark' else '#333')
        )
        fig.update_xaxes(
            title_text='Timeline', 
            tickfont=dict(size=12, family='Arial', color='#e0e0e0' if self.theme == 'dark' else '#333'),
            showgrid=True, gridcolor='#444' if self.theme == 'dark' else '#ddd'
        )
        fig.update_layout(
            title=dict(
                font=dict(size=24, family='Arial', color='#e0e0e0' if self.theme == 'dark' else '#333'),
                x=0.5, xanchor='center'
            ),
            template=self.template,  # Rely on template for background
            height=600, width=1200,
            margin=dict(l=50, r=50, t=80, b=50),
            # Removed plot_bgcolor and paper_bgcolor to use template defaults
            font=dict(family='Arial', size=14, color='#e0e0e0' if self.theme == 'dark' else '#333'),
            showlegend=True, 
            legend=dict(
                orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1,
                font=dict(color='#e0e0e0' if self.theme == 'dark' else '#333')
            )
        )
        # Add annotations with better visibility in dark mode
        for i, row in df.iterrows():
            annotation_color = '#fff' if self.theme == 'dark' else '#000'
            fig.add_annotation(
                x=row['Start'] + timedelta(days=row['Duration']/2),
                y=row['Phase'], text=f"{row['Duration']:.1f}d",
                font=dict(size=12, color=annotation_color),
                bgcolor='rgba(0,0,0,0.5)' if self.theme == 'dark' else 'rgba(255,255,255,0.8)',  # Background for readability
                bordercolor='#fff' if self.theme == 'dark' else '#000',
                borderwidth=1,
                showarrow=False
            )
        if output_file:
            fig.write_html(output_file)
            print(f"Gantt chart saved to {output_file}")
        return fig