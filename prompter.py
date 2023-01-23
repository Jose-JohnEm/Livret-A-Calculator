import pandas as pd
import plotly.express as px

CHART_TITLE = "Évolution de l'argent dans le Livret A"
X_CHART_LABEL = "Temps (en années)"
Y_CHART_LABEL = "Argent (en Euros €)"
Z_CHART_LABEL = "Année"


def from_dict_to_pd(data: dict) -> dict:
    keys = [i for i in range(1, len(data.keys()) + 1)]
    years = [i.split("/")[-1] for i in data.keys()]

    res = {
        X_CHART_LABEL: keys,
        Y_CHART_LABEL: data.values(),
        Z_CHART_LABEL: years
    }

    return res


def prompt_stats(pd_dict: dict):

    df = pd.DataFrame(pd_dict)
    fig = px.line(df,
                  x=X_CHART_LABEL,
                  y=Y_CHART_LABEL,
                  title=CHART_TITLE)
    fig.show()
