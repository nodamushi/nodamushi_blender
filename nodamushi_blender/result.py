FINISHED = {'FINISHED'}
CANCELLED = {'CANCELLED'}
PASS_THROUGH = {'PASS_THROUGH'}
RUNNING_MODAL = {"RUNNING_MODAL"}

# report
DEBUG = {'DEBUG'}
INFO = {'INFO'}
OPERATOR = {'OPERATOR'}
PROPERTY = {'PROPERTY'}
WARNING = {'WARNING'}
ERROR = {'ERROR'}
ERROR_INVALID_INPUT = {'ERROR_INVALID_INPUT'}
ERROR_INVALID_CONTEXT = {'ERROR_INVALID_CONTEXT'}
ERROR_OUT_OF_MEMORY = {'ERROR_OUT_OF_MEMORY'}

class Result:
  _ok: bool
  _cancel: bool
  _debug: str | None
  _info: str | None
  _warn: str | None
  _err: str | None

  def __init__(self, ok: bool, cancel: bool, debug: str|None, info: str | None, warn: str | None, error: str | None) -> None:
    self._ok = not cancel and ok
    self._cancel = cancel
    self._debug = debug
    self._info = info
    self._warn = warn
    self._err = error

  def setOK(self):
    self._ok = True
    self._cancel = False

  def setError(self):
    self._ok = False
    self._cancel = False

  def setCancel(self):
    self._ok = False
    self._cancel = True

  def get(self):
    if self._cancel:
      return CANCELLED
    return FINISHED

  def report(self, target):
    if self._debug:
      target.report(DEBUG, self._debug)
    if self._info:
      target.report(INFO, self._info)
    if self._warn:
      target.report(WARNING, self._warn)
    if self._err:
      target.report(ERROR, self._err)

  def addErrorMessage(self, msg: str):
    self.setError()
    if self._err:
      self._err = msg
    else:
      self._err = self._err + "\n" + msg

  def addDebugMessage(self, msg: str):
    if self._debug:
      self._debug = msg
    else:
      self._debug = self._debug + "\n" + msg

  def addInfoMessage(self, msg: str):
    if self._info:
      self._info = msg
    else:
      self._info = self._info + "\n" + msg

  def addWarnMessage(self, msg: str):
    if self._warn:
      self._warn = msg
    else:
      self._warn = self._warn + "\n" + msg

def createResult():
  return Result(False, False, None, None, None, None)

def ok(info: str | None = None, warn: str | None = None):
  return Result(True, False, None, info, warn, None)

def error(msg: str | None = None):
  return Result(False, False, None, None, None, msg)

def cancel(info: str | None = None, warn: str | None = None):
  return Result(False, True, None, info, warn, None)

