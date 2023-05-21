# Google Drive Python 猴版百宝箱
_没有在 Win 下测试过 理论上是 OK的_
## validate-sa.py
```
python3 validate-sa.py -r <盘ID> -d <SA文件夹> -b -v
```
其中 `-d` 默认为 `files/validate` 文件夹。`-b` 将备份 `SA文件夹` 到 `files/SA文件夹.zip`。`-v` 输出一些没什么卵用的东西。`-t` 测试模式（不备份，不移动错误 json）

```
sudo pip3 install -r requirements.txt
```

