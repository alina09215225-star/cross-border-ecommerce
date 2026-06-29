# 给数据助手的任务单

## 目标

用公开数据证明“大单品配件”机会是否真实。

## 输入

- 主品方向：用户指定或由策略助手给出
- 市场：默认美国
- 平台：Amazon 优先，补充 TikTok Shop、Walmart、eBay、Etsy、AliExpress、Temu、1688

## 任务 1: 主品生态表

字段：

```csv
main_product,brand_or_ecosystem,market,user_base_signal,trend_signal,main_use_scenarios,accessory_types,ip_risk_notes
```

要求：

- 每个主品至少列 5 个配件方向
- 标记是否涉及品牌兼容风险
- 不把搜索热度或评论数等同于真实销量

## 任务 2: 配件候选池

字段：

```csv
accessory_idea,main_product,platform,keyword,top_competitor_url,price_range,rating_range,review_count_range,visible_sales_signal,main_selling_points,common_complaints,notes
```

要求：

- 每个主品至少 10 个候选配件
- 每个候选至少 3 个竞品证据
- 记录公开可见数据来源

## 任务 3: 评论痛点表

字段：

```csv
platform,product_url,rating,review_date,complaint_theme,review_summary,impact,fix_type,opportunity_note
```

主题分类：

- 兼容/适配
- 质量/耐用
- 尺寸/容量
- 材质/气味/安全
- 安装/使用
- 包装/物流
- 售后/退货
- 价格/性价比

## 任务 4: 利润初算表

字段：

```csv
product,estimated_selling_price,product_cost,packaging_cost,shipping_cost,platform_fee,ad_cost_allowance,return_loss_allowance,gross_margin,net_margin_risk
```

规则：

- 低于 12.99 美元的单品要谨慎，除非能套装化
- 优先看 12.99-39.99 美元价格带
- 标记是否轻小、易碎、易退货

## 任务 5: 机会评分表

字段：

```csv
rank,accessory_idea,main_product,total_score,main_product_heat,accessory_demand,competition_access,review_opportunity,margin_space,differentiation_space,operation_simplicity,data_confidence,decision,next_data_gap
```

输出结论：

- Top 3 优先验证
- Top 4-10 观察
- 明确放弃项和原因
