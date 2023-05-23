import os, argparse

if __name__ == '__main__':

    # workDir = 'files/validate'
    scrpPath = os.path.dirname(__file__)
    workDir = os.path.join(scrpPath, 'files','validate')
    rclone_conf = os.path.join(os.path.dirname(workDir), 'rclone.conf')

    # check input argument
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-d', '--directory', default=workDir, help="SA folder location")
    argParser.add_argument('-v', '--verbose', action='store_true')
    argParser.add_argument('-x', '--replace', help='替换目录头用 -x "dir1/dir2:dirA/dirB"')
                 
    args = argParser.parse_args()
    # display input
    if args.verbose: print("运行参数为: %s" % args)

    args.directory = os.path.expanduser(args.directory)
    args.directory = os.path.abspath(args.directory)
    if args.verbose: print("SA 文件夹:" , args.directory)
    if not os.path.isdir(args.directory): exit("SA 文件夹不存在")

    # prepare replace docker path is true
    if args.replace: 
        replace_Dir = True ; 
        try:
            host_PATH , docker_PATH = args.replace.split(sep=':')
            docker_PATH = os.path.expanduser(docker_PATH)
            docker_PATH = os.path.abspath(docker_PATH)
            host_PATH = os.path.expanduser(host_PATH)
            host_PATH = os.path.abspath(host_PATH)
        except:
            exit('读取替换目录参数错误  -x "dir1/dir2:dirA/dirB"')
        if not args.directory.startswith(docker_PATH): 
            exit("替换目录头与 SA 文件夹目录不对应")
       
    # loop through files
    old_root = ''
    countF = 0
    sa_configs = dict()
    if args.verbose: print("开始扫描 jason 文件")
    for root, _, files in os.walk(args.directory):
        for file in files:
            if old_root != root and file.lower().endswith('json') :
                countF = countF + 1
                # path of json file
                oldpath = os.path.join(root, file)
                sa_configs[os.path.basename(root)] = oldpath
                old_root = root
                if args.verbose: print("配置名:" , os.path.basename(root), 
                                       "service_account_file_path:" , os.path.dirname(oldpath), 
                                       "service_account_file:" , oldpath)

    if args.verbose: print("扫描到", countF, "个配置文件")
    if countF == 0: exit("未找到配置文件 无法生成 rclone.conf")
    if args.verbose: print("生成 rclone.conf")
    conf_keys = list(sa_configs)
    conf_keys.sort()

    try: fh = open(rclone_conf,'x') 
    except Exception as error: exit(error)
    
    if replace_Dir and args.verbose: 
        print("开启目录替换")
        print(docker_PATH, "将会被替换为", host_PATH)
    for key in conf_keys:
      conf_name = key
      if replace_Dir: 
          file_name = sa_configs[key].replace(docker_PATH, host_PATH, 1)
      else:
          file_name = sa_configs[key]
      dir_name = os.path.dirname(file_name)

      rclone_sample = f"""
[{conf_name}]
type = drive
scope = drive
service_account_file_path = {dir_name}
service_account_file = {file_name}
      """

      fh.write(rclone_sample)

    fh.close()
    if args.verbose: print("生成完毕", rclone_conf)


