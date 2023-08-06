r"""
The OpenRPA package (from UnicodeLabs/Ivan Maslov)
__main__ file goes outside the package and used like a main file when the python runs module directly from start
"""
import traceback
from .Core import ProcessCommunicator
from .Core import JSONNormalize
from .Core import UIDesktop
##########################################
#Run UIDesktop from new process. Communication with paren process by PIPE channel
##########################################
#Определить разрядность процесса
buffer = ""
lJSONInputString=""
while True:
    #Reset the lProcessResponse
    lProcessResponse={"ErrorFlag":False}
    try:
        #Ожидаем синхронно поступление объекта
        lJSONInput = ProcessCommunicator.ProcessParentReadWaitObject()
        lProcessResponse["ActivitySpecificationDict"]=lJSONInput
        #Выполнить вызов функции
        lFunction = getattr(UIDesktop,lJSONInput['ActivityName'])
        lProcessResponse["Result"]=JSONNormalize.JSONNormalizeDictListStrIntBool(lFunction(*lJSONInput['ArgumentList'],**lJSONInput['ArgumentDict']))
    except Exception as e:
        #Установить флаг ошибки
        lProcessResponse["ErrorFlag"]=True
        #Зафиксировать traceback
        lProcessResponse["ErrorTraceback"]=traceback.format_exc()
        #Зафиксировать Error message
        lProcessResponse["ErrorMessage"]=str(e)
        #lProcessResponse["ErrorArgs"]=str(e.args)
    #Отправить ответ в родительский процесс
    ProcessCommunicator.ProcessParentWriteObject(lProcessResponse)