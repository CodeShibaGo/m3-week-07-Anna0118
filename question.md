## 什麼是 CSRF 攻擊，該如何預防？

  跨站請求偽造 Cross Site Request Forgery (CSRF)為攻擊者透過偽造用戶請求，誘使受害者在不知情的情況下執行惡意操作。當使用者已經在網站上驗證身份後，該網站會生成一個唯一的 session，並將其儲存在使用者的瀏覽器中的 cookie 中。當使用者與網站進行交互時，瀏覽器會自動將這些 cookie 包含在每個請求中。攻擊者利用這一點，透過向受害者發送包含惡意操作的連結，試圖利用受害者的 session 來執行未授權的操作。

  普遍防禦 CSRF 的方法有兩種:

  1. 檢查 referer 欄位: 在 HTTP 的標頭中有 Referrer 的字段，我們可以檢查這個字段，來確保請求不是來自於其他網站。
  2. 加入 CSRF token：token 由 server 產生，並且加密存在 session 中，只有透過 server 給使用者，並在一定時間內刷新，用戶才能獲的有效的 token。，如果客戶端提供的 token 與其不同，則拒絕請求。

## 說明如何在 flask 專案中使用以下 `csrf_token()`語法

  1. 透過 `from flask_wtf.csrf import CSRFProtect` 導入 CSRFProtect。
  2. 將 CSRF 綁定到 app 上 `csrf = CSRFProtect(app)`
  3. 如果是使用 Flaskform，可以直接在模板渲染 CSRF 欄位

  ```html
  <form method="post">
    {{ form.csrf_token }}
    <form></form>
  </form>
  ```

  如果沒有使用 Flaskform，則需要增加一個隱形的輸入框來儲存 CSRF token:

  ```html
  <form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
  </form>
  ```

## ajax 需不需要使用 csrf token 進行防禦？該如何使用？

  在發出ajax請求時，需要保護POST請求。如果是使用jQuery來進行ajax呼叫時，需要添加X-CSRFToken header。

  ```javascript
  <script type="text/javascript"> 
  var csrf_token = "{{ csrf_token() }}"; // 取得了CSRF token

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          // 先檢查請求的類型，且不是跨域請求
          if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrf_token); // 將X-CSRFToken加到header
          }
      }
  });
  // 確保在每個非安全的 AJAX 請求中都包含了有效的 CSRF token，提高安全性和防止跨站請求偽造攻擊
  </script>
  ```

## 學會 VS Code + VirtualEnv 組合技

  - 如何使用 Virtualenv 建立環境
    ```bash
    pip install virtualenv #安裝 virtualenv 套件
    virtualenv venv #創建虛擬環境
    source venv/bin/activate #啟動虛擬環境
    ```
  - 調教VS code讓環境更好用
    1. 使用快捷鍵 Ctrl+Shift+P 或 Cmd+Shift+P
    2. 輸入 `Python: Select Interpreter`
    3. 從列表中選擇剛剛建立的虛擬環境

  - 如何測試環境使否有載入成功
    ```bash
    where python  # Windows 
    which python  # Unix/Linux
    ```

  - 如何判斷套件是否安裝成功?
  
    在終端機下 `flask run` ，從錯誤訊息判斷

## 學會 Python 基本的套件管理
