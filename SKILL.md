---
name: qiudengs-svg-diagrams
description: Create standalone SVG diagrams with minimal shapes, direct connections, and muted colors for software requirements and system design. Use for context, use-case, flow, state, sequence, data relationship, component, and wireframe diagrams. Not for raster images or data charts.
---

# Qiudeng's SVG Diagrams

为软件需求分析和系统设计生成便于审阅的 SVG 图。以简约框图为基础，使用白底、清楚的文字、直接连线和低饱和度配色。

## 输出与依赖

直接编写独立 SVG，无需安装工具或依赖。不生成 PNG，不提供格式转换流程。使用系统字体回退，不嵌入字体或位图。

模板是 SVG 风格示例，不是 draw.io 原生文件。发布平台是否支持 SVG 需单独确认，不能把浏览器可打开等同于平台可嵌入。

## 工作方式

1. 明确图要回答的问题、读者和范围，根据实际需求选图，不要求每种都画。
2. 读取对应 SVG 源码和 [绘图规则](references/drawing-rules.md)，只加载本次相关模板。
3. 用真实业务内容替换示例；先根据直接、共享和专属关系安排节点与分组，再画连线，为分组标识预留独立空间。参考[分组标识与关系布局正反例](references/drawing-rules.md#分组标识与关系布局)。模板用于学习视觉语法，不是已确认的项目需求或固定版式。
4. 先检查业务语义，再检查布局。内容过多时拆图，不靠缩小字体解决。
5. 检查 XML 和引用。已有浏览器预览能力时检查实际呈现；没有时明确说明未目视检查，不为此安装依赖。
6. 交付 SVG 链接和必要注释，说明省略范围与待确认条件。

## 选图与模板

- [系统上下文图](assets/context.svg)：系统与哪些参与方交互，边界在哪里？
- [用例图](assets/use-case.svg)：用户能够在系统中完成什么？
- [业务流程图](assets/flow.svg)：一次请求怎样完成，条件不满足时怎么办？
- [状态图](assets/state.svg)：一个生成请求如何响应事件并改变状态？
- [关键时序图](assets/sequence.svg)：哪些组件先后协作，回答与结算何时发生？
- [数据关系图](assets/er.svg)：业务对象怎样关联，关系的数量约束是什么？
- [组件架构图](assets/components.svg)：职责如何拆分，哪些依赖跨越边界？
- [页面线框图](assets/wireframe.svg)：用户在哪里看信息、选择模型并发送消息？

## 审阅前检查

- 标签、方向、分支条件和基数有业务依据，不从模板推断需求。
- 短重试回环优先用相邻状态间的近邻反向连线，在线上写“失败重试”；不要用多余失败矩形制造尖锐三角回环。确有独立业务意义的失败状态应保留，见[状态图正反例](references/drawing-rules.md#短重试回环用近邻反向连线表达)。
- 文字有余量，连线不穿过节点或标签，箭头连接目标边缘。
- 同级元素的间距、内边距与对齐方式保持一致；局部调整后复查同类结构。差异须有明确的表达需要，见[布局节奏](references/drawing-rules.md#同级元素采用一致的布局节奏)。
- 区分既有实现、拟议设计与待确认内容，不只依靠颜色。
- 配色、分组和连线风格在设计时保持一致，不在成图中添加这些设计说明。必要的业务关系标记（如 «include»）直接放在对应连线上。
- 成图保留图名和业务内容，不添加“回答……”副标题或底部绘图说明；图要回答的问题、范围和补充解释留在文档中。不要混淆不同对象的生命周期。
- SVG 只含静态图形和文本，没有脚本、外部资源或 foreignObject。
- 有 title、desc、viewBox 和可独立打开的完整样式。

## 样例预览

[README.md](README.md) 展示 SVG 模板及正反例，可在仓库页面直接浏览。单个 SVG 也可直接用浏览器打开，无需开发服务器。
