---
name: ppt-master
description: >
  Unified HTML/PPTX presentation orchestrator. Meta-skill that integrates
  html-ppt-skill, frontend-slides, nature-paper2ppt, ui-ux-pro-max, and
  3 template collections (beautiful-html-templates 34, html-ppt-templates
  15 full-deck+31 layouts, frontend-slides refs) into one decision-tree-driven
  workflow. Routes to the correct sub-skill, prevents architecture conflicts
  (inline vs external assets), provides unified template browsing, and applies
  Chinese typography rules. Use when user says: presentation, PPT, slides, deck,
  slideshow, 幻灯片, 演讲稿, 做一份PPT, 小红书图文, 模板浏览, 论文汇报,
  pitch deck, tech sharing, 组会汇报, 学术报告, 课件, 路演, or 投屏.
---

# ppt-master — 统一 PPT 制作编排器

整合 html-ppt-skill（外部资源 HTML deck）、frontend-slides（自包含内联 HTML）、nature-paper2ppt（学术 PPTX）、beautiful-html-templates（34 个独立模板）为**一个统一工作流**。

**核心原则：编排，不重复实现。** 本 skill 负责任务路由和冲突预防，生成逻辑委托给各子 skill。

---

## 一、决策树（核心路由）

这是本 skill 最核心的部分——根据用户需求走对的路：

```
用户提出 PPT 需求
│
├─ 【学术论文汇报】(组会/journal club/文献分享)?
│   → ROUTE nature-paper2ppt 路径
│   │  输出：.pptx 文件
│   │  例外：用户明确要 HTML 时走 html-ppt-skill
│
├─ 【PPTX → HTML 转换】?
│   → ROUTE frontend-slides Phase 4
│   │  使用：extract-pptx.py → 生成自包含 HTML
│
├─ 【单文件分享】(邮件/Slack/嵌入网页/只需一个 .html)?
│   → ROUTE frontend-slides 路径
│   │  特征：零依赖单文件，CSS/JS 全内联
│   │  参考：frontend-slides/ 的 viewport-base.css / html-template.md / STYLE_PRESETS.md
│   │  禁止：引用外部 base.css / runtime.js
│
├─ 【功能丰富 HTML deck】(演讲者模式/主题切换/Canvas特效/多页)?
│   → ROUTE html-ppt-skill 路径 ← 主力路线
│   │  特征：assets/base.css + runtime.js 外部引用
│   │  资源来源：D:/桌面/PPT制作/assets/
│   │  建议：presenter-mode-reveal 模板带逐字稿
│   │  禁止：内联 assets 文件 / 自写导航 JS
│
├─ 【用漂亮模板做首页/全页】?
│   → ROUTE beautiful-html-template 路径
│   │  先检查模板架构：看 template.html 使用内联还是外部 CSS
│   │  保持原架构，不转换模式
│   │  参考：beautiful-html-templates/<name>/design.md 了解设计理念
│
├─ 【不确定风格/需要设计指导】?
│   → 查询 ui-ux-pro-max search.py 获取配色/字体/风格建议
│   │  python3 scripts/search.py "<主题>" --design-system
│   │  将结果应用到所选引擎的视觉系统
│
└─ 【以上都不是/不确定】?
    → 默认 html-ppt-skill 路径（能力最全面，模板最丰富）
    → 推荐起点：presenter-mode-reveal 全 deck 模板
```

### 🔴 冲突预防规则（IRON RULES）

```
RULE 1: 选定引擎后，整个项目保持一致。不用混合架构。
        一个项目要么用「外部引用 assets」（html-ppt-skill 风格），
        要么用「自包含单文件」（frontend-slides 风格）—— 绝对不混用。

RULE 2: html-ppt-skill 路径 → 永远用 <link> 引用外部 CSS，
        <script src="assets/runtime.js"> 引入运行时。
        绝不内联 base.css / fonts.css / animations.css / runtime.js。

RULE 3: frontend-slides 路径 → 永远自包含单文件，
        所有 CSS 写在 <style>，所有 JS 写在 <script>。
        绝不引用 assets/base.css 或 assets/runtime.js。

RULE 4: beautiful-html-template 路径 → 先看 template.html 的结构
        判断是内联还是外部引用，保持原架构不变。

RULE 5: nature-paper2ppt 路径 → 输出 .pptx 文件。
        除非用户明确要求，不转成 HTML。
```

