import time
import logging
from functools import wraps


def benchmark(mensaje):
    """
    Decorador para medir el tiempo de ejecución de una función.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            inicio = time.perf_counter()
            resultado = func(*args, **kwargs)
            fin = time.perf_counter()
            tiempo_transcurrido = (fin - inicio) * 1000
            if tiempo_transcurrido < 1:
                tiempo_formateado = f"{tiempo_transcurrido * 1000:.2f} ms"
            else:
                tiempo_formateado = f"{tiempo_transcurrido:.2f} s"
            logging.warning("%s - '%s' ejecutada en %s", mensaje,
                            func.__name__, tiempo_formateado)

            return resultado
        return wrapper
    return decorator
