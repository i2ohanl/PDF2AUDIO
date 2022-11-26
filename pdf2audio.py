import PyPDF2
from gtts import gTTS

def audioconvert(file_name):
# file_name=input("Enter your file name:")
# language=input("Enter language of choice from given list\n[en,ar,bn,de,en-in,en-au,en-gb,hi,ml,mr,ta,te,ur] :")
# if language in ["en","ar","bn","de","en-in","en-au","en-gb","hi","ml","mr","ta","te","ur"]:
#     pass
# else:
#     print("Invalid language choice, try again!")
    print("Inside module")
    path = open("uploaded_files/"+file_name, 'rb')
    
    pdfReader = PyPDF2.PdfFileReader(path)
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