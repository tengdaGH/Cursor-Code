# TOEFL Listen & Repeat - Design System Reference

本文档描述了 TOEFL Listen & Repeat 测试界面的视觉设计系统，供未来开发参考。

## 设计系统变量

### CSS 变量定义

所有颜色、尺寸和间距都通过 CSS 变量定义，便于统一管理和主题切换。

```css
:root {
  /* 主色调 - ETS 蓝色系 */
  --ets-blue: #0066b3;           /* 主蓝色 */
  --ets-blue-dark: #004c87;      /* 深蓝色（悬停状态） */
  --ets-blue-light: #e6f2fa;     /* 浅蓝色（背景、高亮） */
  
  /* 背景和卡片 */
  --bg: #f0f2f5;                 /* 页面背景 */
  --card: #ffffff;                /* 卡片背景 */
  --border: #d1d5db;             /* 边框颜色 */
  
  /* 文本颜色 */
  --text: #1a1a1a;               /* 主文本 */
  --muted: #6b7280;              /* 次要文本 */
  
  /* 状态颜色 */
  --success: #10b981;            /* 成功/完成状态 */
  --warning: #f59e0b;            /* 警告/处理中状态 */
  --error: #ef4444;              /* 错误/录音状态 */
  
  /* 尺寸 */
  --header-height: 48px;         /* 顶部导航栏高度 */
}
```

### 字体系统

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
```

使用系统默认字体栈，确保跨平台一致性。

## 组件样式规范

### Header 组件

顶部导航栏，固定高度，ETS 蓝色背景。

```css
.header {
  height: var(--header-height);
  background: var(--ets-blue);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  font-size: 15px;
  font-weight: 600;
  box-shadow: 0 1px 4px rgba(0,0,0,.15);
}
```

### Card 组件

主要内容容器，白色背景，带边框和阴影。

```css
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,.06);
}
```

### Button 组件

#### 主按钮（Primary Button）

```css
.btn {
  padding: 12px 24px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all .2s;
  background: var(--ets-blue);
  color: #fff;
}
.btn:hover:not(:disabled) { 
  background: var(--ets-blue-dark); 
}
.btn:disabled { 
  opacity: .5; 
  cursor: not-allowed; 
}
```

#### 次按钮（Secondary Button）

```css
.btn-secondary {
  background: var(--card);
  color: var(--text);
  border: 1px solid var(--border);
}
.btn-secondary:hover:not(:disabled) {
  background: #f3f4f6;
  border-color: var(--ets-blue);
  color: var(--ets-blue);
}
```

### Screen 容器系统

页面屏幕容器，支持淡入动画。

```css
.screen {
  display: none;
  max-width: 720px;
  margin: 0 auto;
  padding: 20px 16px;
}
.screen.active { 
  display: block; 
}
.screen.fade-in {
  animation: fadeIn 0.3s ease-in;
}
```

### 进度条组件

显示当前进度（如：第几句/共几句）。

```css
.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-bottom: 24px;
  padding: 12px;
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 6px;
}

.progress-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--border);
  transition: all .3s;
}
.progress-dot.active {
  background: var(--ets-blue);
  transform: scale(1.2);
}
.progress-dot.completed {
  background: var(--success);
}

.progress-connector {
  width: 24px;
  height: 2px;
  background: var(--border);
}
.progress-connector.completed {
  background: var(--success);
}
```

### 音频播放器组件

#### 播放进度条

```css
.audio-progress {
  width: 100%;
  max-width: 400px;
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 16px;
}
.audio-progress-bar {
  height: 100%;
  background: var(--ets-blue);
  transition: width 0.1s linear;
}
```

### 录音组件

#### 录音状态显示

```css
.phase-recording {
  border-color: var(--error);
}
.phase-recording .phase-icon {
  font-size: 64px;
  margin-bottom: 16px;
  color: var(--error);
  animation: pulse 1s ease-in-out infinite;
}
.recording-timer {
  font-size: 32px;
  font-weight: 700;
  color: var(--error);
  margin: 16px 0;
  font-variant-numeric: tabular-nums;
}
```

#### 波形可视化

```css
.waveform-container {
  width: 100%;
  max-width: 500px;
  height: 80px;
  margin: 20px 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 3px;
}
.waveform-bar {
  width: 4px;
  background: var(--ets-blue);
  border-radius: 2px;
  transition: height 0.1s;
  min-height: 4px;
}
```

## 状态样式

### 播放中状态（Listening Phase）

```css
.phase-listening {
  border-color: var(--ets-blue);
}
.phase-listening .phase-icon {
  font-size: 64px;
  margin-bottom: 16px;
  animation: pulse 1.5s ease-in-out infinite;
}
```

### 录音中状态（Recording Phase）

```css
.phase-recording {
  border-color: var(--error);
}
```

### 处理中状态（Processing Phase）

```css
.phase-processing {
  border-color: var(--warning);
}
.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--border);
  border-top-color: var(--ets-blue);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}
