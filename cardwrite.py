# Card Writer v1.2
# Apr 16 2025
# (C) 2025 Matt Burrough

from guizero import *
import datetime
import subprocess
import re

# Path to log file for troubleshooting purposes:
logFilePath = "cardlog.csv"

# Function to read value from the prox card
# Used by readcard, but also write and erase functions to verify they succeeded. 
# Returns the value read from the card, or 0 if there was an error.
def doRead():
    # Proxmark command: lf em 410x read
    result = subprocess.run('pm3 -p /dev/ttyACM0 -c "lf em 410x read"', capture_output=True, text=True, shell=True)
    cmdoutput = result.stdout
    x = re.search(" EM 410x ID [0-9A-Z]{10}$", cmdoutput)
    if x:
        id=x.group(0).split(' ')[-1]
        print(datetime.datetime.now(), ", Read ID ",id, file=logFile)
        return id
    else:
        print(datetime.datetime.now(), ", Failed or Empty read attempt.", file=logFile)
        return 0


# Triggered by Write Card button
# Gets the value from the text box, 
# checks to make sure it is a valid 10-digit hex value greater than 0, 
# then writes it to the card. 
# Finally, perfoms a read of the card to confirm the value was written correctly.
def writecard():
    id=tbValue.value
    notNull = True
    if(tbValue.value == "0000000000"):
        notNull = False
    txtStatus.value = "Writing to card..."
    app.update() # Needed to force a re-draw before entering the subprocess. 
    chk = re.search("^[0-9A-Fa-f]{10}$",id)
    if chk and notNull:
        # Proxmark command: lf em 410x clone --id nnnnnnnnnn
        cmdtxt = 'pm3 -c "lf em 410x clone --id "' + id
        result = subprocess.run(cmdtxt, capture_output=True, text=True, shell=True)
        print(datetime.datetime.now(), ", Attempting to Write ID ",id, file=logFile)
        txtStatus.value = "Validating card value..."
        app.update()
        test = doRead()
        if str(id).upper() == str(test).upper():
            txtStatus.value = "Card written successfully!"
            tbValue.clear()
            print(datetime.datetime.now(), ", Successfully wrote ID ",id, file=logFile)
        else:
            txtStatus.value = "Card write failed. Please realign card and try again."
            print(datetime.datetime.now(), ", Failed to write ID: ",id, " != ", test, file=logFile)
    else:
        print(datetime.datetime.now(), ", Regex Failed trying to Write ID: ",id, file=logFile)
        print("Invalid ID for Write!")
        txtStatus.value = "Invalid ID to Write!"
    return


# Triggered by Erase Card button
# Sets the card's value to all 0s to clear it.
# Verifies the card was cleared.
def erasecard():
    tbValue.clear()
    txtStatus.value = "Erasing card..."
    app.update()
    # Proxmark command: lf em 410x clone --id 0000000000
    result = subprocess.run('pm3 -c "lf em 410x clone --id 0000000000"', capture_output=True, text=True, shell=True)
    print(datetime.datetime.now(), ", Erasing card", file=logFile)
    txtStatus.value = "Validating card value is erased..."
    app.update()
    test = doRead()
    if test==0:
        txtStatus.value = "Card erased successfully!"
        tbValue.append("0000000000")
        print(datetime.datetime.now(), ", Successfully erased card", file=logFile)
    else:
        txtStatus.value = "Card erase failed. Please realign card and try again."
        print(datetime.datetime.now(), ", Failed to erase. ID: ",id, " != 0", file=logFile)
    return


# Triggered by Read Card button
# Gets the card's value and sets the text box to the value read
def readcard():
    tbValue.clear()
    txtStatus.value = "Reading card..."
    app.update()
    id = doRead()
    tbValue.append(id)
    if id==0:
        txtStatus.value = "Card is blank or read failed."
    else:
        txtStatus.value = "Read successful."
    return



# Main
logFile = open(logFilePath, "a")

print(datetime.datetime.now(), ", APP START", file=logFile)
logFile.flush()

app = App(title="Lockpick Village Card Writer", width=1920, height=1080)

title = Text(app, text="Lockpick Village Card Writer", size=64, font="Arial", color="darkblue")
box = Box(app, layout="grid")

txtVal = Text(box, text="0x", grid=[0,1], align="right")
txtVal.text_size=36
tbValue = TextBox(box, text="0000000000", width=11, grid=[1,1], align="left")
tbValue.text_size = 36

btnWrite = PushButton(box, text="Write to Card", command=writecard, grid=[0,3,2,1], align="top")
btnWrite.text_size = 36

btnRead = PushButton(box, text="Read Card", command=readcard, grid=[0,5,2,1], align="top")
btnRead.text_size = 36

btnErase = PushButton(box, text="Erase Card", command=erasecard, grid=[0,7,2,1], align="top")
btnErase.text_size = 36

txtStatus=Text(box, text="", grid=[0,9,2,1], align="top")
txtStatus.text_size=36

# Empty text fields for spacing purposes
text = Text(box, text=" ", grid=[0,0])
text = Text(box, text=" ", grid=[0,2])
text = Text(box, text=" ", grid=[0,4])
text = Text(box, text=" ", grid=[0,6])
text = Text(box, text=" ", grid=[0,8])

app.display()

print(datetime.datetime.now(), ", APP SHUTDOWN", file=logFile)
