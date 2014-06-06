"""
Utlities for starting the server
"""

from __future__ import print_function

import daemon
import lockfile.pidlockfile
import os
import os.path
import subprocess

from mcserver import base

def start_server(path, is_daemon = False, uid = None, gid = None):
    """
    Start the server. Optionally start it as a daemon.
    """

    base._validate_server_path(path)

    settings = base.load_server_settings(path)

    jvm        = base._get_setting_jvm(settings)
    max_heap   = base._get_setting_max_heap(settings)
    max_stack  = base._get_setting_max_stack(settings)
    perm_gen   = base._get_setting_perm_gen(settings)
    jar        = base._get_setting_jar(settings)
    extra_args = base._get_extra_start_args(settings)

    command = '{jvm} -Xmx{heap} -Xms{stack} -XX:MaxPermSize={perm_gen} -jar {jar} {args}'.format(
        jvm      = jvm,
            heap     = max_heap,
            stack    = max_stack,
            perm_gen = perm_gen,
            jar      = os.path.join(path, jar) if not is_daemon else jar,
            args     = extra_args,
        )

    base.LOGGER.info('Starting server...')
    base.LOGGER.debug('Starting server with `{0}`'.format(command))

    if not is_daemon:
        if uid != None:
            base.LOGGER.warn('User option is ignored when not running as a daemon')
            uid = None
        if gid != None:
            base.LOGGER.warn('Group option is ignored when not running as a daemon')
            gid = None

    if is_daemon:
        base.LOGGER.debug(
            'Starting daemon process with user and group: {user}, {group}'.format(
                user  = uid,
                group = gid,
            )
        )

        pidfile = os.path.abspath(base._get_pidfile(path))
        if not os.path.exists(pidfile):
            open(pidfile, 'w').close()

        with daemon.DaemonContext(
            gid               = gid,
            pidfile           = lockfile.pidlockfile.PIDLockFile(pidfile),
            prevent_core      = True,
            uid               = uid,
            working_directory = path,
        ) as daemon_context:
            process = subprocess.Popen(command, shell = True)
            process.communicate()
    else:
        process = subprocess.Popen(command, shell = True)

        process.wait()
