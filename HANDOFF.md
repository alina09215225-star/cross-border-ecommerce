# Handoff

## 当前状态

本仓库已经把跨境电商相关资料从本机 Codex 工作目录整理为可同步结构，适合通过 GitHub private repo 在不同电脑之间继续工作。

本地仓库路径：

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

## 维护规则

- 不提交 `.env`、API key、密码、账号 cookie、浏览器 profile。
- 可以提交稳定的 Markdown、脚本、模板、研究报告和压缩归档。
- 每次重要进展都更新 `HANDOFF.md`，让另一台电脑能接上。
- 方向包保持版本化命名，例如 `xxx-v1`、`xxx-v2`。

