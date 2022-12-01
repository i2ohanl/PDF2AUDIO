import PyPDF2
from gtts import gTTS
import os

def audioconvert(file_name):
#["en","ar","bn","de","en-in","en-au","en-gb","hi","ml","mr","ta","te","ur"]:
    path = open("uploaded_files/"+file_name, 'rb')

    # Checking for upload size, limit set to 10mb
    stats=os.stat("uploaded_files/"+file_name)
    if stats.st_size > 10485760: #size comes in bytes so we use 1024*1024*10
        return -1

    #Checking for file format
    print(file_name)
    if file_name[-3:] != ".pdf":
        return -2

    pdfReader = PyPDF2.PdfFileReader(path)

    text=[]
    try:
        for i in range(pdfReader.getNumPages()):
            try:
                from_page = pdfReader.getPage(i)
                text.append(from_page.extractText())
            except:
                return -3
    except:
        return -3
    try:
        text=" ".join(text)
        speech = gTTS(text=text, lang="en", slow=False)
    except:
        return -3
    speech.save("converted_audios/" + file_name[:-3] + "mp3")
    return 1