---
name: global-ecommerce-product-intelligence
description: 当用户需要分析某个行业、品类或具体产品在全球市场、美国市场或各大电商平台上的销售表现、竞品格局、公开可见真实用户评价、差评痛点、产品机会、选品方向、Amazon/TikTok Shop/Walmart/eBay/Etsy/AliExpress/Temu/Shopify 等平台表现时使用。适合做跨境电商选品、市场调研、竞品分析、评论采集、评论洞察、产品改良、卖点提炼和机会报告。
---

# Global Ecommerce Product Intelligence

这个技能用于帮助用户回答两类问题：

1. 某个行业或品类里，哪些产品在全球或美国市场卖得更好，为什么
2. 某款特定产品在各大电商平台上的公开评价是什么，用户到底满意和不满什么

核心原则：公开平台很少提供完整真实销量。不要把估算说成事实。把结论分成 `观察到的数据`、`合理推断`、`需要验证的假设`。

## 任务路由

先判断用户要做哪种任务：

- `行业/品类机会分析`：例如“厨房收纳在美国什么产品卖得好”
- `单品跨平台评价分析`：例如“帮我看这款折叠凳全球平台评价”
- `公开评价采集`：例如“把这款产品在 Amazon、Walmart、eBay、Etsy 的评论抓出来”
- `竞品对比`：例如“这 5 个 Amazon 产品谁更值得跟”
- `选品评分`：例如“给这些候选产品打分，选前 3 个”
- `产品改良/卖点提炼`：例如“从差评里找产品升级点”
- `完整报告`：例如“做一份进入美国市场的选品报告”

按任务读取对应参考：

- 行业/品类机会分析：读 [market-research-workflow.md](./references/market-research-workflow.md)
- 评论分析：读 [review-intelligence.md](./references/review-intelligence.md)
- 评论采集：读 [public-review-collection.md](./references/public-review-collection.md)
- 评分方法：读 [scoring-models.md](./references/scoring-models.md)
- 平台指标：读 [platform-signals.md](./references/platform-signals.md)
- 报告模板：读 [report-templates.md](./references/report-templates.md)
- 数据格式和脚本：读 [data-schemas.md](./references/data-schemas.md)

## 数据来源优先级

优先使用用户提供的数据，其次使用公开网页和公开榜单，再使用第三方工具导出。

可用数据类型：

- 商品链接、搜索结果页、榜单页、店铺页
- 商品标题、价格、评分、评论数、销量展示、Best Sellers Rank、上架时间
- 评论文本、评分、评论时间、变体、地区、是否 Verified Purchase
- Google Trends、社媒讨论、YouTube/TikTok 内容热度
- Keepa、Helium 10、Jungle Scout、Similarweb、卖家后台、广告后台等导出文件

如果需要最新平台页面、榜单、价格、评论、销量代理指标，必须联网验证，不要依赖记忆。

## 评论采集规则

这个技能包包含“评论采集 + 评论分析”两段：

1. `评论采集`：从平台公开可见页面、榜单页、商品页、评论页或用户导出文件中收集评论
2. `评论分析`：把评论标准化后做主题、评分、痛点和机会分析

能做的采集范围：

- 平台公开可见、无需违规绕过即可访问的评论页
- 用户提供的评论 CSV/JSON 导出
- 用户提供的一组商品链接，由 Codex 逐个平台整理评论

不能默认做的事：

- 绕过登录墙、验证码、反爬限制
- 未授权读取浏览器 cookies
- 抓取平台后台、付费工具私有数据、受限 API

如果用户要求“看全球各平台真实评价”，默认理解为：

- 优先收集 `公开可见评价`
- 需要时辅以用户授权的登录态或用户提供的导出文件
- 输出时明确说明样本来源和覆盖范围

## 销量判断规则

把“卖得好”拆成多个信号，不要只看单一指标：

- `需求热度`：搜索趋势、榜单出现频率、社媒热度
- `平台表现`：排名、评论增长、销量展示、类目位置、店铺表现
- `购买转化迹象`：评分、评论数、近期评论密度、收藏/点赞/售出记录
- `竞争强度`：同质化数量、价格战、广告密度、头部品牌集中度
- `利润空间`：价格带、体积重量、材料复杂度、退货风险、售后风险

公开数据只能估算销量。输出时用：

- `高置信观察`：页面直接显示的数据
- `中置信推断`：多个平台信号一致
- `低置信假设`：样本少或数据缺口大

## 评论分析规则

评价分析不是简单数好评差评。每次都要提炼：

- 用户购买这个产品的真实动机
- 好评中反复出现的满意点
- 差评中反复出现的痛点
- 质量、尺寸、材质、安装、物流、包装、售后、性价比等主题
- 哪些问题是产品本身，哪些是预期管理或详情页表达问题
- 哪些卖点可以写进标题、主图、五点描述、短视频脚本
- 哪些差评能转化为产品改良机会

如果用户提供 CSV/JSON 评论数据，优先用：

```bash
./scripts/analyze_reviews.py reviews.csv -o review-analysis.md
```

如果评论来自不同平台、字段不统一，先标准化：

```bash
./scripts/normalize_marketplace_reviews.py reviews.csv -o normalized-reviews.csv
./scripts/analyze_reviews.py normalized-reviews.csv -o review-analysis.md
```

## 选品输出要求

默认输出要能帮助用户做决策，而不是只讲市场概况。至少包含：

1. `结论先行`：是否值得继续研究/进入
2. `证据表`：关键数据来自哪里
3. `头部产品/竞品`：谁在卖，卖什么价位，靠什么赢
4. `用户评价洞察`：好评驱动和差评痛点
5. `机会点`：可差异化的产品、内容、价格、渠道或服务
6. `风险`：合规、物流、售后、季节性、平台规则、同质化
7. `下一步验证`：还需要抓什么数据、做什么小测试

## 常用脚本

- `scripts/check_inputs.py`：检查 CSV/JSON 字段是否可用于分析
- `scripts/analyze_reviews.py`：评论清洗、主题统计、评分分布、可疑评论提示
- `scripts/normalize_marketplace_reviews.py`：把 Amazon/Walmart/eBay/Etsy/AliExpress/Temu/TikTok Shop 等评论导出统一成标准字段
- `scripts/score_products.py`：按代理指标给候选产品打分并排序
- `scripts/make_research_brief.py`：从产品评分和评论分析结果生成报告骨架

## 安全与合规

- 遵守平台条款和 robots 限制；不要绕过登录、验证码、付费墙或反爬机制
- 用户未明确授权时，不要读取浏览器 cookies、后台数据或付费工具账号
- 不要把估算销量说成真实销量
- 不要输出平台不允许的刷评、操纵评论、规避风控建议
- 涉及法律、税务、合规、认证、知识产权时，给出风险提醒并建议专业确认

## 何时不要使用

- 用户只要普通翻译、文案润色，且不涉及市场/产品/评价分析
- 用户要求获取非公开后台数据但没有授权
- 用户要求违规抓取、绕过平台限制、操纵评价
