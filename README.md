# 实时交互黑洞模型

一个可直接在现代浏览器运行的 WebGL 1 黑洞教学模型。它包含引力光线弯曲、薄吸积盘、光子临界辉光、Kerr ISCO 读数、引力红移和相对论多普勒增亮，并支持实时调整质量、自旋、吸积率与观测倾角。

## 运行

最简单的方式是直接打开 `index.html`。也可以在项目目录启动本地静态服务器：

```bash
python3 -m http.server 8000
```

然后访问 `http://localhost:8000/`。

## 交互

- 质量：改变物理尺度、ISCO 周期与动画时间尺度。
- 自旋：改变 Kerr 事件视界、顺行 ISCO 与启发式帧拖曳。
- 吸积率：同时改变盘面亮度、近似色温与临界辉光；0% 时盘面辐射消失。
- 观测倾角：高倾角时更容易看出相对论多普勒明暗不对称。
- 画布拖动：改变方位角和倾角。
- 滚轮或触控板：缩放。
- 暂停运动：冻结盘面细丝和团块的差分旋转。

如果系统启用了“减少动态效果”，模型会显示“减少动态 · 点击启动”并默认暂停。点击“启动运动”即可显式播放。

## 本轮修复

- 用有界色调映射替代“背景色加发光色再硬截断”，避免浅色主题及中高吸积率下整片饱和。
- 采用近似 `T ∝ Ṁ^(1/4)`，让吸积率同时影响伪色温和亮度。
- 使用统一轨道相位驱动非轴对称螺旋细丝与团块，形成可辨识的差分旋转。
- 提高低帧率下的时间步上限，避免 GPU 较慢时动画相位几乎停止。
- 保留暂停、后台/离屏暂停、动态分辨率、着色器 96/64/48 步降级和 WebGL 上下文恢复。

## 相对论处理

盘面使用特殊相对论多普勒因子：

```text
δ = 1 / [γ(1 − βμ)]
```

它与引力红移近似合并为总频移 `g`，再以 `g³` 调制比强度。顺行 ISCO、事件视界半径和内盘周期使用 Kerr 解析公式。

实时光线弯曲仍采用“Schwarzschild 各向同性光学曲率 + 启发式帧拖曳”的混合模型，并不是完整 Kerr 零测地线或科研级辐射传输计算。

## 验证

运行无依赖测试：

```bash
node tests/model.test.js
```

测试覆盖：

- HTML fragment 和 JavaScript 语法结构；
- 关键着色器修复是否存在；
- Kerr 顺行 ISCO 的边界和单调性；
- 吸积率亮度映射与色温的单调变化；
- 默认参数下 1.5 秒内的可见螺旋相位位移。

## 项目结构

```text
index.html                              独立运行页面
src/black-hole-accretion-motion-lab.html  可编辑的 Codex HTML fragment
tests/model.test.js                     无依赖验证脚本
output/pdf/black-hole-model-guide-zh.pdf  详细中文原理与使用文档
build_black_hole_guide.py               PDF 生成脚本
```

## 文档

详细公式、算法流程、实验方法、性能设计、局限性与故障排查见 [`output/pdf/black-hole-model-guide-zh.pdf`](output/pdf/black-hole-model-guide-zh.pdf)。

重新生成 PDF 需要 ReportLab：

```bash
python3 -m pip install reportlab
python3 build_black_hole_guide.py
```

脚本会优先使用 macOS 中文字体；其他系统会回退到 ReportLab 的 `STSong-Light` CID 字体。
