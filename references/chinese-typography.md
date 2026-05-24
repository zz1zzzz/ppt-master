# 中文排版规则（HTML 幻灯片通用）

应用于所有 HTML 输出路径（html-ppt-skill、frontend-slides、beautiful-template 适配）。

---

## 核心规则

### 1. 禁止字内断行

```css
/* 在 <style> 中添加 */
html {
  word-break: keep-all;
  /* 自动在标点处换行，不在中文字符间断开 */
}
```

### 2. 短关键词强制不断行

```css
.nobr { white-space: nowrap; }
```

```html
<!-- ✅ 正确用法：短数字短语、地名组合、专有名词 -->
<span class="nobr">1921年7月</span>
<span class="nobr">50+ 名成员</span>
<span class="nobr">北京、上海、深圳</span>
<span class="nobr">中国共产党</span>
<span class="nobr">机器学习</span>

<!-- 手动 <br> 分行的每行 ≤12 字时可用 -->
<span class="nobr">坚守信仰</span><br>
<span class="nobr">不畏牺牲</span>
```

### 3. 长短语禁止使用 nobr（🔴 硬性规则）

**超过 15 字的短语禁止用 `.nobr`**，否则在小屏幕上会溢出重叠。

```html
<!-- ❌ 错误：长短语用 nobr 导致溢出 -->
<p class="nobr">这是非常长的一句话会导致在小屏幕上溢出重叠</p>

<!-- ✅ 正确：长短语不用 nobr，自动在标点处换行 -->
<p>这是非常长的一句话，会在标点处自动换行，不会溢出重叠。</p>
```

### 4. 字体栈

```css
:root {
  --font-sans: 'Inter', 'Noto Sans SC', -apple-system, sans-serif;
  --font-serif: 'Playfair Display', 'Noto Serif SC', Georgia, serif;
  --font-mono: 'JetBrains Mono', 'Noto Sans SC', monospace;
}
```

- 纯中文演示使用 `Noto Sans SC` / `Noto Serif SC`
- Google Fonts 导入：`@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@400;600;700&display=swap');`
- 无需额外网络时，使用系统后备字体

### 5. 间距

```css
:root {
  --slide-padding: clamp(80px, 5vw, 120px);  /* 中文排版最少 80px */
  --content-gap: clamp(70px, 4vw, 100px);    /* header/内容间距最少 70px */
}
```

---

## 快速检查清单

- [ ] `word-break: keep-all` 已添加
- [ ] 长短语未使用 `.nobr`
- [ ] 字体栈包含中文后备字体
- [ ] 幻灯片内边距 ≥ 80px
- [ ] 在 1280×720 窗口测试无溢出
