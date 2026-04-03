---
name: crypto-daily
description: 每日自動抓取幣圈與總經新聞（The Block、ForexLive、WSJ、CoinDesk），用 Claude AI 分析摘要，生成繁體中文財經日報。輸出流光字卡與蘋果風網頁，供金蹦社群 LINE 分享使用。觸發詞：「今日幣圈日報」「昨日財經日報」「幣圈日報」等。
---

# 金蹦社群幣圈日報

每日從四大 RSS 來源抓取幣圈與總經新聞，透過 Claude AI 分析摘要，生成繁體中文財經日報，並輸出流光字卡與蘋果風網頁。

## 快速開始

```
昨日幣圈日報
今日財經日報
2026-04-02 的幣圈日報
```

---

## 工作流程

```
Progress:
- [ ] Step 1: 解析日期
- [ ] Step 2: 抓取 RSS
- [ ] Step 3: 檢查是否有資料
- [ ] Step 4: AI 分析與摘要
- [ ] Step 5: 輸出純文字日報
- [ ] Step 6: 生成流光字卡 HTML
- [ ] Step 7: 生成蘋果風網頁 HTML
```

---

## Step 1：解析日期

從使用者輸入判斷目標日期：

| 輸入 | 目標日期 |
|------|----------|
| 昨日、昨天 | 今天 - 1 天 |
| 前天 | 今天 - 2 天 |
| 今日、今天 | 今天 |
| 2026-04-02 | 直接使用 |

日期格式統一為 `YYYY-MM-DD`（台北時間 UTC+8）

---

## Step 2：抓取 RSS

執行腳本抓取四大來源：

```bash
python scripts/fetch_news.py --relative yesterday
```

其他用法：
```bash
# 指定日期
python scripts/fetch_news.py --date 2026-04-02

# 查看可用日期範圍
python scripts/fetch_news.py --date-range

# JSON 格式輸出
python scripts/fetch_news.py --relative yesterday --json
```

RSS 來源：
- The Block (https://www.theblock.co/rss.xml)
- ForexLive (https://www.forexlive.com/feed)
- WSJ Markets (https://feeds.a.dj.com/rss/RSSMarketsMain.xml)
- CoinDesk (https://www.coindesk.com/arc/outboundfeeds/rss/)

---

## Step 3：檢查資料

若輸出以 `NO_CONTENT:` 開頭，表示該日無資料：

```
抱歉，YYYY-MM-DD 暫無財經資訊。

可用日期請執行：python scripts/fetch_news.py --date-range
```

若有資料則繼續 Step 4。

---

## Step 4：AI 分析與摘要

使用以下角色設定分析原始新聞：

**角色**：金蹦社群 & JB Club 首席加密貨幣總經分析師

**任務**：從大量幣圈與總經新聞中，自主判斷重要程度，主動過濾農場文或重複資訊，精縮成 3 條重要的市場資訊。

**分析重點**：
- 對加密貨幣市場的潛在影響
- 機構動向、監管政策、總經數據
- 地緣政治、重大安全事件

**分類標籤**（從以下選擇最適合的）：
- 地緣政治、幣圈安全、機構採用、監管政策、總經數據、DeFi 動態、產品發布、市場行情

---

## Step 5：輸出純文字日報

嚴格按照以下格式，禁止使用任何 Markdown 符號（#, ##, **, __, > 等）：

```
📅【金蹦社群幣圈日報｜YYYY-MM-DD】

📈 昨日市場總結：
（1-2句精煉總結）

💡 三大關鍵資訊：

01｜🔥【分類標籤】核心事件標題
2-3句說明事件內容，並點出對加密貨幣市場的潛在影響。

02｜🔥【分類標籤】核心事件標題
2-3句說明事件內容，並點出對加密貨幣市場的潛在影響。

03｜🔥【分類標籤】核心事件標題
2-3句說明事件內容，並點出對加密貨幣市場的潛在影響。
```

---

## Step 6：生成流光字卡

**重要：必須以 [references/card-template.html](references/card-template.html) 為基礎生成，不得自行設計版面。**

讀取模板後，只填入以下三個位置的內容，其餘 CSS/HTML 結構保持完全不變：
1. 日期：填入 `<!-- 填入日期 -->` 的位置
2. 3 條新聞的標籤 Emoji + 分類文字：填入 `<!-- Emoji -->` 和 `<!-- 分類標籤 -->`
3. 3 條新聞標題：填入 `<!-- 核心事件標題 -->`

儲存至 `docs/cards/YYYY-MM-DD-card.html`。

生成後告知使用者：
```
✅ 流光字卡已生成：docs/cards/YYYY-MM-DD-card.html
在瀏覽器開啟後截圖即可分享至 LINE。
```

---

## Step 7：生成蘋果風網頁

生成單一 HTML 檔案，儲存至 `docs/YYYY-MM-DD.html`。

詳細設計規範見 [references/html-themes.md](references/html-themes.md)。

**蘋果風規格**：
- 純黑背景 + 藍色光暈
- 完整日報內容（市場總結 + 3 條詳細分析）
- 卡片淡入動畫、hover 效果
- 無外部依賴

生成後告知使用者：
```
✅ 網頁日報已生成：docs/YYYY-MM-DD.html
```

---

## 完整範例

**輸入**：「昨日幣圈日報」

**執行流程**：
1. 解析日期 → 昨天
2. 執行 `python scripts/fetch_news.py --relative yesterday`
3. 確認有資料
4. Claude 分析 → 選出 3 條關鍵資訊
5. 輸出純文字日報
6. 生成 `docs/cards/YYYY-MM-DD-card.html`（流光字卡）
7. 生成 `docs/YYYY-MM-DD.html`（蘋果風網頁）

---

## 參考文件

- [輸出格式](references/output-format.md)
- [HTML 主題](references/html-themes.md)