---

## 二、7 阶段工作流

### Phase 0: 意图分类

**一次 AskUserQuestion 问清楚以下 4 点：**

1. **演示类型**（单选）：商务/技术汇报 / 学术论文 / 小红书图文 / 产品发布/路演 / 内部培训 / 设计展示
2. **技术偏好**（单选）：HTML 幻灯片（浏览器打开） / PPTX 文件（PowerPoint） / 不确定
3. **内容状态**（单选）：已有完整内容 / 粗略大纲 / 只有主题 / 有篇论文要讲
4. **视觉方式**（单选）："先看看模板" / "我已有想法" / "你帮我定"

→ 根据以上回答，进入决策树路由到对应子 skill。

### Phase 1: 模板与风格选择

按**场合**统一展示跨集合模板。参见 `references/template-catalog.md`。

展示 3-5 个最匹配的候选，让用户选：

```
【技术分享】推荐模板：
1. tech-sharing (full-deck) — 代码块+架构图，暗色主题
2. tokyo-night (theme) — 开发者友好，蓝紫色夜空格调
3. 8-bit-orbit (beautiful) — 像素风，适合创意型技术分享
4. hermes-cyber-terminal (full-deck) — 终端风格，极客感十足
```

### Phase 1A: 架构路由

决策树确定引擎后，**立即应用对应 RULE**，锁定架构。

### Phase 2: 项目脚手架

按引擎创建项目结构：

**html-ppt-skill 路径：**
```bash
mkdir -p "项目名/slides"
cp -r D:/桌面/PPT制作/assets/ "项目名/slides/assets/"
# 然后从 assets/full-decks/ 复制最接近的 full-deck 模板
```

**frontend-slides 路径：**
```bash
mkdir -p "项目名"
# 创建单个 .html 文件，全部内联
```

**beautiful-template 路径：**
```bash
cp -r "D:/桌面/PPT制作/assets/template-packs/<色系>/<氛围>/<name>/" "项目名/"
```

**nature-paper2ppt 路径：**
```bash
mkdir -p "项目名/output"
# 委托 nature-paper2ppt 处理
```

### Phase 3: 内容生成

按引擎规则生成幻灯片内容：

**html-ppt-skill 路径：**
- 每个 `<section class="slide" data-title="页名">` 一页
- 主题 CSS 内联在 `<style>` 标签（使用 `var(--xxx)` 标记）
- 资源引用顺序：`fonts.css` → `base.css` → `animations.css`
- Canvas 特效 via `data-fx="firework"`
- CSS 动画 via `class="anim-fade-up"`
- 逐字稿在 `<div class="notes">`（150-300 字）
- 结尾 `<script src="assets/runtime.js"></script>`

**frontend-slides 路径：**
- 单文件，CSS/JS 全内联
- 全量包含 viewport-base.css
- 使用 `.reveal` 类 + 字体使用 Fontshare/Google Fonts
- 严格 viewport 适配（100vh，clamp，内容密度限制）

**beautiful-template 路径：**
- 保持 template.html 的原有结构
- 参考 design.md 色彩/字体体系
- 必要时拆分或扩展页面

**所有 HTML 路径共用：** 应用中文排版规则（见下方）

### Phase 4: 预览与迭代

```bash
# 在浏览器中打开
start "项目名/slides/项目名.html"
```
- 检查是否有溢出
- 检查中文换行是否正确
- 按用户反馈修改

### Phase 5: 演示模式设置

**html-ppt-skill 路径：** 告知用户快捷键
| 按键 | 功能 |
|------|------|
| ← → | 翻页 |
| 空格 | 下一页 |
| F | 全屏 |
| S | 演讲者视图（弹出窗口：当前页/下一页/逐字稿/计时器） |
| N | 备注面板 |
| O | 幻灯片概览 |
| T | 循环切换主题 |
| A | 循环切换动画 |

