# html-ppt-skill 快速参考（外部资源路径）

## 三步上手

### 1. 选主题

```
Business → pitch-deck-vc, corporate-clean, swiss-grid
Tech     → tokyo-night, dracula, catppuccin-mocha, terminal-green
小红书   → xiaohongshu-white, soft-pastel, rainbow-gradient
Academic → academic-paper, editorial-serif, minimal-white
Edgy     → cyberpunk-neon, vaporwave, y2k-chrome, neo-brutalism
```

预览：`templates/theme-showcase.html`（按 T 键循环）

### 2. 选模板

```
演讲+逐字稿 → presenter-mode-reveal（推荐）
技术分享    → tech-sharing
产品发布    → product-launch
投资人路演  → pitch-deck
小红书图文  → xhs-white-editorial / xhs-pastel-card
课件        → course-module
周报        → weekly-report
```

参考：`templates/full-decks/<name>/`

### 3. 开始写

```bash
mkdir -p "项目名/slides"
cp -r D:/桌面/PPT制作/assets/ "项目名/slides/assets/"
```

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>标题</title>
  <link rel="stylesheet" href="assets/fonts.css">
  <link rel="stylesheet" href="assets/base.css">
  <link rel="stylesheet" href="assets/animations/animations.css">
  <style>
    :root { /* 主题 CSS 变量覆盖 */ }
  </style>
</head>
<body>
<div class="deck">
  <section class="slide" data-title="封面">
    <div class="slide-content">
      <h1>标题</h1>
      <p class="subtitle">副标题</p>
    </div>
    <div class="notes">逐字稿 150-300 字</div>
  </section>
  <!-- 更多 slide ... -->
</div>
<script src="assets/runtime.js"></script>
</body>
</html>
```

## 常用快捷键

| 按键 | 功能 |
|------|------|
| ← → / 空格 | 翻页 |
| F | 全屏 |
| S | 演讲者视图（弹出） |
| N | 备注面板 |
| O | 概览 |
| T | 循环主题 |
| A | 循环动画 |

## 动画

```html
<!-- CSS 入场动画 -->
<div class="anim-fade-up">...</div>
<div class="anim-zoom-pop">...</div>
<div class="anim-glitch-in">...</div>
<div class="anim-typewriter">...</div>

<!-- Canvas 特效 -->
<section class="slide" data-fx="firework">...</section>
<section class="slide" data-fx="starfield">...</section>
<section class="slide" data-fx="confetti-cannon">...</section>
<section class="slide" data-fx="neural-net">...</section>
```
