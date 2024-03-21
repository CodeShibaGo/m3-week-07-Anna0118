[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/Gbi5cF2w)
## Readme 


以下步驟將指導您如何將此專案在本地運行。

- 確保您已安裝 Python 3 和 pip

### 安裝步驟

1. **Clone專案**

   Clone此專案到您的本地機器上：

   ```bash
   git clone [repository url]
   ```

2. **創建虛擬環境**

   在專案目錄中建立一個虛擬環境：

   ```bash
   # 安裝 virtualenv 如果還未安裝
   pip3 install virtualenv

   # 創建虛擬環境
   virtualenv venv

   # 啟用虛擬環境
   # 在 Windows 上
   venv\Scripts\activate
   # 在 Unix 或 MacOS 上
   source venv/bin/activate
   ```

3. **安裝所需套件**

   安裝 `requirements.txt` 中列出的所有套件：

   ```bash
   pip install -r requirements.txt
   ```

4. **配置環境變數**

   根據 `.env.example` 文件配置環境變數：

5. **數據庫遷移**

   如果需要，進行數據庫遷移：

   ```bash
   flask db upgrade
   ```

6. **啟動Flask**

   ```bash
   flask run
   ```
    在 [http://localhost:5000](http://localhost:5000) 瀏覽器看到畫面
