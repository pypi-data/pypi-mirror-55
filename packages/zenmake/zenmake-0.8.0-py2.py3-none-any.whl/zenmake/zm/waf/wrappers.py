# coding=utf-8
#

"""
 Copyright (c) 2019, Alexander Magola. All rights reserved.
 license: BSD 3-Clause License, see LICENSE for more details.
"""

import os
import sys
import subprocess

from waflib import Options, Context, Configure, Scripting, Utils
from waflib.ConfigSet import ConfigSet
from zm import log, assist, utils
from zm.pyutils import stringtype
from zm.pypkg import PkgPath

joinpath = os.path.join

# Force to turn off internal WAF autoconfigure decorator.
# It's just to rid of needless work and to save working time.
Configure.autoconfig = False

def _areBuildTypesNotConfigured(clicmd, bconfHandler):
    buildconf = bconfHandler.conf
    buildtype = clicmd.args.buildtype
    zmcachedir = bconfHandler.confPaths.zmcachedir
    for taskName in buildconf.tasks:
        taskVariant = assist.makeTaskVariantName(buildtype, taskName)
        fname = assist.makeCacheConfFileName(zmcachedir, taskVariant)
        if not os.path.exists(fname):
            return True
    return False

def _loadLockfileEnv(bconfPaths):
    env = ConfigSet()
    try:
        env.load(joinpath(bconfPaths.wscriptout, Options.lockfile))
    except EnvironmentError:
        return None
    return env

def _handleNoLockInTop(ctx, envGetter):

    if Context.top_dir and Context.out_dir:
        return False

    env = envGetter()
    if not env:
        if ctx.cmd != 'build':
            return True
        from zm.error import ZenMakeError
        raise ZenMakeError('The project was not configured: run "configure" '
                           'first or enable features.autoconfig in buildconf !')

    Context.run_dir = env.run_dir
    Context.top_dir = env.top_dir
    Context.out_dir = env.out_dir

    # It's needed to rerun command to apply changes in Context otherwise
    # Waf won't work correctly.
    Scripting.run_command(ctx.cmd)
    return True

def wrapBldCtxNoLockInTop(bconfHandler, method):
    """
    Decorator that handles only case with conf.env.NO_LOCK_IN_RUN = True and/or
    conf.env.NO_LOCK_IN_TOP = True
    """

    def execute(self):
        bconfPaths = bconfHandler.confPaths
        if not _handleNoLockInTop(self, lambda: _loadLockfileEnv(bconfPaths)):
            method(self)

    return execute

def wrapBldCtxAutoConf(clicmd, bconfHandler, method):
    """
    Decorator that enables context commands to run *configure* as needed.
    It handles also case with conf.env.NO_LOCK_IN_RUN = True and/or
    conf.env.NO_LOCK_IN_TOP = True
    """

    def runConfigAndCommand(self, env):
        Scripting.run_command(env.config_cmd or 'configure')
        Scripting.run_command(self.cmd)

    def execute(self):

        wrapBldCtxAutoConf.callCounter += 1
        if wrapBldCtxAutoConf.callCounter > 10:
            # I some cases due to programming error, user actions or system
            # problems we can get infinite call of current function. Maybe
            # later I'll think up better protection but in normal case
            # it shouldn't happen.
            raise Exception('Infinite recursion was detected')

        if wrapBldCtxAutoConf.onlyRunMethod:
            method(self)
            # reset flag
            wrapBldCtxAutoConf.onlyRunMethod = False
            return

        bconfPaths = bconfHandler.confPaths

        # Execute the configuration automatically
        autoconfig = bconfHandler.conf.features['autoconfig']

        if not autoconfig:
            if not _handleNoLockInTop(self, lambda: _loadLockfileEnv(bconfPaths)):
                method(self)
            return

        # mark for the next recursive call
        # FIXME: can be more stable solution?
        wrapBldCtxAutoConf.onlyRunMethod = True

        env = _loadLockfileEnv(bconfPaths)
        if not env:
            log.warn('Configuring the project')
            runConfigAndCommand(self, ConfigSet())
            return

        if env.run_dir != bconfPaths.wscriptdir:
            runConfigAndCommand(self, env)
            return

        cmnConfSet = assist.loadZenMakeCmnConfSet(bconfPaths)
        if not cmnConfSet or assist.isZmVersionChanged(cmnConfSet) or \
                    assist.areMonitoredFilesChanged(cmnConfSet) or \
                    assist.areToolchainEnvVarsAreChanged(cmnConfSet):
            runConfigAndCommand(self, env)
            return

        if _areBuildTypesNotConfigured(clicmd, bconfHandler):
            runConfigAndCommand(self, env)
            return

        if not _handleNoLockInTop(self, lambda: env):
            method(self)
        return

    return execute

wrapBldCtxAutoConf.callCounter = 0
wrapBldCtxAutoConf.onlyRunMethod = False

def wrapUtilsGetProcess(_):
    """
    Wrap Utils.get_process to have possibility of running from a zip package.
    """

    from zm import WAF_DIR
    filepath = joinpath(WAF_DIR, 'waflib', 'processor.py')
    # it must be text
    code = PkgPath(filepath).readText()

    def execute():
        if Utils.process_pool:
            return Utils.process_pool.pop()

        cmd = [sys.executable, '-c', code]
        return subprocess.Popen(cmd, stdout = subprocess.PIPE,
                                stdin = subprocess.PIPE, bufsize = 0)

    return execute

def getFileExtensions(src):
    """
	Returns the file extensions for the list of files given as input

	:param src: files to process
	:list src: list of string or :py:class:`waflib.Node.Node`
	:return: list of file extensions
	:rtype: set of strings
	"""

    # This implementation gives more optimal result for using in
    # waflib.Tools.c_aliases.sniff_features

    ret = set()
    for path in utils.toList(src):
        if not isinstance(path, stringtype):
            path = path.name
        ret.add(path[path.rfind('.') + 1:])
    return ret

def setupAll(cmd, bconfHandler):
    """ Setup all wrappers for Waf """

    Utils.get_process = wrapUtilsGetProcess(Utils.get_process)

    from waflib import Build

    Build.BuildContext.execute = wrapBldCtxAutoConf(cmd, bconfHandler,
                                                    Build.BuildContext.execute)
    for ctxCls in (Build.CleanContext, Build.ListContext):
        ctxCls.execute = wrapBldCtxNoLockInTop(bconfHandler, ctxCls.execute)

    from waflib.Tools import c_aliases
    c_aliases.get_extensions = getFileExtensions
