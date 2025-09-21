from flask_socketio import SocketIO, emit
from .simulation import ClinicalTrialSimulator
from .visualization import Visualizer
import pandas as pd
from .config import AppConfig

socketio = SocketIO()

class CollaborationManager:
    """Manages real-time collaboration for timeline updates."""
    def __init__(self):
        self.clients = {}
        self.df = None

    def initialize(self, app):
        socketio.init_app(app, cors_allowed_origins="*")
        @socketio.on('update_delay')
        def handle_update_delay(data):
            phase = data['phase']
            delay = data['delay']
            if self.df is not None:
                self.df.loc[self.df['Phase'] == phase, 'Duration'] += delay
                self.df = ClinicalTrialSimulator().calculate_end_dates(self.df)
                visualizer = Visualizer(theme=AppConfig.get_visualization()['theme'])
                fig = visualizer.generate_gantt(self.df, output_file=None)
                plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
                emit('update_chart', {'plot': plot_html}, broadcast=True)
        @socketio.on('connect')
        def handle_connect():
            self.clients[request.sid] = True
            emit('user_count', len(self.clients))
        @socketio.on('disconnect')
        def handle_disconnect():
            del self.clients[request.sid]
            emit('user_count', len(self.clients), broadcast=True)