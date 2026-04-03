# 專案背景

## 幣圈財經日報專案

目標：仿照 ai-daily-skill 的架構，建立一個幣圈版的財經日報 Claude Code Skill，提供給社群使用。

### 社群資訊
- 社群名稱：讀書社群 & JB Club
- 主要發布平台：LINE

### 現有 n8n 工作流（參考基礎）
- 觸發：每天早上 8 點自動執行
- RSS 來源（4 個）：
  - The Block (https://www.theblock.co/rss.xml)
  - ForexLive (https://www.forexlive.com/feed)
  - WSJ Markets (https://feeds.a.dj.com/rss/RSSMarketsMain.xml)
  - CoinDesk (https://www.coindesk.com/arc/outboundfeeds/rss/)
- 過濾：只取昨天以後的文章
- AI 分析：Gemini 2.5 Flash
- 儲存：Notion 資料庫「讀書社群財經日報」

### AI 角色設定（來自 n8n prompt）
讀書社群 & JB Club 首席加密貨幣總經分析師，從大量資訊中篩選出能影響市場趨勢、值得交易者關注的核心資訊，精縮成適合 LINE 閱讀的高含金量簡報。

### 輸出格式要求
- 禁止使用任何 Markdown 符號（#, ##, **, __, > 等）
- 使用 Emoji 作為視覺引導
- 語氣專業親切
- 3 條核心市場資訊
- 格式範本：
  📊【讀書社群財經日報｜yyyy-MM-dd】
  📈 昨日市場總結（1-2句）
  💡 三大關鍵資訊（每條2-3句，點出對加密貨幣的潛在影響）
  --------------------
  📁 完整日報存檔請至 Notion 查閱

### 語言
繁體中文

### 已確認的設計決策
- 不需要 Notion 儲存功能
- RSS 來源全部沿用（The Block、ForexLive、WSJ、CoinDesk）
- 觸發方式：自動排程（每天早上 8 點，沿用 n8n 設定）
- 輸出格式：網頁 + 流光字卡（HTML，存在本機）
- 不需要自動推送到 LINE，手動發送即可

### 社群名稱
金蹦社群（JB Club）

### 流光字卡格式（參考截圖）
- 深色背景（深藍近黑）
- 左側有流光掃過效果（CSS 動畫）
- 內容：
  - 標題：📅 金蹦社群財經日報
  - 日期
  - 「核心摘要」標籤
  - 3 條新聞（格式：序號｜Emoji【分類標籤】核心事件標題 + 2-3句說明）
  - 無浮水印
- 尺寸：適合手機截圖分享到 LINE（約 400x700px）

### 網頁格式
- 完整日報的視覺化呈現
- 風格：仿 ai-daily 蘋果風（純黑背景、藍色光暈、SF Pro 字體、極簡設計）
