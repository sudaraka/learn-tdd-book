""" Deployment automation via fabric """

import random

from fabric.contrib.files import exists, sed, append
from fabric.api import env, run, local

REPO_URL = 'https://github.com/sudaraka/tddbook.git'


def deploy():
    """ Main function for deploying """

    site_dir = '/home/%s/sites/%s' % (env.user, env.host)
    source_dir = site_dir + '/source'

    _create_dirs_if_needed(site_dir)

    _get_latest_source(source_dir)

    _update_settings(source_dir, env.host)

    _update_virtualenv(source_dir)
    _update_static_files(source_dir)
    _update_databse(source_dir)


def _create_dirs_if_needed(site_dir):
    """ Create base directory structure if not exists """

    for directory in ('data', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_dir, directory))


def _get_latest_source(source_dir):
    """ Clone git repo or fetch the latest code from it """

    if exists(source_dir + '/.git'):
        run('cd %s && git fetch' % source_dir)
    else:
        run('git clone %s %s' % (REPO_URL, source_dir))

    current_commit = local('git log -n 1 --format=%H', capture=True)
    run('cd %s && git reset --hard %s' % (source_dir, current_commit))


def _update_settings(source_dir, site_name):
    """ Update settings file to work on server """

    settings_path = source_dir + '/app/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["%s"]' % site_name)

    secret_key_file = source_dir + '/app/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-='
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "%s"' % key)

    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_dir):
    """ Install dependencies in to the virtual environment """

    virtualenv_dir = source_dir + '/../virtualenv'

    if not exists(virtualenv_dir + '/bin/pip'):
        run('virtualenv --python=python3 %s' % virtualenv_dir)

    run('%s/bin/pip install -r %s/requirements.txt' %
        (virtualenv_dir, source_dir))


def _update_static_files(source_dir):
    """ populate static files """

    run('cd %s && ../virtualenv/bin/python3 manage.py collectstatic --noinput '
        % source_dir)


def _update_databse(source_dir):
    """ synchronize database """

    run('cd %s && ../virtualenv/bin/python3 manage.py syncdb --migrate' %
        source_dir)
