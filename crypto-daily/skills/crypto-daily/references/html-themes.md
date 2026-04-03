# HTML 主題規範

## 網頁版：蘋果風（Apple Style）

### 設計原則
- 純黑背景 (#000000)
- 右下角藍色漸層光暈 (#0A1929 → #1A3A52)
- 大量留白，內容密度 ≤ 40%
- 標題字體：SF Pro Display（fallback: -apple-system, BlinkMacSystemFont）
- 內文字體：SF Pro Text
- 平滑動畫與懸停效果
- 單一 HTML 檔案，無外部依賴

### 色彩系統
- 標題：#FFFFFF
- 內文：#E3F2FD
- 強調色：#42A5F5
- 次要文字：#B0BEC5
- 分隔線：rgba(255,255,255,0.08)
- 卡片背景：rgba(255,255,255,0.04)

### Logo
Logo 圖檔路徑：`/Users/kunbu0505/Downloads/8F150216-AD1D-4161-801A-0522C1615422_1_105_c-Photoroom.png`
生成網頁時讀取此檔案轉為 base64 嵌入，以 `<img>` 標籤顯示，圓形裁切，寬高 48px，白色背景。

### 頁面結構
```
Header
  - JB Logo 圖片（圓形 48px）+ 「金蹦社群幣圈日報」
  - 日期 Badge

Main
  - 市場總結卡片
  - 三大關鍵資訊（各為獨立卡片）
    - 序號 + 分類標籤
    - 標題
    - 內文說明

Footer
  - 資料來源：The Block / ForexLive / WSJ / CoinDesk
  - 版權文字
```

### 動畫效果
- 頁面載入時卡片由下往上淡入
- 卡片 hover 時微微上移 + 邊框發光

---

## 流光字卡：深色流光風

### 設計原則
- 尺寸：400 × 700px（適合手機截圖）
- 深藍近黑背景（#0D1117）
- 左側或頂部流光掃過動畫（白色/金色半透明光帶）
- 圓角卡片，內邊距充足
- 無浮水印

### 流光動畫 CSS 範例
```css
@keyframes shimmer {
  0% { transform: translateX(-100%) skewX(-15deg); }
  100% { transform: translateX(400%) skewX(-15deg); }
}

.card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 60px;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
  animation: shimmer 3s infinite;
}
```

### 色彩系統
- 背景：#0D1117
- 邊框：rgba(255,255,255,0.1)
- 標題：#FFFFFF
- 日期：#8B949E
- 標籤背景：rgba(66,165,245,0.15)
- 標籤文字：#42A5F5
- 內文：#C9D1D9

### 字卡結構
```
📅 金蹦社群財經日報
YYYY-MM-DD

核心摘要

01｜🔥【分類標籤】標題
02｜🔥【分類標籤】標題
03｜🔥【分類標籤】標題
```
