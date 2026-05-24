# frontend-slides 快速参考（自包含单文件路径）

## 适用场景

- 只需一个 `.html` 文件（邮件/Slack/嵌入）
- PPTX → HTML 转换
- 强调独特视觉风格，需要先看 3 个预览再确定

## 核心差异（vs html-ppt-skill）

| html-ppt-skill | frontend-slides |
|---------------|----------------|
| 多文件：.html + assets/ | 单文件：全内容内联 |
| `<link>` 外部 CSS | `<style>` 内嵌 CSS |
| `<script src="runtime.js">` | `<script>` 内嵌 JS |
| S 键演讲者模式 | 箭头键+滚轮导航 |
| 36 主题 + Canvas 特效 | 纯 CSS 动画 + 预设风格 |

## 参考文件

```
~/.claude/skills/frontend-slides/
├── viewport-base.css     → 必须全量包含
├── html-template.md      → HTML 架构
├── STYLE_PRESETS.md      → 12 预设风格
├── animation-patterns.md → 动画模式
└── scripts/
    ├── extract-pptx.py   → PPTX 提取
    ├── deploy.sh         → Vercel
    └── export-pdf.sh     → PDF
```

## 快速上手

```bash
mkdir -p "项目名"
# 创建 project.html，CSS/JS 全内联
```

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <!-- 字体：Fontshare / Google Fonts，不用系统字体 -->
  <link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=...">
  <style>
    /* 【必需】全量包含 viewport-base.css 内容 */
    /* 【必需】:root CSS 变量定义颜色/字体/间距 */
    /* 【必需】所有字体用 clamp() */
    /* 【必需】100vh 视口适配 */
    /* 【必需】内容密度限制 */
  </style>
</head>
<body>
  <section class="slide title-slide">
    <h1 class="reveal">标题</h1>
    <p class="reveal">副标题</p>
  </section>
  <section class="slide">
    <div class="slide-content">
      <h2 class="reveal">正文</h2>
      <p class="reveal">内容...</p>
    </div>
  </section>
  <script>
    /* SlidePresentation 类：键盘/触摸/进度条/导航点 */
  </script>
</body>
</html>
```

## 关键规则

- ✅ 全量包含 viewport-base.css
- ✅ 所有尺寸用 `clamp()`
- ✅ 每页 100vh，禁止滚动
- ✅ 字体用 Fontshare / Google Fonts
- ⚠ 不要引用外部 assets（base.css / runtime.js）
- ⚠ 不要用 Canvas 特效（不支持）
