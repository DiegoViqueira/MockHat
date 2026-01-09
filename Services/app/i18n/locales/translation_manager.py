import gettext
import logging
import os
from fastapi import Request


class TranslationManager:
    """
    Handles translations for the application.
    """

    def __init__(self, lang: str):
        self.lang = lang
        self._load_translation(lang)

    def _load_translation(self, lang: str) -> bool:
        """
        Carga los archivos de traducción para el idioma especificado.
        Retorna True si se cargó correctamente, False si hubo un error.
        """
        localedir = "app/i18n/locales"

        # Verificar si existe el directorio de traducciones
        if not os.path.exists(localedir):
            logging.error(
                "ADVERTENCIA: El directorio de traducciones %s no existe.", localedir)
            self.translation_loaded = False
            self.gettext = gettext.NullTranslations()
            return False

        # Verificar si existe el archivo de traducción para este idioma
        mo_path = os.path.join(localedir, lang, 'LC_MESSAGES', 'messages.mo')
        if not os.path.exists(mo_path):
            logging.error(
                "ADVERTENCIA: No se encontró el archivo de traducción para %s en %s.", lang, mo_path)

        try:
            self.gettext = gettext.translation(
                "messages", localedir=localedir, languages=[lang], fallback=True)
            self.gettext.install()
            self.translation_loaded = True
            return True
        except Exception as e:
            logging.error(
                "ERROR: No se pudieron cargar las traducciones para %s: %s", lang, str(e))
            self.gettext = gettext.NullTranslations()
            self.translation_loaded = False
            return False

    def get_lang_from_request(self, request: Request) -> str:
        """
        Obtiene el idioma del encabezado de la solicitud.
        """
        return request.headers.get('Accept-Language', 'en').split('-')[0].lower()

    def translate(self, message: str) -> str:
        """
        Translates a message to the current language.
        """
        return self.gettext.gettext(message)

    def set_language(self, lang: str):
        """
        Sets the language for the translation manager.
        """
        self.lang = lang
        self._load_translation(lang)

    def is_translation_loaded(self) -> bool:
        """
        Retorna True si las traducciones se cargaron correctamente.
        """
        return self.translation_loaded
