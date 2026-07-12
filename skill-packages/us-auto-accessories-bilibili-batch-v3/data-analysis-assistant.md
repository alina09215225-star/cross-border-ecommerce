# 数据能手：美国汽配大单品 B站批量学习 v3

## 来源

本技能包来自 10 个 B站课程/视频，重点沉淀数据化选品、市场容量、竞品过滤、利润测算和评论/QA 分析。

## 数据总流程

```text
精准关键词
  ↓
排除干扰数据
  ↓
市场容量
  ↓
竞争结构
  ↓
产品分类
  ↓
价格和新品
  ↓
评论/QA
  ↓
利润
  ↓
结论
```

## 关键词和类目校验

先判断数据是否干净。

必须检查：

- 搜索关键词是否对应目标产品。
- 小类目是否和目标产品一致。
- TOP 产品是否混入无关品。
- 是否有错放类目抢排名的产品。
- 车型过滤后结果是否仍足够。

字段：

```csv
keyword,platform,search_result_count,relevant_result_count,irrelevant_examples,category_match,fitment_filter,clean_data,notes
```

## 市场容量

粗分：

- 高容量：需求大，但价格战和广告战更强。
- 中容量：更适合中小卖家找机会。
- 低容量：谨慎，可能需求不足。

采样字段：

```csv
keyword,category,top_30_monthly_sales,top_100_monthly_sales,bsr_range,trend_12m,trend_5y,capacity_level,seasonality
```

## 竞争结构

字段：

```csv
keyword,brand_concentration,seller_concentration,amazon_or_big_seller_share,china_seller_share,fba_share,fbm_share,new_seller_entry,competition_level
```

判断规则：

- 品牌集中度要结合容量看，不能机械设阈值。
- 高容量市场可以容忍更高集中度。
- 中低容量市场中，少数品牌吃掉大部分份额时谨慎。
- 中国卖家过多且低价明显，容易价格战。

## 产品分类分析

同一个二级类目要继续拆产品类型：

```csv
market,product_subtype,function,appearance,package_type,vehicle_fitment,avg_price,new_launch_count,bsr_entry_count,opportunity
```

重点看：

- 哪个子类型更好卖。
- 新品进入的是低价冲排名，还是功能/外观迭代。
- 是否有套装/组合包机会。

## 评论和 QA

不要只看差评。四星/中评经常反映真实需求。

字段：

```csv
asin,source,rating_or_question,theme,user_need,fitment_issue,install_issue,quality_issue,opportunity,visual_or_listing_fix
```

主题：

- 适配不清。
- 安装困难。
- 尺寸误解。
- 材质/耐用。
- 包装损坏。
- 套装缺件。
- 场景不匹配。

## 利润测算

字段：

```csv
sku,sale_price,landed_cost,fba_fee,referral_fee,storage_fee,ad_cost,coupon_cost,return_allowance,net_profit,net_margin,profit_safe
```

规则：

- 不只看采购价和售价。
- 低价品不适合重促销。
- 价格战市场要模拟低价冲排名后的亏损。
- 退货率和安装客服成本要计入。

## 输出模板

```markdown
# 汽配数据报告

## 结论
推荐/观察/放弃。

## 关键词是否干净
## 市场容量
## 竞争结构
## 产品分类
## 价格和新品
## 评论/QA 机会
## 利润测算
## 风险
## 给策略能手的建议
## 给运营能手的注意事项
## 给视觉能手的素材重点
```
