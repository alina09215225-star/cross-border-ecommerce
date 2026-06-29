# 数据格式

## 产品候选 CSV

推荐字段：

```csv
product_title,platform,product_url,brand,price,rating,review_count,sales_count,best_seller_rank,monthly_sales_estimate,listing_age_days,recent_review_count,trend_score,competition_score,margin_score,operations_risk_score,differentiation_score,notes
```

字段说明：

- `price`：售价
- `rating`：评分，通常 1 到 5
- `review_count`：评论数
- `sales_count`：平台公开销量或售出数，如果有
- `best_seller_rank`：Amazon BSR 或类似排名，数字越小越好
- `monthly_sales_estimate`：第三方工具估算销量
- `listing_age_days`：上架天数
- `recent_review_count`：近 30/90 天评论数
- `trend_score`：人工或外部工具给的趋势分，0 到 100
- `competition_score`：竞争可进入性，0 到 100，越高越容易进入
- `margin_score`：利润空间，0 到 100
- `operations_risk_score`：运营风险，0 到 100，越高风险越大
- `differentiation_score`：差异化空间，0 到 100

## 评论 CSV

推荐字段：

```csv
platform,product_id,product_title,brand,rating,review_title,review_text,review_date,variant,country,verified_purchase,helpful_votes,review_url
```

最低字段：

```csv
rating,review_text
```

## 脚本输出

`analyze_reviews.py` 输出 Markdown，包含：

- 样本量
- 评分分布
- 主题统计
- 高频词
- 好评/差评代表性片段
- 可疑评论信号
- 产品改良建议骨架

`normalize_marketplace_reviews.py` 输出标准 CSV，字段固定为：

```csv
platform,product_id,product_title,brand,rating,review_title,review_text,review_date,variant,country,verified_purchase,helpful_votes,review_url
```

`score_products.py` 输出 CSV，包含：

- 原始字段
- 子项评分
- 总分
- 置信度提示
