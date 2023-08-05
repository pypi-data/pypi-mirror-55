import os
import signal


# noinspection PyUnusedLocal
def _handle_signal(signal_number, frame):
    """
    Send the signal to all processes in runrestic's process group, which includes child process.
    """
    os.killpg(os.getpgrp(), signal_number)


def configure_signals():  # pragma: no cover
    """
    Configure runrestic's signal handlers to pass relevant signals through to any child processes
    like Restic. Note that SIGINT gets passed through even without these changes.
    """
    for signal_number in (
        signal.SIGHUP,
        signal.SIGTERM,
        signal.SIGUSR1,
        signal.SIGUSR2,
    ):
        signal.signal(signal_number, _handle_signal)
