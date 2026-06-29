# 新电脑安装与验证

## 目标

让另一台电脑上的 Codex 复制本技能后，可以完成：

1. B 站链接直读字幕
2. 无字幕时下载音频
3. 本地 Whisper 转写
4. 生成转写文本和学习稿
5. 基于学习稿继续总结、复盘、出应用方案

## 推荐安装路径

把整个 `bilibili-course-learning` 目录放到：

```bash
~/.codex/skills/bilibili-course-learning
```

安装后重启 Codex，让技能元数据重新加载。

## macOS 依赖

推荐用 Homebrew 安装：

```bash
brew install yt-dlp ffmpeg whisper-cpp
```

也可以直接运行技能内脚本：

```bash
./scripts/setup_macos_runtime.sh
```

## Whisper 模型

本技能默认优先找：

1. `assets/models/ggml-small.bin`
2. `assets/models/ggml-base.bin`
3. `~/.cache/bilibili-course-learning/models/ggml-small.bin`
4. `~/.cache/bilibili-course-learning/models/ggml-base.bin`

建议安装 `small`，中文口语比 `base` 稳；`base` 更快但错字更多。

下载模型：

```bash
./scripts/download_whisper_model.sh small
```

如果机器较弱或只想快速测试：

```bash
./scripts/download_whisper_model.sh base
```

## 环境验证

运行：

```bash
./scripts/check_environment.py
```

期望看到：

- `yt-dlp` 可用
- `ffmpeg` 可用
- `whisper-cli` 可用
- 至少一个 `ggml` 模型文件存在

## 基本测试

用一个 B 站链接测试：

```bash
./scripts/fetch_bilibili_course_material.py "https://www.bilibili.com/video/BVxxxxx" -o /tmp/bili-study
```

如果需要登录态字幕或更高质量音频访问：

```bash
./scripts/fetch_bilibili_course_material.py "https://www.bilibili.com/video/BVxxxxx" -o /tmp/bili-study --cookies-from-browser chrome
```

## 常见问题

### 只有 danmaku，没有字幕

这是正常情况。B 站很多视频没有公开字幕。脚本会自动下载音频并转写。

### 提示没有模型

运行：

```bash
./scripts/download_whisper_model.sh small
```

或手动传入：

```bash
./scripts/fetch_bilibili_course_material.py "URL" -o ./out --whisper-model /path/to/ggml-small.bin
```

### Chrome cookies 读取失败

先让用户明确授权读取浏览器 cookies。没有授权时，不要尝试读取用户登录态。

可替代方案：

- 用户导出 `cookies.txt`
- 用户提供字幕文本
- 用户直接提供音频文件

### 转写有错字

这是 Whisper 模型常见现象。处理学习总结时，应按上下文做轻度纠错，例如：

- `跨境电视` 通常应理解为 `跨境电商`
- `快念商` 通常应理解为 `跨境电商`
- 人名、品牌名和平台名要结合课程主题纠正

不要过度改写事实；不确定的专名应标注“疑似”。
