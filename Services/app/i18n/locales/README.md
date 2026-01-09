# Internacionalización (i18n)

Este directorio contiene los archivos de traducción para la internacionalización de la aplicación.

## Estructura de directorios

```
locales/
├── en/
│   ├── LC_MESSAGES/
│   │   └── messages.po # Archivo de traducción en formato PO
│   │   └── messages.mo # Archivo de traducción compilado en formato MO
├── es/
│   ├── LC_MESSAGES/
│   │   └── messages.po # Archivo de traducción en formato PO
│   │   └── messages.mo # Archivo de traducción compilado en formato MO
```

## Flujo de trabajo para añadir/actualizar traducciones

1. **Inicializar un nuevo idioma** (solo la primera vez para cada idioma):

   ```bash
   python tools/i18n_tools.py init es  # Para español
   python tools/i18n_tools.py init en  # Para inglés
   ```

2. **Editar los archivos .po** con las traducciones:

   - Abre el archivo .po del idioma correspondiente (ej. `locales/en/LC_MESSAGES/messages.po`)
   - Traduce las cadenas en el campo `msgstr` para cada entrada `msgid`

3. **Compilar las traducciones** para generar los archivos .mo:

   ```bash
   python tools/i18n_tools.py compile
   ```

## Uso en el código
