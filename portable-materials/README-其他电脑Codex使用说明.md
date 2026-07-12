# 其他电脑 Codex 使用说明

## 目的

这套物料用于让另一台电脑上的 Codex 快速继承当前跨境学习体系，尤其是美国汽配大单品方向。

## 包含内容

- `archives/crossborder-learning-distributor-skill-2026-07-12.tar.gz`
  - Codex 本地技能：跨境学习沉淀与四能手分发。
- `archives/crossborder-knowledge-role-pack-2026-07-12.tar.gz`
  - 完整备份包，体积较大。
- `archives/crossborder-knowledge-role-pack-lite-2026-07-12.tar.gz`
  - 推荐使用的轻量包，只包含知识库和四能手 Markdown 物料。
- `prompts/四能手启动提示词.md`
  - 给策略、数据、运营、视觉四个 Codex 的固定开工提示词。
- `scripts/install_crossborder_materials.sh`
  - 在新电脑上安装物料的脚本。
- `manifests/物料清单-2026-07-12.md`
  - 本次打包清单和版本说明。

## 新电脑安装

在新电脑上，把整个 `跨电脑Codex物料` 文件夹放到任意位置，然后执行：

```bash
bash scripts/install_crossborder_materials.sh
```

安装后，其他电脑的 Codex 应先读取：

```text
~/.codex/skills/crossborder-learning-distributor/SKILL.md
~/Desktop/创收/跨境/技能包/策略（选品）能手/_最新更新.md
~/Desktop/创收/跨境/技能包/数据能手/_最新更新.md
~/Desktop/创收/跨境/技能包/运营能手/_最新更新.md
~/Desktop/创收/跨境/技能包/视觉能手/_最新更新.md
```

## 使用原则

不要让每个助手重新学习全部课程。每次开工前只需要让它：

1. 读取自己角色文件夹的 `_最新更新.md`。
2. 读取 `_索引.md`。
3. 只打开和当前任务相关的技能包。
4. 按技能包执行。