```

### 完成状态（Scored Phase）

```css
.phase-scored {
  border-color: var(--success);
}
.score-display {
  font-size: 48px;
  font-weight: 700;
  color: var(--success);
  margin-bottom: 8px;
  animation: scoreFlash 0.5s ease-out;
}
```

## 动画效果

### 页面过渡动画

```css
@keyframes fadeIn {
  from { 
    opacity: 0; 
    transform: translateY(10px); 
  }
  to { 
    opacity: 1; 
    transform: translateY(0); 
  }
}
```

### 脉冲动画

用于播放和录音图标的动画效果。

```css
@keyframes pulse {
  0%, 100% { 
    transform: scale(1); 
  }
  50% { 
    transform: scale(1.1); 
  }
}
```

### 加载动画（Spinner）

```css
@keyframes spin {
  to { 
    transform: rotate(360deg); 
  }
}
```

### 分数显示动画

```css
@keyframes scoreFlash {
  0% { 
    transform: scale(0.5); 
    opacity: 0; 
  }
  50% { 
    transform: scale(1.2); 
  }
  100% { 
    transform: scale(1); 
    opacity: 1; 
  }
}
```

## 使用示例

### 基本页面结构

```html
<header class="header">
  <div class="title">TOEFL® Speaking Section</div>
  <div class="progress" id="headerProgress"></div>
</header>

<div class="screen active">
  <div class="card">
    <!-- 内容 -->
  </div>
</div>
```

### 按钮使用

```html
<!-- 主按钮 -->
<button class="btn">Continue →</button>

<!-- 次按钮 -->
<button class="btn btn-secondary">Cancel</button>

<!-- 禁用状态 -->
<button class="btn" disabled>Disabled</button>
```

### 进度条使用

```html
<div class="progress-bar">
  <div class="progress-dot completed"></div>
  <div class="progress-connector completed"></div>
  <div class="progress-dot active"></div>
  <div class="progress-connector"></div>
  <div class="progress-dot"></div>
</div>
```

### 状态显示

```html
<!-- 播放中 -->
<div class="sentence-phase phase-listening">
  <div class="phase-icon">🔊</div>
  <div class="phase-text">Playing audio...</div>
</div>

<!-- 录音中 -->
<div class="sentence-phase phase-recording">
  <div class="phase-icon">🎙️</div>
  <div class="recording-timer">00:15</div>
  <div class="waveform-container"></div>
</div>

<!-- 处理中 -->
<div class="sentence-phase phase-processing">
  <div class="spinner"></div>
  <div class="phase-text">Analyzing...</div>
</div>
```

## 响应式设计

所有组件都使用相对单位和 flexbox，确保在不同屏幕尺寸下正常显示。

- 最大宽度：720px（卡片容器）
- 内边距：20px 16px（屏幕容器）
- 字体大小：使用相对单位（rem/em）或固定像素值

## 颜色使用指南

- **ETS 蓝色**：主要操作、链接、强调
- **深蓝色**：悬停状态、重要文本
- **浅蓝色**：背景高亮、表格标题
- **成功绿色**：完成状态、正确标记
- **警告橙色**：处理中状态
- **错误红色**：录音状态、错误提示
- **灰色**：边框、禁用状态、次要文本

## 注意事项

1. 所有交互元素都应该有明确的视觉反馈（hover、active 状态）
2. 禁用状态应该降低不透明度（opacity: 0.5）
3. 动画应该流畅但不干扰用户操作
4. 保持一致的间距和圆角（8px 圆角，24px 内边距）
5. 确保足够的对比度以满足可访问性要求
