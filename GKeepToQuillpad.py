import re
import sys
import os
import subprocess

def extractnote(line):
    #print(line)
    ispinned =re.search(r'"isPinned"(.*?),',line[0]).group(0)
    print(ispinned)
    note = re.search(r'"text(.*)title":"(.*?)"', line[0]).group(0)
    note = ''.join((ispinned,note))
    print(note)
    return note
def main():
    files = sys.argv[1:]
    respath='./res/'
    if not os.path.exists(respath):
        os.makedirs(respath)
    id=1
    filename_all= ''.join((respath,'backup.json'))
    file_all= open(filename_all,'a')
    readout=open(filename_all,'r')
    file_all.write('{"version":17,"notes":[')
    for filename in files:
        filein=open(filename,'r')
        line = filein.readlines()
        #print(filename)
        note=extractnote(line)

        fileout = open(''.join((respath, filename)),'w')
        newline = ''.join(('{',note,''.join((',"id":',str(id),'}'))))
        #print(note)
        if id==1 :
            file_all.writelines(newline)
        else :
            file_all.writelines(',')
            file_all.writelines(newline)
#        file_all.write(''.join((newline,',')))
        readout.readlines()
        #fileout.writelines(newline)
        fileout.close()
        filein.close()
        id=id+1
    file_all.write(']}')
    file_all.close()

    sedcmd = ''.join(("sed -i -e 's/textContent/content/g' ", filename_all))
    print("sed : \n") 
    print(sedcmd)
    #subprocess.run([sedcmd])
print(__name__)
if __name__ == '__main__':
    main()
