import os
import sys
import platform
import threading

import pymel.core as pmc
import maya.utils

from email.mime.text import MIMEText
import smtplib


# directory where this file is located, used to detect exception in our library
LIB_DIR = _normalize(os.path.dirname(__file__))
EMAIL_ADDR = 'dalvarez@yourdomain.com' # Your email here
EMAIL_SERVER = 'smtp.yourdomain.com' # Your email server here 


def _collect_info():
    lines = []
    lines.append('Scene Info')
    lines.append('  Maya Scene: ' + pmc.sceneName())

    lines.append('Maya/Python Info')
    lines.append('  Maya Version: ' + pmc.about(version=True))
    lines.append('  Qt Version: ' + pmc.about(qtVersion=True))
    lines.append('  Maya64: ' + str(pmc.about(is64=True)))
    lines.append('  PyVersion: ' + sys.version)
    lines.append('  PyExe: ' + sys.executable)

    lines.append('Machine Info')
    lines.append('  OS: ' + pmc.about(os=True))
    lines.append('  Node: ' + platform.node())
    lines.append('  OSRelease: ' + platform.release())
    lines.append('  OSVersion: ' + platform.version())
    lines.append('  Machine: ' + platform.machine())
    lines.append('  Processor: ' + platform.processor())

    lines.append('Environment Info')
    lines.append('  EnvVars')
    for k in sorted(os.environ.keys()):
        lines.append('    %s: %s' % (k, os.environ[k]))
    lines.append('  SysPath')
    for p in sys.path:
        lines.append('    ' + p)
    return lines

def _normalize(p):
    return os.path.normpath(os.path.abspath(p))



def _send_email(body):
    msg = MIMEText(body)
    msg['To'] = EMAIL_ADDR
    msg['From'] = EMAIL_ADDR
    msg['Subject'] = 'Maya Tools Error'
    server = smtplib.SMTP(EMAIL_SERVER)
    try:
        server.sendmail(msg['From'], msg['To'], msg.as_string())
    finally:
        server.quit()

def _send_email_in_background(body):
    t = threading.Thread(
        target=_send_email, args=(body,),
        name='send_email_in_background')
    t.start()

def _handle_our_exc(etype, evalue, tb, detail):
    s = maya.utils._formatGuiException(etype, evalue, tb, detail)
    body = [s]
    body.extend(_collect_info())
    _send_email_in_background('\n'.join(body))
    lines = [
        s,
        'An unhandled exception occurred.',
        'An error report was automatically sent to ',
        EMAIL_ADDR + ' with details about the error. ',
        'You should get a followup response in three days '
        'or less.']
    return '\n'.join(lines)

def _is_important_tb(tb):
    while tb:
        codepath = tb.tb_frame.f_code.co_filename
        if _normalize(codepath).startswith(LIB_DIR):
            return True
        tb = tb.tb_next
    return False

_orig_excepthook = maya.utils.formatGuiException

def excepthook(etype, evalue, tb, detail=2):
    result = _orig_excepthook(etype, evalue, tb, detail)
    if _is_important_tb(tb):
        result = _handle_our_exc(etype, evalue, tb, detail)
    return result


maya.utils.formatGuiException = excepthook