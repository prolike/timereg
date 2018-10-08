from . import shared
import subprocess, logging


settings = {} # keeps settings in memory while current call is being executed if setting is needed multiple times
default = {'autopush': 'True'} #default settings used if settings can not be found in git comfig

def run_setup():
    set_setting('autopush', True)

def set_setting(setting, enable):
    settings[setting] = enable
    call = shared.git_prefix() + ['config', '--global', 'timereg.' + setting, str(enable)]
    p = subprocess.run(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')


def get_setting(setting):
    if setting in settings:
        return settings[setting]
    call = shared.git_prefix() + ['config', 'timereg.' + setting]
    p = subprocess.run(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    if len(p.stdout) > 0:
        return p.stdout.rstrip()
    else:
        return default_settings(setting)

def default_settings(setting):
    settings[setting] = default[setting]
    return default[setting]
