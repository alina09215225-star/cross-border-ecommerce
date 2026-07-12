# Handoff

## 当前状态

本仓库已经把跨境电商相关资料从本机 Codex 工作目录整理为可同步结构，适合通过 GitHub private repo 在不同电脑之间继续工作。

2026-07-12 已补充美国汽配大单品方向的 v2/v3 学习沉淀：

- `knowledge-base/`: 课程学习、方法论和分发记录。
- `role-packs/`: 策略（选品）、数据、运营、视觉四个能手的最新技能包镜像。
- `skill-packages/us-auto-accessories-amazon-v2/`: 《跨境汽配选品逻辑》课程沉淀。
- `skill-packages/us-auto-accessories-bilibili-batch-v3/`: B 站美国汽配大单品课程批量学习沉淀。
- `portable-materials/`: 给其他电脑 Codex 使用的 README、提示词、安装脚本和轻量归档。

本地仓库路径：

当前电脑：

`/Users/yongliangfei/Documents/Playground/cross-border-ecommerce`

历史来源路径：

`/Users/admin/Documents/Codex/2026-05-24/new-chat/cross-border-ecommerce`

远程仓库计划使用：

`https://github.com/alina09215225-star/cross-border-ecommerce.git`

## 五个能手分工

### 学习能手

路径：`agents/learning/`

当前已放入 `bilibili-course-learning`，用于课程学习、字幕整理、知识点提取和行动计划生成。

### 策略（选品）能手

路径：`agents/strategy-selection/`

后续用于沉淀平台选择、品类判断、选品框架和机会排序。当前具体策略内容主要在 `skill-packages/` 里的方向包中。

### 数据能手

路径：`agents/data-analysis/`

当前已放入 `global-ecommerce-product-intelligence`，用于市场研究、评论分析、竞品信号、产品评分和报告生成。

### 运营能手

路径：`agents/operations/`

后续用于沉淀刊登、履约、库存、客服、账号运营和日常 SOP。当前具体运营内容主要在各方向包的 `operations-*.md` 文件中。

### 视觉能手

路径：`agents/visual-creative/`

后续用于沉淀主图、详情页、广告图、短视频脚本、素材规范和视觉测试流程。当前具体视觉内容主要在各方向包的 `visual-creative-assistant.md` 文件中。

## 另一台电脑如何继续

1. 安装并登录 GitHub。
2. clone 仓库：

```bash
git clone https://github.com/alina09215225-star/cross-border-ecommerce.git
```

3. 在 Codex 里打开 clone 下来的 `cross-border-ecommerce` 文件夹。
4. 新线程第一句话可以说：

```text
请先阅读 HANDOFF.md，然后按跨境电商五个能手结构继续工作。
```

如果要在另一台电脑恢复本机的跨境知识库和四能手目录，先读：

```text
portable-materials/README-其他电脑Codex使用说明.md
portable-materials/prompts/四能手启动提示词.md
```

## 维护规则

- 每次开始仓库工作前先运行 `git pull`。
- 不提交 `.env`、API key、密码、账号 cookie、浏览器 profile。
- 可以提交稳定的 Markdown、脚本、模板、研究报告和压缩归档。
- 每次重要进展都更新 `HANDOFF.md`，让另一台电脑能接上。
- 方向包保持版本化命名，例如 `xxx-v1`、`xxx-v2`。
- 不执行任何付款、充值、投放扣费、下单等和钱相关的操作。
- 稳定可复用的方法要沉淀到对应能手目录、`shared/` 或 `skill-packages/`。
- 大体积完整备份包默认不提交；优先提交 Markdown 和轻量安装包。

## 最近交接记录

### 2026-06-30

- 已在当前电脑克隆仓库到 `/Users/yongliangfei/Documents/Playground/cross-border-ecommerce`。
- 已确认入口文档为 `README.md` 和 `HANDOFF.md`。
- 已补充仓库级 `AGENTS.md`，固化安全边界、五个能手结构和提交维护规则。
