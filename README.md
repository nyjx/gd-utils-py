# Google Drive Python 猴版百宝箱
_没有在 Win 下测试过 理论上是 OK的_

首先：安装依赖
```
sudo pip3 install -r requirements.txt
```
## validate-sa.py
测试 SA文件夹中 json 文件对 目录ID 的权限
```
python3 validate-sa.py -r <盘ID> -d <SA文件夹>
```
### 参数
* `-r` folder_id
* `-d` 默认为 `files/validate` 文件夹
* `-b` 备份 `SA文件夹` 到 `files/SA文件夹.zip`
* `-v` 输出一些没什么卵用的东西
* `-t` 测试模式（不备份，不移动错误 json）
### 运行
```
# 运行前
files
└── validate              # 默认检测目录
    ├── sa                # 目录内可以放多个文件夹
    └── sb                # 区分多个 sa project

# 运行后
files
├── validate.zip          # SA 备份文件
└── validate              # 默认检测目录
    ├── sa                # 有效的 sa json 保持原位不移动
    ├── sa_404            # 错误的 sa json 根据错误类型
    ├── sa_cred           # 分别放入不同的错误文件夹
    ├── sa_json
    ├── sa_ukwn
    ├── sb                # 另一个有效的 sa project 文件夹
    ├── sb_404            # 另一个 sa project 的错误文件夹
    ├── sb_cred
    ├── sb_json
    └── sb_ukwn
```
### 错误类型
* json: 读取 json 错误
* cred: json 读取成功 但是云端登录失败
* [http error]: 登录成功后无法操作 `<盘ID>`
  * 404：`<盘ID>` 不存在或 SA 没有权限
  * 400: access_token 获取失败
  * 其他类型遇到了再更新
* ukwn: 别的错误

## config-gen.py
生成一套符合 fclone/gclone 方案的 rclone.conf 文件
```
python3 config-gen.py -d <SA文件夹>
```
### 参数
* `-d` 默认为 `files/validate` 文件夹
* `-v` 输出一些没什么卵用的东西
* `-x` 替换文件夹中的目录地址，和 docker run -v 命令相同格式 `-x "/[rclone/SA工作/目录]:/gd-utils-py/files/validate"` 注意目录中不包含 SA 文件夹名
### 运行
`rclone.conf` 文件默认生成于 `files` 文件夹内，如果已经存在会报错。
```
# 运行前
files
└── validate              # 默认检测目录
    ├── sa                # 目录内可以放多个文件夹
    └── sb                # 区分多个 sa project
# 运行后
files
├── rclone.conf           # rclone 配置文件
...
```
`rclone.conf` 范例
```
# 不替换
[sa]
type = drive
scope = drive
service_account_file_path = /gd-utils-py/files/validate/sa
service_account_file = /gd-utils-py/files/validate/sa/xx1.json

[sb]
type = drive
scope = drive
service_account_file_path = /gd-utils-py/files/validate/sb
service_account_file = /gd-utils-py/files/validate/sb/yy1.json
```
```
# 替换参数 -x "/root/rclone_sa:/gd-utils-py/files/validate"
[sa]
type = drive
scope = drive
service_account_file_path = /root/rclone_sa/sa
service_account_file = /root/rclone_sa/sa/xx1.json

[sb]
type = drive
scope = drive
service_account_file_path = /root/rclone_sa/sb
service_account_file = /root/rclone_sa/sb/yy1.json
```

# Reference:
https://developers.google.com/drive/api/guides/about-files

https://github.com/iwestlin/gd-utils/blob/master/validate-sa.js