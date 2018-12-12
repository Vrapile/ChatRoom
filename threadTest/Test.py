import threading
import time
import inspect
import ctypes


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


def sayTime():
    i = 0
    while True:
        print('正在录音...' + str(i) + '秒')
        time.sleep(1)
        i = i + 1


def saveVoice(tsayTime):
    i = 0
    while i < 5:
        print('正在保存录音...' + str(i) + '秒')
        time.sleep(0.5)
        i = i + 0.5
    stop_thread(tsayTime)


if __name__ == "__main__":
    tsayTime = threading.Thread(target=sayTime)
    tsayTime.start()

    tsaveVoice = threading.Thread(target=saveVoice(tsayTime))
    tsaveVoice.start()

    print("stoped")
