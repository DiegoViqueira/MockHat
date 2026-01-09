import json
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, cohen_kappa_score

# Función para calcular ±1 Accuracy


def plus_minus_one_accuracy(y_true, y_pred):
    """Calculate the plus/minus one accuracy."""
    return np.mean(np.abs(np.array(y_true) - np.array(y_pred)) <= 1)


# Cargar archivo JSON
with open("tools/db_data/evaluation_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

criterios = list(data.keys())
modelos = list(data["Content"].keys())
modelos.remove("Profesor")
metricas = ["QWK", "Exact Match", "±1 Accuracy", "MAE"]

# Preparar estructura para resultados
results = {metrica: pd.DataFrame(
    index=criterios, columns=modelos) for metrica in metricas}

# Calcular métricas por criterio y modelo
for criterio in criterios:
    y_true = data[criterio]["Profesor"]
    for modelo in modelos:
        y_pred = data[criterio][modelo]
        results["QWK"].loc[criterio, modelo] = cohen_kappa_score(
            y_true, y_pred, weights="quadratic")
        results["Exact Match"].loc[criterio, modelo] = np.mean(
            np.array(y_true) == np.array(y_pred))
        results["±1 Accuracy"].loc[criterio,
                                   modelo] = plus_minus_one_accuracy(y_true, y_pred)
        results["MAE"].loc[criterio, modelo] = mean_absolute_error(
            y_true, y_pred)

# Exportar a CSV
output = pd.concat(results, names=["Métrica", "Criterio"])
output.to_csv("tools/db_data/evaluation_data_metrics.csv")
print("Exportado a 'evaluation_data_metrics.csv'")
