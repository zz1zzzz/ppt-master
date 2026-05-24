# nature-paper2ppt 快速参考（学术论文 → PPTX）

## 适用场景

- 组会汇报（journal club）
- 文献分享
- 论文答辩
- 学术会议报告

## 工作流

```
1. 提供论文（PDF / DOI / arXiv ID / 粘贴文本）
2. nature-paper2ppt 读取论文，提取核心论点
3. 生成中文学术汇报 .pptx
   - 含封面、背景、方法、结果、讨论、总结
   - 含图文混排
   - 含中文讲稿
```

## 输出

| 项目 | 内容 |
|------|------|
| 格式 | `.pptx` |
| 语言 | 中文（幻灯片）+ 英文（术语保留） |
| 页数 | 按论文长度，通常 8-15 页 |
| 讲稿 | 写入 speaker notes |

## 如果需要 HTML 版本

用 nature-paper2ppt 理解论文结构后，切换到 `html-ppt-skill` 路径重建为 HTML：

```
nature-paper2ppt 分析论文 → 提取论点结构
        ↓
html-ppt-skill 重建 → 每页对应一个 <section class="slide">
        ↓
逐字稿写入 <div class="notes">
```

## 注意事项

- 需要网络？nature-paper2ppt 需要读取论文 PDF
- 输出是 .pptx，不是 HTML
- 如需 Canvas 特效/演讲者模式等 HTML 特性，切换到 html-ppt-skill 路径
