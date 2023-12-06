# JBD-BMS-bluetooth

JBD BMS and Thornwave bluetooth data monitoring<br>
([https://github.com/bitbybyte/fantiadl](https://github.com/tgalarneau/bms))をベースに改修<br>

メインプログラム(bluetoothから生データ取得)
 - jbdbms-4-socket-1temp.py   ( 4S / 1temp用) original
 - jbdbms-4-socket-2temps.py  ( 4S / 2temp用) original
 - jbdbms-8-socket-2temps.py  ( 8S / 2temp用) original
 - jbdbms-14-socket-4temps.py (14S / 4temp用)
 - jbdbms-16-socket-4temps.py (16S / 4temp用) original

使用方法：<br>
python3 bdbms-4-socket-1temp.py -b {ブルートゥースアドレス} -i {取得間隔(秒}) -m {任意名称}

使用例：<br>
python3 bdbms-14-socket-4temps.py -b A5:C2:37:04:EB:EE -i 5 -m liion48

----------------------------------------------------------------------------------------
サブプログラム(生データからjsonファイル生成)
 - bt-jbd-4s.py
 - bt-jbd-8s.py
 - bt-jbd-14s.py

修正箇所
 - ブルートゥースのアドレス
 - 任意名称
 - jsonファイル配置先

<pre>
####  Change Param ####
DEVICE = "A5:C2:37:04:EB:FF" # Bluetooth Address
BMSNAME= "liion48-1"         # BMS Name

FILENAME= str("/mnt/data/%s.json" % BMSNAME)  # File Location
#####################3#
</pre>
使用方法：<br>
python3 bt-jbd-14s.py

出力データ例.
<pre>
  {
    device:liion48
    voltage:55.56
    amp:0
    watt:0
    remain:0
    capacity:40
    cycles:35
    cellmin:cell2
    cellsmin:3.779
    cellmax:cell12
    cellsmax:4.047
    delta:268
    cell1:3.783
    cell2:3.779
    cell3:3.78
    cell4:3.784
    cell5:4.042
    cell6:4.042
    cell7:4.043
    cell8:4.044
    cell9:4.043
    cell10:4.046
    cell11:4.046
    cell12:4.047
    cell13:4.045
    cell14:4.044
    datetime:20231205103107
}
</pre>
----------------------------------------------------------------------------------------
