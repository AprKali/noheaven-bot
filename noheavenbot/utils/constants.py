import os

import logging
from typing import NamedTuple
from pathlib import PurePath


class _TextChannels:
    def get(self, attr_name: str):
        return self.__getattribute__(attr_name)


class _TrustedBotIds:
    def get(self, attr_name: str):
        return self.__getattribute__(attr_name)


TEXTCHANNELS = _TextChannels()
TRUSTED_BOTS = _TrustedBotIds()


class Fields(NamedTuple):
    help_fields = (

        ('__**Admins**__', 'Commands only avaliable for admins'),
        ('!reset', 'resets the bots, only admins can do that'),
        ('!perms <user>', 'Shows the optional <users> permissions, ctx.author by default'),
        ('!d <number>', 'Deletes <number> messages from the channel'),
        ('!reload', 'Reloads cogs'),
        ('!garch delete <indice>', 'Borra el nombre de garch de ese indice, los indices empiezan en 0'),
        ('__**Users**__', 'Commands avaliable for every user'),
        ('!info <user>', 'Shows <users> info'),
        ('!ping', 'echo PONG'),
        ('__**Nsfw**__', 'nsfw commands avaliable for every user'),
        ('!porn <argument>', 'Sends an image of <argument> category'),
        ('!porn list', 'Shows possible <argument>'),
        ('!gif <argument>', 'Sends a gif of <argument> category'),
        ('!gif list', 'Shows possible <argument>'),
        ('!lol <argument', 'SEnds an image of <argument> category'),
        ('!lol list', 'Shows possible <argument>'),
        ('__**Garch**__', 'Garch commands'),
        ('!garch', 'Shows a random garch name'),
        ('!garch save <name>', 'Saves new garch name'),
        ('!garch list', 'Shows the saved list'),
        ('!music', 'Shows you the music options'),
        ('!text <texto - >', 'Transforms <texto> in emoji text'),
        ('!beaten <destructor> <vencido1> <vencido2>', 'Shows your enemies who the boss is')
    )

    music_fields = (

        ('!music', 'muestra este mensaje'),
        ('!play <canción>', 'Toca la <canción>'),
        ('!skip', 'Salta a la siguiente canción, si no hay ninguna espera 60 segundos'),
        ('!stop', 'Cierra el bot'),
        ('!pause', 'La música se pausa'),
        ('!resume', 'La musica continua'),
        ('!volumen', 'Te dice el volumen actual'),
        ('!volumen <numero>', 'Cambia el volumen global a <numero> 0-100'),
        ('!join', 'Mueve el bot a tu canal (No necesario hacerlo, play lo hace automaticamente'),
        ('!playlist', 'Te muestra las 5 primeras playlists que existen, con 3 canciones cada una'),
        ('!playlist p <nombredeplaylist> <r>', 'Empieza a tocar la playlist, si añades la opcion "r", la toca random.'),
        ('!playlist make <nombre>', 'Crea una playlist con <nombre> nombre.'),
        ('!playlist add <nombre> <cancion>', 'Añade la canción <cancion> a la playlist <nombre>'),
        ('!playlist del <nombre>', 'borra la playlist <nombre>'),
        ('!playlist dels <nombre> <cancion>', 'Borra la canción <cancion> de la playlist <nombre>'),
        ('!temp', 'Te muestra la lista temporal actual, esta se crea con las canciones que tocas con !play'),
        ('!temp copy <nombre>', 'Crea una playlist <nombre> con las canciones de la playlsit temporal'),
        ('!temp d <índice>', 'Borra el la canción que esta en el <indice> Nota: Los indices empiezan en 0'),
        ('**Información adicional**', 'El bot tiene un timeout de 60 segundos, si en 60 segundos no toca musica,'
                                      'se sale del canal'),
    )

    nsfw_categories = [

        'amateur', 'anal', 'asian', 'ass', 'babes', 'bbw', 'bdsm', 'big', 'tits', 'blonde', 'blowjob',
        'brunette', 'celebrity', 'college', 'creampie', 'cumshots', 'double', 'penetration', 'ebony',
        'emo', 'female-ejaculation', 'fisting', 'footjob', 'gangbang', 'gay', 'girlfriend', 'group',
        'sex', 'hairy', 'handjob', 'hardcore', 'hentai', 'indian', 'interracial', 'latina', 'lesbian',
        'lingerie', 'masturbation', 'mature', 'milf', 'non-nude', 'panties', 'penis', 'pornstar', 'public',
        'sex', 'pussy', 'redhead', 'self', 'shot', 'shemale', 'teen', '(18+)', 'threesome', 'toys'
    ]

    nsfw_lol = [
        'ahri', 'akali', 'anivia', 'annie', 'ashe', 'caitlyn',
        'camille', 'cassiopeia', 'diana', 'elise', 'evelynn',
        'fiora', "kai'sa", 'kalista', 'karma', 'katarina',
        'kayle', 'kindred', 'leblanc', 'leona', 'lissandra',
        'lulu', 'lux', 'missfortune', 'morgana', 'nami', 'nidalee',
        'oriana', 'poppy', 'quinn', "rek'sai", 'riven', 'sejuani',
        'shyvana', 'sivir', 'sona', 'soraka', 'syndra', 'taliyah',
        'tristana', 'vayne', 'vi', 'xayah', 'zoe', 'zyra', 'group',
        'cosplay', 'genderbender', 'male', 'irelia', 'jinx', 'random or r'
    ]

    nsfw_conversion = {
        'conversion_index': ['taliyah', 'camille', "kai'sa", "rek'sai", 'zoe', 'xayah'],
        'taliyah': '360-taliyah',
        'camille': '363-camille',
        "kai'sa": '374-kai_sa',
        "rek'sai": '256-rek_sai',
        'zoe': '373-zoe',
        'xayah': '370-xayah'
    }


class Path(NamedTuple):
    UTILS_FOLDER = str(PurePath(__file__).parent)
    _ROOT_FOLDER = UTILS_FOLDER.replace('utils', '')

    COGS_FOLDER = f'{_ROOT_FOLDER}cogs/'
    DOTENV_FOLDER = UTILS_FOLDER + '/.env'
    COMMANDS_FOLDER = f'{COGS_FOLDER}commands/'
    EVENTS_FOLDER = f'{COGS_FOLDER}events/'
    ASSETS_FOLDER = f'{_ROOT_FOLDER}assets/'
    IMGS_FOLDER = f'{ASSETS_FOLDER}imgs/'


class EnvVariables(NamedTuple):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ModuleNotFoundError:
        logging.warning('dotenv not installed')

    # try:
    #     debug_mode = True if os.environ['DEBUG_MODE'] == 'True' else False
    # except KeyError:
    #     logging.warning('are env variables set?')
    #     debug_mode = False

    @classmethod
    def get(cls, name: str) -> str:
        env_var = ''
        try:
            env_var = os.environ[name]
        except KeyError:
            logging.warning(f' Are .env variables set? could not get "{name}" variable')
        return env_var
