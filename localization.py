# Simple localization demo for Coghedrin
LOCALES = {
    'en': {
        'pong': 'Pong!',
        'roll': '{user}, you rolled a {number}',
        'invalid_condition': "Invalid condition. Please choose from 'day', 'night', 'normal', or 'rain'.",
        'balding_percent': '{user} is {percent}% balding. o7',
        'balding_none': "Congratz! You're not balding.",
        'coinflip_specify': "Please specify either 'even' or 'odd'.",
        'coinflip_win': 'You won! ({result})',
        'coinflip_lose': 'You lost. ({result})',
        'coinflip_error': 'Error in coinflip command: {error}',
    },
    'es': {
        'pong': '¡Pong!',
        'roll': '{user}, sacaste un {number}',
        'invalid_condition': "Condición inválida. Elija entre 'día', 'noche', 'normal' o 'lluvia'.",
        'balding_percent': '{user} tiene {percent}% de calvicie. o7',
        'balding_none': "¡Felicidades! No tienes calvicie.",
        'coinflip_specify': "Por favor especifica 'par' o 'impar'.",
        'coinflip_win': '¡Ganaste! ({result})',
        'coinflip_lose': 'Perdiste. ({result})',
        'coinflip_error': 'Error en el comando lanzar moneda: {error}',
    }
}

def t(key, lang='en', **kwargs):
    """Translate a key to the given language."""
    template = LOCALES.get(lang, LOCALES['en']).get(key, key)
    return template.format(**kwargs)
