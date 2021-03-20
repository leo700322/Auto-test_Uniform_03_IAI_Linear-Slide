# Introduction

IAI Linear slide是日本IAI精密滑台，主要以設定滑軌的載重、速度、定位來進行自動化的工作，我們能使用設備來執行插卡功能的自動化測試。

## How to control to the device

1. 將IAI線性滑軌接上電源，連接RS-232到電腦，並於裝置管理員頁面確認COM port number，並對應修改下面cmd指令中的"COM5"。
2. 請使用Python 3.6以上64位元的環境，並以cmd執行command如下：

   ```cmd
   IAI_OP.py COM5
   ```

3. 畫面將顯示功能選項如下：

   ```python
   COM4 on, please select option:
   1.GO HOME、2.FORWARD、3.REVERSE、4.LOOP、5.RESET、按e退出:
   ```

4. 選擇執行option 1~3控制滑軌移動的位置，option 4為速度隨機的反覆抽插卡片，option 5則為回歸預設值(目前option 5容易造成機器LED顯示Error)。

5. 官方文件請參考資料夾"Doc\"中的"IAI SSEL Serial Communication Protocol Operating Manual.pdf"，文件"IAI指令格式及參數說明.ods"則是整理過的command規則說明。
