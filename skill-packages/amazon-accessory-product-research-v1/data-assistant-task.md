# 数据助手任务单：Amazon 配件调研

## 任务 1: 关键词树

字段：

```csv
main_product,brand_or_ecosystem,seed_keyword,accessory_keyword,pain_keyword,compatibility_keyword,search_intent,notes
```

要求：

- 每个主品至少 20 个关键词
- 区分主品词、配件词、痛点词、兼容词
- 标记是否包含品牌词和潜在 IP 风险

## 任务 2: 搜索结果采样

字段：

```csv
keyword,rank,ad_or_organic,product_title,brand,seller,price,rating,review_count,coupon,delivery_method,product_url,main_image_note,compatibility_note
```

要求：

- 每个关键词采样前 20 个结果
- 标记 Sponsored 和自然结果
- 不把排名等同真实销量

## 任务 3: 竞品矩阵

字段：

```csv
competitor,product_url,brand,price,rating,review_count,variant_count,bundle_type,main_selling_points,listing_strength,main_weakness,qa_fit_issues,low_star_review_themes,ip_risk_note
```

要求：

- 每个方向至少 5 个竞品
- 至少包含 2 个头部竞品、2 个中腰部竞品、1 个弱竞品

## 任务 4: 评论和 Q&A 痛点

字段：

```csv
product_url,source_type,rating_or_question,review_date,theme,summary,impact_on_purchase,fix_type,opportunity
```

主题：

- fit_compatibility
- size_dimension
- quality_durability
- material_smell_safety
- installation_use
- packaging_shipping
- value_price
- unclear_listing

## 任务 5: 供应端粗查

字段：

```csv
accessory_idea,supplier_platform,supplier_url,moq,unit_cost,material,customization_option,packaging_option,lead_time,quality_risk,notes
```

供应端平台：

- 1688
- Alibaba
- AliExpress
- Temu 仅看同质化和低价竞争，不作为稳定供应商结论

## 任务 6: 评分表

字段：

```csv
accessory_idea,total_score,search_demand,main_product_heat,competitor_weakness,review_opportunity,margin_space,compatibility_clarity,ip_compliance_control,listing_differentiation,data_confidence,decision,next_gap
```

决策标签：

- prioritize_validation
- needs_more_data
- watchlist
- reject
