import re
import sys
import os
import subprocess


#OK :
#-text content of notes
#-title of notes
#-pinned status

#TODO
#-note date (will be reset to today by quillpad at import)
#-tags
#-id (now made with alphabetical order)


def extractnote(line):
    #print(line)
    #extracts if the note is pinned or not
    isPinned =re.search(r'"isPinned"(.*?),',line[0]).group(0)
    #print(ispinned)
    #extracts title and content
    note = re.search(r'"text(.*)title":"(.*?)"', line[0]).group(0)
    note = ''.join((isPinned,note))
    #print(note)
    return note
def main():
    '''
    export your google keep notes with takeout
    unzip the downloaded archive
    move all json to a separate folder
    from this json only folder run 
    python3 GKeepToQuillad.py *.json
    then run the written sed command
    compress the res/backup.json file in a zip
    import this zip in Quillpad and hope it works
    '''
    files = sys.argv[1:]
    respath='./res/'
    if not os.path.exists(respath):
        os.makedirs(respath)
    id=1
    #Quillpad has all notes in one json file. GKeep has one json file per note. 
    #create a result file to write all GKeep migrated notes. this file MUST be named backup.json to be imported by Quillpad.
    filename_all= ''.join((respath,'backup.json'))
    file_all= open(filename_all,'a')
    readout=open(filename_all,'r')
    #Quillpad header
    file_all.write('{"version":17,"notes":[')
    for filename in files:
        filein=open(filename,'r')
        line = filein.readlines()
        #print(filename)
        note=extractnote(line)

        #fileout = open(''.join((respath, filename)),'w')
        newline = ''.join(('{',note,''.join((',"id":',str(id),'}'))))
        #print(note)
        if id==1 :
            file_all.writelines(newline)
        else :
            file_all.writelines(',')
            file_all.writelines(newline)
        #file_all.write(''.join((newline,',')))
        readout.readlines()
        #fileout.writelines(newline)
        filein.close()
        id=id+1
    file_all.write(']}')
    file_all.close()
    #fileout.close()
  
    sedcmd = ''.join(("sed -i -e 's/textContent/content/g' ", filename_all))
    print("run this sed command : \n")
    #don't edit the file with a text editor, or use vim -b to keep the file as a [noeol] (no end of line) file, to match Quillpad format. not sure if necessary.
    print(sedcmd)
    #subprocess.run([sedcmd])
print(__name__)
if __name__ == '__main__':
    main()
