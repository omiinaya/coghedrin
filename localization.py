# Simple localization demo for Coghedrin
LOCALES = {
    'en': {
        'pong': 'Pong!',
        'roll': '{user}, you rolled a {number}',
        'invalid_condition': "Invalid condition. Please choose from 'day', 'night', 'normal', or 'rain'.",
    },
    'es': {
        'pong': '¡Pong!',
        'roll': '{user}, sacaste un {number}',
        'invalid_condition': "Condición inválida. Elija entre 'día', 'noche', 'normal' o 'lluvia'.",
    }
}

def t(key, lang='en', **kwargs):
    """Translate a key to the given language."""
    template = LOCALES.get(lang, LOCALES['en']).get(key, key)
    return template.format(**kwargs)
