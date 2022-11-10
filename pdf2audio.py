import PyPDF2
from gtts import gTTS

file_name=input("Enter your file name:")
language=input("Enter language of choice from given list\n[en,ar,bn,de,en-in,en-au,en-gb,hi,ml,mr,ta,te,ur] :")
if language in ["en","ar","bn","de","en-in","en-au","en-gb","hi","ml","mr","ta","te","ur"]:
    pass
else:
    print("Invalid language choice, try again!")
try:
    path = open(file_name+'.pdf', 'rb')
except:
    print("Such a file does not exist! Try the following:\n* Make sure its a PDF file\n* Check whether file name is correct\n input:")
     
pdfReader = PyPDF2.PdfFileReader(path)
text=[]
for i in range(pdfReader.getNumPages()):
    try:
        from_page = pdfReader.getPage(i)
        text.append(from_page.extractText())
    except:
        pass
try:
    text=" ".join(text)
    speech = gTTS(text=text, lang=language, slow=False)
except:
    print("speech formation error!")
speech.save("output.mp3")