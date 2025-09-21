from flask import Flask, request, render_template, url_for
import pandas as pd
from io import StringIO
from .simulation import ClinicalTrialSimulator, HistoricalDelaySimulator, MLDelaySimulator
from .visualization import Visualizer
from .gcp import GCPComplianceChecker
from .export import export_pdf, export_csv
from .collaboration import CollaborationManager, socketio
from .config import AppConfig
from .deployment import configure_deployment

app = Flask(__name__, template_folder='../templates', static_folder='../static')
AppConfig.load()
collaboration = CollaborationManager()
collaboration.initialize(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    plot_html = ''
    gcp_flags = ''
    theme = request.args.get('theme', AppConfig.get_visualization()['theme'])
    simulator_type = request.args.get('simulator', 'default')  # default, historical, ml
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                df = pd.read_csv(StringIO(file.read().decode('utf-8')))
                if simulator_type == 'historical':
                    simulator = HistoricalDelaySimulator()
                elif simulator_type == 'ml':
                    simulator = MLDelaySimulator()
                else:
                    simulator = ClinicalTrialSimulator()
                df = simulator.simulate(df)
                df = simulator.calculate_end_dates(df)
                collaboration.df = df  # Share with collaboration
                visualizer = Visualizer(theme=theme)
                fig = visualizer.generate_gantt(df, output_file=None)
                plot_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
                checker = GCPComplianceChecker()
                gcp_flags = checker.check_flags(df)
                export_pdf(df)
                export_csv(df)
            except Exception as e:
                return render_template('index.html', error=str(e), theme=theme)
    return render_template('index.html', plot=plot_html, gcp_flags=gcp_flags, theme=theme)

if __name__ == '__main__':
    configure_deployment(app)