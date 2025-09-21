# Clinical Trial Timeline Simulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple Python tool to simulate clinical trial phases with random delays, generating interactive Gantt charts. Built to demonstrate skills in data simulation (numpy), processing (pandas), and visualization (Plotly), with relevance to ICH GCP timelines and clinical research planning.

## Motivation
As a Biomedical & Software Engineering graduate, I created this to bridge my experience in clinical data management and software development. It simulates real-world uncertainties in trials, like enrollment delays, without using real data—aligning with GCP ethics.

## Features
- Input: CSV with trial phases, start dates, and durations.
- Simulation: Adds random delays (e.g., normal distribution) to model risks.
- Output: Interactive HTML Gantt chart with hover details.
- Optional: Flask web app for easy uploads and viewing.
- GCP Tie-in: Flags if simulated timeline exceeds typical caps (e.g., 18 months for Phase II).

## Demo
<!-- ![Gantt Chart Example](docs/example_gantt.png) -->

Run the script with the sample CSV to generate `timeline.html`.

## Installation
```bash
git clone https://github.com/GitHiFi/clinical-trial-timeline-simulator.git
cd clinical-trial-timeline-simulator
pip install -r requirements.txt