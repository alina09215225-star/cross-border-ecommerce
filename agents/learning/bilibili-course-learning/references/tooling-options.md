# 现成工具与参考方案

下面这些方案是 2026-05-21 检索时确认过的可参考来源，适合后续增强这个技能包。

## 1. clawdbot / bilibili-transcript

- 来源：`openclaw/skills` 中的 `skills/54lynnn/bilibili-transcript`
- 特点：优先用 CC 字幕，其次 AI 字幕，再退回 Whisper 转写
- 适合：希望自动拿到高质量转写文本
- 备注：依赖 `yt-dlp`、`ffmpeg`、`whisper`，更适合本地环境完整时使用

## 2. openakita / bilibili-watcher

- 来源：`openakita/skills`
- 特点：面向 Bilibili 和 YouTube 的字幕抽取与问答
- 适合：先把视频变成字幕文本，再做总结问答
- 备注：结构轻，适合作为技能思路参考

## 3. guomo233 / bccdl

- 来源：`guomo233/bccdl`
- 特点：专注下载 B 站 CC 字幕
- 适合：只需要字幕、不需要整套笔记生成系统

## 4. indefined / bilibiliCCHelper

- 来源：`indefined/UserScripts`
- 特点：浏览器侧一键复制字幕
- 适合：本地命令行工具没装好，但网页能正常看视频时
- 备注：很适合作为“低门槛应急入口”

## 5. JefferyHcool / BiliNote

- 来源：`JefferyHcool/BiliNote`
- 特点：把视频自动转成结构化 Markdown 笔记
- 适合：想要更完整的视频笔记系统
- 备注：如果后续你要把这个技能升级成完整产品，BiliNote 很值得继续研究

## 当前技能包的选型策略

这个技能包不直接绑定某一个外部项目，而是采用更稳妥的组合思路：

1. 优先接收用户已提供文本
2. 其次兼容字幕文件清洗
3. 再留出接入外部下载/转写工具的扩展位
4. 最后把重点放在“学习与应用”而不是“单纯抓取”

## 当前实现状态

这个本地技能包当前已经内置：

- 字幕清洗脚本
- 分块学习稿生成脚本
- 基于 `yt-dlp` 的 B 站链接字幕提取脚本

还没有内置真正的音频转写模型。如果公开视频没有字幕，后续建议再补：

- `ffmpeg`
- `whisper` 或 `faster-whisper`
