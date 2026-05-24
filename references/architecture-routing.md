# 架构路由与冲突预防参考

详细版决策树 + 三大引擎架构对比 + 冲突场景处理。

---

## 一、三大引擎架构对比

| 维度 | html-ppt-skill | frontend-slides | nature-paper2ppt |
|------|---------------|----------------|------------------|
| **输出格式** | 多 HTML 文件 + 外部 assets | 单 HTML 文件（全内联） | .pptx 文件 |
| **CSS 引用** | `<link>` 外部 | 内嵌 `<style>` | N/A |
| **JS 引用** | `<script src="assets/runtime.js">` | 内嵌 `<script>` | N/A |
| **导航系统** | runtime.js（键盘/演讲者/主题切换） | 自建 SlidePresentation 类 | PowerPoint |
| **字体** | Google Fonts CDN + 后备 | Fontshare / Google Fonts | PowerPoint |
| **模板来源** | 36 themes + 15 full-decks + 31 layouts | 无模板库，参考 STYLE_PRESETS | — |
| **Canvas 特效** | ✅ 20 种 via data-fx | ❌ 不可用 | ❌ |
| **演讲者模式** | ✅ S 键弹出窗口 | ❌ 无 | ❌ |
| **主题切换** | ✅ T 键实时切换 | ❌ 编译时确定 | ❌ |
| **动画** | ✅ 27 CSS + 20 Canvas | ✅ 纯 CSS（.reveal） | PowerPoint 动画 |
| **PPT 转换** | ❌ | ✅ extract-pptx.py | N/A（本身就是 PPTX） |
| **导出** | PNG (Chrome) | PDF + Vercel 部署 | PowerPoint |
| **适用场景** | 日常汇报/课件/技术分享 | 单文件分享/邮件/Slack | 学术论文组会 |

## 二、决策树完整版

```
用户提出 PPT 需求
│
├─ 1. 科学论文汇报?（组会/journal club/文献分享/毕业论文答辩）
│   → ROUTE nature-paper2ppt
│   │   输出：.pptx 文件
│   │   例外：用户明确要 HTML 时走 html-ppt-skill
│   │   注意：nature-paper2ppt 会读取论文，提取核心论点，生成中文学术 PPTX
│   │
├─ 2. 需要转 PPTX → HTML?
│   │   （用户有 .pptx 文件，想转成网页版）
│   → ROUTE frontend-slides Phase 4
│   │   使用 extract-pptx.py 提取内容，然后生成自包含 HTML
│   │   pip install python-pptx（如未安装）
│   │
├─ 3. 需要单文件分享?（邮件附件/Slack/嵌入网页）
│   │   "只要一个 .html 文件"
│   → ROUTE frontend-slides 路径
│   │   ⚠ 禁止引用外部 assets（base.css / runtime.js）
│   │   ✅ 所有 CSS 写在 <style>
│   │   ✅ 所有 JS 写在 <script>
│   │   ✅ 全量包含 viewport-base.css
│   │
├─ 4. 功能丰富的 HTML deck?
│   │   "要键盘翻页/演讲者模式/主题切换/特效"
│   → ROUTE html-ppt-skill 路径（主力路线）
│   │   ✅ 复制 D:/桌面/PPT制作/assets/ 到项目
│   │   ✅ fonts.css → base.css → animations.css → runtime.js
│   │   ⚠ 禁止内联 assets 文件
│   │   ⚠ 禁止自写导航 JS
│   │   💡 推荐：presenter-mode-reveal（带逐字稿）
│   │
├─ 5. 用漂亮模板做首页/全页?
│   │   "我看中那个 xx 风格的模板"
│   → ROUTE beautiful-html-template
│   │   先检查 template.html 的结构：
│   │   ├─ 如果自包含（CSS 内联）→ 保持自包含
│   │   └─ 如果外部引用 → 保持外部引用
│   │   参考 design.md 了解设计理念
│   │
├─ 6. 不确定风格?
│   → 查询 ui-ux-pro-max search.py
│   │   python3 scripts/search.py "<主题>" --design-system
│   │   根据结果选择 theme 或模板
│   │
└─ 7. 以上都不是?
    → 默认 html-ppt-skill（能力最全面）
    → 推荐 presenter-mode-reveal
```

## 三、冲突场景处理

### 场景 A：用户在 html-ppt-skill 项目中想要 frontend-slides 的某个功能

❌ **不行。** runtime.js 和 frontend-slides 的内联 JS 控制器不兼容。解决方案：
- 如果是想要**设计风格**：用 ui-ux-pro-max 查询，然后应用到 html-ppt-skill 的 theme
- 如果是想要**单文件导出**：用 html-ppt-skill 完成后，复制一份用 frontend-slides 样式重制

### 场景 B：用户在 frontend-slides 单文件中想要 Canvas 特效

❌ **不行。** Canvas FX 依赖于 `assets/animations/fx-runtime.js`，而 frontend-slides 是单文件模式。解决方案：
- 要么切换为 html-ppt-skill 路径
- 要么使用纯 CSS 动画替代（`.reveal` 类）

### 场景 C：用户想把 beautiful-template 放入现有项目

✅ 可以。但要看模板类型：
- 自包含模板：作为独立 HTML 文件放在项目中，单独打开
- 外部引用模板：统一使用项目的 assets/，不要复制模板自己的 CSS

### 场景 D：用户想用 nature-paper2ppt 但输出 HTML

✅ 可以。用 nature-paper2ppt 理解论文结构，然后用 html-ppt-skill 重建为 HTML，逐字稿写在 `<div class="notes">` 中。

## 四、快速决策口诀

```
论文汇报 → PPTX（nature-paper2ppt）
单文件 → 内联（frontend-slides）
要功能 → 外部引用（html-ppt-skill + assets）
要模板 → 看结构（保持原架构）
不确定 → html-ppt-skill
