import pandas as pd
def test_simulate_delays():
    df = pd.DataFrame({'Duration': [10]})
    df_sim = simulate_delays(df.copy())
    assert df_sim['Duration'].iloc[0] > 0