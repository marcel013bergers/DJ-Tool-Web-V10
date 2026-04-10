Set WshShell = CreateObject("WScript.Shell")
scriptPath = Replace(WScript.ScriptFullName, "Start_DJ_Tool_LEISE.vbs", "Start_DJ_Tool_NUR_EIN_BROWSER.bat")
WshShell.Run Chr(34) & scriptPath & Chr(34), 0, False
Set WshShell = Nothing