投屏：浏览器拖到投影 → F 全屏 → S 演讲者视图（笔记本上）

**frontend-slides 路径：** 箭头键翻页，F 全屏，滚轮/滑动

**PPTX 路径：** 标准 PowerPoint 快捷键

### Phase 6: 交付与导出（可选）

完成后询问："需要导出或分享吗？"
- **导出 PDF**：`bash scripts/export-pdf.sh 文件名.html`（frontend-slides 脚本）
- **部署到 URL**：`bash scripts/deploy.sh 文件夹/`（frontend-slides 脚本）
- **上传 PPTX**：标准方式

---

## 三、资源引用路径

### PPT制作项目资源（主力）
```
D:/桌面/PPT制作/assets/
├── base.css                → <link rel="stylesheet" href="assets/base.css">
├── fonts.css               → <link rel="stylesheet" href="assets/fonts.css">
├── runtime.js              → <script src="assets/runtime.js"></script>
├── themes/                 → 36 个主题，选一个内联 <style> 或 <link>
├── animations/
│   ├── animations.css      → <link rel="stylesheet" href="assets/animations/animations.css">
│   ├── fx-runtime.js       → <script src="assets/animations/fx-runtime.js"></script>
│   └── fx/*.js             → 20 canvas 特效
├── template-packs/            → 34 个设计模板（色系/氛围分类）
├── full-decks/                → 15 个完整 deck（用途分类）
├── layouts/                   → 31 种单页布局（功能分类）
└── references/                → 4 个参考文件（原 frontend-slides）
```

### full-decks（assets 内）
```
assets/full-decks/{business,tech,social,academic,special}/<name>/
```

### layouts（assets 内）
```
assets/layouts/{cover,content,data,process,media,special}/<name>.html
```

### frontend-slides 参考（assets 内）
```
assets/references/
├── viewport-base.css        → 必须全量包含到每个演示中
├── html-template.md         → HTML 架构参考
├── STYLE_PRESETS.md         → 12 种视觉预设
└── animation-patterns.md    → 动画模式参考
```

### template-packs（assets 内）
```
assets/template-packs/{light,dark,mixed}/{mood}/<name>/
```

### ui-ux-pro-max 设计查询
```bash
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<主题>" --design-system
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain style
python3 ~/.claude/skills/ui-ux-pro-max/scripts/search.py "<关键词>" --domain color
```

---

## 四、中文排版规则（所有 HTML 路径通用）

1. 在 `<style>` 中添加 `word-break: keep-all;` 防止中文在字符间断开
2. 短关键词（不超过 15 字）用 `<span class="nobr">` 强制不断行
3. **超过 15 字的短语禁用 `.nobr`**，否则会溢出重叠
4. `.nobr { white-space: nowrap; }` 定义在 CSS 中
5. 适合 `.nobr` 的场景：短数字短语（"1927年7月"）、地名组合（"北京、上海"）、专有名词（"中国共产党"）、`<br>` 分行的每行 ≤12 字
6. 字体栈包含中文后备：`'Inter','Noto Sans SC',sans-serif` / `'Playfair Display','Noto Serif SC',serif`
7. 纯中文演示使用 `Noto Sans SC` / `Noto Serif SC`
8. 幻灯片内边距至少 80px（中文排版需要）
9. deck header 与内容的间距至少 70px

详细参考：`references/chinese-typography.md`

---

## 五、快速参考

| 场景 | 路径 | 参考文件 |
|------|------|---------|
| 日常汇报/课件 | html-ppt-skill | `references/quick-start-guides/html-ppt-skill.md` |
| 单文件分享 | frontend-slides | `references/quick-start-guides/frontend-slides.md` |
| 漂亮首页/全页 | beautiful-template | `references/quick-start-guides/beautiful-template.md` |
| 论文组会汇报 | nature-paper2ppt | `references/quick-start-guides/nature-paper2ppt.md` |
| 不确定风格 | ui-ux-pro-max | `references/template-catalog.md` |
| 模板浏览 | 统一目录 | `references/template-catalog.md` |
| 架构路由 | 决策树 | `references/architecture-routing.md` |
