# beautiful-html-template 快速参考

## 模板结构

每个模板在 `assets/template-packs/<色系>/<氛围>/<name>/` 中包含：

| 文件 | 用途 |
|------|------|
| `template.html` | 完整 deck（10-12 页） |
| `template.json` | 元数据：色调、氛围、适用场合、页数 |
| `design.md` | 设计理念：配色/字体/排版体系 |

## 选择模板

按 `template.json` 的字段匹配：

```json
{
  "mood": ["retro-tech", "playful", "cyberpunk"],
  "occasion": ["gaming pitch", "hackathon demo"],
  "tone": ["geeky", "neon", "rebellious"],
  "formality": "low",
  "scheme": "dark",
  "slide_count": 10
}
```

快速筛选：`scripts/browse_templates.py --occasion "tech sharing"`

## 用法

### 选项 A：单独使用

```bash
cp -r "D:/桌面/PPT制作/assets/template-packs/<色系>/<氛围>/<name>/" "项目名/"
# 直接编辑 template.html 修改内容
```

### 选项 B：作为设计参考

- 阅读 `design.md` 了解配色/字体体系
- 用 `template.json` 的配色方案创建新 theme CSS
- 或手动将颜色/字体应用到 html-ppt-skill 项目

## 关键规则

- ✅ 先检查 template.html 是内联还是外部引用，**保持原架构**
- ✅ 阅读 design.md 理解设计意图再修改
- ⚠ 不要混用架构：自包含模板不接 runtime.js，外部模板不强制改内联
