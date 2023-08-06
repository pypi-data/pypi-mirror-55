"""
Command module allows executing ad hoc commands
"""
import os
import signal
import logging
import subprocess

from gradefast import logconfig

logger = logconfig.configure_and_get_logger(__name__)

class Command:
    """
    A runnable command

    A command in :class:`gradefast.test.GFCommandTest` gets executed to
    return a result, comment and exceptions.
    
    Alternatively, a command can be executed before or after a test runs
    like for moving student's code before execution and deleting it when
    test is done. 
    
    A long running command can be started before a test like a socket server
    that listens for input.

    Parameters
    ----------
    command_builder: function
        A function that gets called with submission, *args and **kwargs

    args: tuple, optional
        Arguments passed to command_builder

    kwargs: namedtuple, optional
        Named arguments passed to command_builder

    working_directory: str, optional
        Directory from where the command is executed

    long_running: bool, optional
        Is the function long running? Default is False

    timeout: float, optional 
        Seconds to wait before the process completes
    
    Attributes
    ----------
    command_builder: function

    long_running: bool

    cwd: str

    timeout: float

    args: tuple

    kwargs: namedtuple

    """
    def __init__(self, command_builder, *args, working_directory='.', long_running=False,
    timeout=None, **kwargs):
        self.command_builder = command_builder
        self.long_running = long_running
        self.cwd = working_directory
        self.timeout = timeout
        self.args = args
        self.kwargs = kwargs
    
    def build_command(self, submission):
        return self.command_builder(submission, *self.args, **self.kwargs)

    def run(self, submission):
        command = self.build_command(submission)
        if type(command) == str:
            shell = True
        elif type(command) == list:
            shell = False
        # command_str = command_str.split(" ")
        self.proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
        shell=shell, preexec_fn=os.setsid, cwd=self.cwd)
        out, err = None, None
        self.status = 'RUNNING'
        if not self.long_running:
            out, err = self.proc.communicate(timeout=self.timeout)
            self.status = 'FINISHED'
        
        if out != None:
            out = out.decode('utf-8')
        
        if err != None:
            err = err.decode('utf-8')

        return self.proc, out, err

    def kill(self):
        os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        out, errs = self.proc.communicate()
        return out, errs
