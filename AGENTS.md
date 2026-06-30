# AGENTS.md

## 工作原则

- 不泄漏密码、密钥、API key、cookie、浏览器 profile 或其他敏感信息。
- 不操作任何和钱相关的动作，包括下单、付款、充值、退款、广告投放扣费、订阅购买等。
- 目标导向，注重结果；用户没有明确说停止时，持续推进到任务可交付。
- 每次开始仓库工作前先同步远程最新内容。
- 重要修改完成后，先更新 `HANDOFF.md`，再提交并推送。
- 主动复盘可复用流程，把稳定方法沉淀为模板、SOP 或技能包。

## 仓库工作流

1. 开始前运行 `git pull`。
2. 先阅读 `README.md` 和 `HANDOFF.md`。
3. 按五个能手结构归档新内容：
   - 学习能手：`agents/learning/`
   - 策略选品能手：`agents/strategy-selection/`
   - 数据能手：`agents/data-analysis/`
   - 运营能手：`agents/operations/`
   - 视觉能手：`agents/visual-creative/`
4. 完整方向包放入 `skill-packages/`，使用版本化目录名，例如 `xxx-v1`、`xxx-v2`。
5. 跨能手共用模板、术语和评分框架放入 `shared/`。

## 禁止提交

- `.env`、`.env.*`
- 密码、API key、私钥、证书、token
- cookie、浏览器 profile、登录态文件
- 任何可能导致资金操作或账号风险的私密配置
