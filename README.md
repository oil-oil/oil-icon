<p align="center">
  <img src="./assets/readme/readme-hero.png" width="100%" alt="oil-icon：一次生成一整套，让每个图标都像来自同一个设计师。">
</p>

<p align="center">
  <img src="./assets/readme/readme-section-what.svg" width="100%" alt="02 oil-icon 是什么">
</p>

`oil-icon` 是一个给 Agent 使用的图标生成 Skill。我们只需要说明想要哪些图标、喜欢什么风格，或把项目的配色和页面交给它，它会生成一整套风格统一、背景透明、可以直接使用的 PNG 图标。

上面的两组图标使用了完全相同的 16 个概念：配色、网格、魔法棒、图层、品牌、标签、卡片、分类、空状态、营销、产品、角色、切图、透明背景、质检和导出。改变的是整套的画法，因此一组是柔软 3D，另一组是等轴微缩。

它适合产品功能、分类、营销卡片、空状态和品牌化插图；如果只是制作 16–24px 的按钮小图标，直接使用 Lucide 等矢量图标库会更合适。

<p align="center">
  <img src="./assets/readme/readme-section-consistency.svg" width="100%" alt="03 为什么整套生成更统一">
</p>

让模型一张一张画，后面的图标很容易忘记前面的线宽、圆角、视角和颜色。`oil-icon` 把 16 个图标放在同一次生成里，让模型始终看见整套作品；开始画之前，还会先把共同的规则定清楚。

一套图标会共同遵守：

- **同一套画法**：网格、视角、线宽、圆角和繁简程度一致。
- **同一套颜色**：色值直接锁定，避免每一批越画越艳、越画越偏。
- **同一个记号**：反复出现的小火花、切角或其他母题，让图标拥有自己的身份。
- **同一次生成**：16 个图标共享同一段视觉上下文，比逐张生成更容易保持一致。

所以它不是给通用图标换一套颜色，而是先把整套的画法定清楚，再让模型按照这些规则画完。

<p align="center">
  <img src="./assets/readme/readme-section-workflow.svg" width="100%" alt="04 一张图，得到 16 张透明 PNG">
</p>

```text
图标清单 + 风格或项目素材
          ↓
定好颜色、视角、圆角和专属记号
          ↓
在纯灰背景生成一张 4×4 图标图
          ↓
自动切成 16 张图片并移除背景
          ↓
在高对比底色检查灰边、串格和一致性
          ↓
交付 16 张透明 PNG
```

硬边图标使用颜色识别清除背景，3D、贴纸等软边图标使用背景移除模型。切图程序只保留每个格子中心的主体，避免把旁边图标的碎片一起带走。

<p align="center">
  <img src="./assets/readme/readme-section-styles.svg" width="100%" alt="05 支持哪些风格">
</p>

| 方向 | 内置风格 | 适合场景 |
| --- | --- | --- |
| 简洁 | 线性、面性 | 工具、设置、导航和内容型产品 |
| 平面 | 撞色、卡通、贴纸 | 创意产品、社区、教育和活动 |
| 立体 | 等轴、柔软 3D | 功能介绍、工作台、引导和奖励 |
| 具象 | 写实、动物徽章 | 电商、角色、头像和主题内容 |

也可以不使用预设：`oil-icon` 会读取项目的真实配色、圆角、页面和品牌素材，先整理成一份专属风格规则，再生成与产品匹配的图标。

<p align="center">
  <img src="./assets/readme/readme-section-start.svg" width="100%" alt="06 怎么使用">
</p>

**方式一 · 执行命令**

```bash
npx skills add oil-oil/oil-icon
```

**方式二 · 直接交给 Agent**

把下面这句话发给任何支持 Skill 的 Agent：

```text
请安装这个 Skill：https://github.com/oil-oil/oil-icon
```

安装完成后，可以直接描述图标清单和使用场景：

```text
[$oil-icon] 根据这个产品的页面和配色，生成一套 16 个功能图标。
```

如果没有现成品牌，也可以指定一个方向：

```text
[$oil-icon] 为我的 AI 写作工具生成一套柔软 3D 图标，包含创作、改写、翻译、素材、历史和导出。
```

`oil-icon` 会优先使用 Agent 当前可用的图片生成能力；没有内置图片工具时，再根据环境选择其他生成方式。切图与检查流程保持一致。

<details>
<summary><strong>仓库里有什么</strong></summary>

- `SKILL.md`：完整工作流与执行规则
- `styles/`：内置风格和构造规范
- `reference/`：提示词、品牌适配、图标设计与生成说明
- `scripts/`：环境安装、切图和背景移除工具

</details>

## License

MIT
