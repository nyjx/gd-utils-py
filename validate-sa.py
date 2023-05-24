
import os, argparse, shutil
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import GoogleAuthError
from google.oauth2 import service_account

def testSA(real_file_id,service_account_file):
    try:
        credentialsSA = service_account.Credentials.from_service_account_file(service_account_file)
    except Exception as jerror:
        code = 'json'
        details = service_account_file + ' json ' + str(jerror)
        return [code, details]

    try:
        service = build('drive', 'v3', credentials=credentialsSA)
        # Call the Drive v3 API
        results = service.files().get(fileId=real_file_id, supportsAllDrives=True).execute()
        # print(results)
        code = ''
        details = service_account_file + ' ' + results['kind'] + ' OK'
        return [code, details]
    
    except GoogleAuthError as auth_error:
        # Handle errors from google auth
        details = service_account_file + ' ' + auth_error.args[0]
        code = 'cred'
        return [code, details]
    except HttpError as http_error:
        # Handle errors from drive API.
        details = service_account_file + ' ' + http_error.reason
        code = str(http_error.status_code)
        return [code, details]
    except Exception as uerror:
        code = 'ukwn'
        details = service_account_file + ' ' + str(uerror)
        return [code, details]
        


if __name__ == '__main__':

    # workDir = 'files/validate'
    scrpPath = os.path.dirname(__file__)
    workDir = os.path.join(scrpPath, 'files','validate')
    workBase = os.path.dirname(workDir)

    # check input argument
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-r', '--remote', help="GDrive ID for testing", required=True)
    argParser.add_argument('-d', '--directory', default=workDir, help="SA folder location")
    argParser.add_argument('-b', '--backup', action='store_true', help="backup [SA] folder to [SA_bak] before check")
    argParser.add_argument('-v', '--verbose', action='store_true')
    argParser.add_argument('-t', '--test', action='store_true', help="TEST MODE: VERBOSE ENABLED & MOVE BACK UP DISABLED")
                        
    args = argParser.parse_args()

    if args.test: 
        args.verbose = True
        args.backup = False

    # display input
    if args.verbose: print("运行参数为: %s" % args)

    if len(args.remote) <10 or len(args.remote) >100: exit("目录ID缺失或格式错误")

    args.directory = os.path.expanduser(args.directory)
    args.directory = os.path.abspath(args.directory)
    if args.verbose: print("SA 文件夹:" , args.directory)
    if not os.path.isdir(args.directory): exit("SA 文件夹不存在")

    if not os.path.exists(workDir) :
        try: os.makedirs(workDir)
        except: exit("脚本目录文件冲突")

    saProjName = os.path.basename(args.directory)

    if args.backup: 
        try: 
            archPath = os.path.join(scrpPath, saProjName)
            archPath = shutil.make_archive(archPath, 'zip', args.directory)
            shutil.move(archPath, workBase)
            print("备份至：", os.path.join(workBase, saProjName + '.zip'))

            # backPath= args.directory + '_bak'
            # shutil.copytree(args.directory, backPath)
            # print("备份至：", backPath)
        except OSError as err:
            print(err)
            exit("备份失败")


    # loop through files
    countF = 0
    errorF = 0
    for root, _, files in os.walk(args.directory):

        for file in files:
            if file.lower().endswith('json') :
                countF = countF + 1
                oldpath = os.path.join(root, file)

                # check SA
                code, details = testSA(args.remote,service_account_file=oldpath)
                if args.verbose: print(code, details)

                # test mode, since code is given 0, move is disabled
                if args.test: 
                    if code: errorF = errorF + 1 ; code = 0

                # if len(code) > 0:
                if code:
                    errorF = errorF + 1
                    errpath = root + '_' + code
                    newpath = os.path.join(errpath, file)
                    if not os.path.exists(errpath): os.mkdir(errpath)
                    if args.verbose: print("moved to", errpath)
                    # shutil.copy(oldpath, newpath)
                    shutil.move(oldpath, newpath)
                # status
                print('Checked:', countF, '/ Error:', errorF, end='\r')
    print('Checked:', countF, '/ Error:', errorF)
