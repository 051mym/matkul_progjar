#https://docs.python.org/3/library/ftplib.html                                              SEMUA TUTORIAL TERSEDIA DISINI

from ftplib import FTP
import shutil

print('Input user: ') 
user = input()
print('Input password: ')
pswd = input()
print('Input IP FTP: ')
ipftp = input()

f = FTP('localhost')
f.login(user, pswd)

print('(LIST/PWD/CD/MKDIR/SENDALL/DOWNZIP)')

while True:
    print('>>', end='')
    action = input()
    # list action
    act1 = 'LIST'
    act2 = 'PWD'
    act3 = 'CD'
    act4 = 'MKDIR'
    act5 = 'SENDALL'
    act6 = 'DOWNZIP'

    if action.count(act1) == 1:
        names = f.nlst()                                        #LIST DIRECTORY
        print('List : ' + str(names))

    elif action.count(act2) == 1:
        print('PWD :' + f.pwd())           #PRESENT WORK DIRECTORY

    # elif action.count(act2) == 1:                               
    #     inpt2 = action.replace('RETR ', '')                        #DOWNLOAD   
    #     f.retrbinary("RETR " + inpt2, open(inpt2, 'wb').write)

    
    # elif action.count(act3) == 1:
    #     inpt2 = action.replace('STOR ', '')
    #     f.storbinary('STOR ' + inpt2, open(inpt2, 'rb'))              #UPLOAD


    elif action.count(act3) == 1:
        inpt2 = action.replace('CD ', '')
        f.cwd(inpt2)                                                   #CD
        


    elif action.count(act4) == 1:
        inpt2 = action.replace('MKDIR ', '')                                           
        f.mkd(inpt2)                                               #BUAT DIRECTORY
    
    elif action.count(act5) == 1:
        print('PWD :' + f.pwd())           #PRESENT WORK DIRECTORY

    elif action.count(act6) == 1:                               #DOWNPRESS (FILE DIRECTORY DIUBAH SECARA MANUAL)
        inpt2 = action.replace('DOWNZIP ', '')  
        shutil.make_archive('./filezilla/' + inpt2, 'zip', './filezilla/' + inpt2)
        fz = inpt2 + '.zip'                   
        f.retrbinary("RETR " + fz, open(fz, 'wb').write)
        f.delete(fz)

    else:
        print('Salah Command')
        print('(LIST/RETR/STOR/MKD/PWD/DOWNPRESS)')
f.quit()