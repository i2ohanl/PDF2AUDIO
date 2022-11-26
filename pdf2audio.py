import PyPDF2
from gtts import gTTS
import os

def audioconvert(file_name):
# file_name=input("Enter your file name:")
# language=input("Enter language of choice from given list\n[en,ar,bn,de,en-in,en-au,en-gb,hi,ml,mr,ta,te,ur] :")
# if language in ["en","ar","bn","de","en-in","en-au","en-gb","hi","ml","mr","ta","te","ur"]:
#     pass
# else:
#     print("Invalid language choice, try again!")
    print("Inside module")
    file_path="uploaded_files/"+file_name
    stats=os.stat(file_path)
    if stats.st_size > 10485760: #size comes in bytes so we use 1024*1024*10
        print("File size too big")
    else:
        try:
            pdfReader = PyPDF2.PdfFileReader(open(file_path, 'rb'))
        except PyPDF2.utils.PdfReadError:
            print("invalid PDF file")
        else:
            pass
        text=[]
        try:
            for i in range(pdfReader.getNumPages()):
                try:
                    from_page = pdfReader.getPage(i)
                    text.append(from_page.extractText())
                except:
                    pass
        except:
            print("Number of pages error, please enter valid pdf!")
        try:
            text=" ".join(text)
            speech = gTTS(text=text, lang="en", slow=False)
        except:
            print("speech formation error!")
        speech.save("converted_audios/" + file_name[:-3] + "mp3")
        os.remove(file_path)
