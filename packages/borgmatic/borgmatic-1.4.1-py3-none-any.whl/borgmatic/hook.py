import logging
import os

import requests

from borgmatic import execute

logger = logging.getLogger(__name__)


def interpolate_context(command, context):
    '''
    Given a single hook command and a dict of context names/values, interpolate the values by
    "{name}" into the command and return the result.
    '''
    for name, value in context.items():
        command = command.replace('{%s}' % name, str(value))

    return command


def execute_hook(commands, umask, config_filename, description, dry_run, **context):
    '''
    Given a list of hook commands to execute, a umask to execute with (or None), a config filename,
    a hook description, and whether this is a dry run, run the given commands. Or, don't run them
    if this is a dry run.

    The context contains optional values interpolated by name into the hook commands. Currently,
    this only applies to the on_error hook.

    Raise ValueError if the umask cannot be parsed.
    Raise subprocesses.CalledProcessError if an error occurs in a hook.
    '''
    if not commands:
        logger.debug('{}: No commands to run for {} hook'.format(config_filename, description))
        return

    dry_run_label = ' (dry run; not actually running hooks)' if dry_run else ''

    context['configuration_filename'] = config_filename
    commands = [interpolate_context(command, context) for command in commands]

    if len(commands) == 1:
        logger.info(
            '{}: Running command for {} hook{}'.format(config_filename, description, dry_run_label)
        )
    else:
        logger.info(
            '{}: Running {} commands for {} hook{}'.format(
                config_filename, len(commands), description, dry_run_label
            )
        )

    if umask:
        parsed_umask = int(str(umask), 8)
        logger.debug('{}: Set hook umask to {}'.format(config_filename, oct(parsed_umask)))
        original_umask = os.umask(parsed_umask)
    else:
        original_umask = None

    try:
        for command in commands:
            if not dry_run:
                execute.execute_command(
                    [command],
                    output_log_level=logging.ERROR
                    if description == 'on-error'
                    else logging.WARNING,
                    shell=True,
                )
    finally:
        if original_umask:
            os.umask(original_umask)


def ping_healthchecks(ping_url_or_uuid, config_filename, dry_run, append=None):
    '''
    Ping the given healthchecks.io URL or UUID, appending the append string if any. Use the given
    configuration filename in any log entries. If this is a dry run, then don't actually ping
    anything.
    '''
    if not ping_url_or_uuid:
        logger.debug('{}: No healthchecks hook set'.format(config_filename))
        return

    ping_url = (
        ping_url_or_uuid
        if ping_url_or_uuid.startswith('http')
        else 'https://hc-ping.com/{}'.format(ping_url_or_uuid)
    )
    dry_run_label = ' (dry run; not actually pinging)' if dry_run else ''

    if append:
        ping_url = '{}/{}'.format(ping_url, append)

    logger.info(
        '{}: Pinging healthchecks.io{}{}'.format(
            config_filename, ' ' + append if append else '', dry_run_label
        )
    )
    logger.debug('{}: Using healthchecks.io ping URL {}'.format(config_filename, ping_url))

    logging.getLogger('urllib3').setLevel(logging.ERROR)
    requests.get(ping_url)
