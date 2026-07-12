# 数据能手：美国汽配选品和运营数据分析 v2

## 来源

- 课程：《跨境汽配选品逻辑》BV1T1421r7ps
- 本地文件：`/Users/admin/Documents/Codex/2026-06-28/ku-2/work/course-transcripts/BV1T1421r7ps/quick_transcript.txt`
- 说明：快速转写稿有错字，数据框架按课程逻辑和跨境实操语境校正。

## 数据任务

数据能手负责把汽配选品从“感觉”变成“可验证”：

1. 判断类目是长青、季节、促销、还是高售后。
2. 判断车型/车系是否有美国真实需求。
3. 判断 SKU 数量和销售是否相关。
4. 判断促销后是否仍有利润。
5. 判断哪些 SKU 应该加码，哪些应该下架。

## 季节日历

课程给出的美国汽配大致节奏：

| 时间 | 判断 |
|---|---|
| 1-2 月 | 相对淡季，整体较低 |
| 3-4 月 | 出行季启动，很多汽配类目爆发 |
| 5-6 月 | 仍较好，但弱于 3-4 月 |
| 7 月 | Prime Day 带来促销波峰 |
| 8-11 月 | 相对平稳 |
| 黑五-圣诞 | 年末大促和礼品/升级需求波峰 |

数据动作：

- 每个候选品必须查 Google Trends 美国近 5 年曲线。
- 标记上架提前期：季节品至少提前 30-60 天准备。
- 不只看当前销量，要看是否已过季节高点。

## 类目标签

每个 SKU 必须打标签：

```csv
sku,category,sub_category,vehicle_type,vehicle_model,evergreen_or_seasonal,order_difficulty,return_risk,margin_level,fitment_complexity,visual_priority,status
```

标签含义：

- `evergreen`：全年稳定，如保养消耗、基础替换、通用保护。
- `seasonal`：雨季、夏季、出行季、节日促销明显。
- `easy_order`：容易出单，适合新店启动。
- `high_margin`：销量可能不大，但利润较好。
- `high_return`：低单量、高客服、高退货，策略需谨慎。

## 车型数据

优先建立美国车型表：

```csv
make,model,vehicle_type,year_range,us_popularity,accessory_scenes,fitment_notes,source
```

重点车型：

- Ford F-Series / F-150
- Chevrolet Silverado
- GMC Sierra
- RAM
- Jeep Wrangler / Grand Cherokee
- Toyota Tacoma / 4Runner / RAV4

验证来源：

- Amazon 搜索结果
- eBay Motors 结果
- Google Trends 美国
- YouTube 安装视频数量
- Reddit/论坛讨论
- AutoZone/Walmart 类目结构

## Amazon/eBay 采样表

```csv
platform,keyword,rank,title,brand,price,rating,review_count,coupon,shipping_method,category,vehicle_fitment,main_image_quality,a_plus,video,low_star_theme,url
```

要求：

- 每个关键词采样前 20 个结果。
- 同时采 Amazon 和 eBay，观察类目是否重合。
- 标记是否有 A+、安装视频、适配图。

## 关键词结构

```csv
level,keyword,type,vehicle,scene,season,risk_note
```

层级：

- 类目词：truck bed cover、rain guard、headlight assembly、control arm、seat organizer
- 车型词：for Ford F150、for Jeep Wrangler、for Toyota Tacoma
- 场景词：road trip、camping、towing、storage、rain、summer
- 问题词：easy install、waterproof、anti slip、fitment、replacement

注意：

- 不把品牌车型词用于误导性标题。
- 车型词用于研究和适配表达，Listing 必须遵守平台规则。

## 利润和促销测算

课程提到优惠券/促销适合客单价较高的产品，低价品促销后容易倒贴。

测算表：

```csv
sku,selling_price,landed_cost,platform_fee,shipping_or_fba,ad_cost,coupon_cost,return_cost,gross_profit,gross_margin,break_even_price,promo_safe
```

规则：

- 客单价过低的 SKU 不适合重促销。
- 促销后仍要覆盖平台费、物流费、优惠券成本、退货损耗。
- 高客单产品更适合用优惠券拉动成交，但必须验证退货风险。

## 上架数量和组合分析

课程强调汽配强适配，单 SKU 覆盖有限，SKU 数量与销量有相关性。

数据能手每周输出：

```csv
week,total_skus,active_skus,orders,revenue,conversion_rate,returns,return_rate,top_20_skus_orders,bottom_20_skus_returns,action
```

判断：

- SKU 少且无订单：优先补 SKU 和补关键词覆盖。
- SKU 多但无转化：检查价格、图文、适配表达。
- SKU 有订单但退货高：优先反馈运营和视觉，必要时下架。

## 加减法规则

加法信号：

- 有曝光、有点击、有订单。
- 低退货、低客服。
- 竞品有 A+ 或视频，说明视觉优化能拉动转化。
- 可扩展同车型、同类目、同套装。

减法信号：

- 长期低曝光低点击。
- 有订单但退货/差评集中。
- 客服问题集中在不适配、安装难、尺寸误解。
- 促销后仍亏损。

## 数据报告模板

```markdown
# 美国汽配数据报告

## 结论
推荐加码/继续观察/下架。

## 季节位置
当前处于淡季、旺季前、旺季中、旺季后。

## 类目标签
长青/季节/易出单/高利润/高售后。

## 车型需求
车型、年份、关键词、搜索趋势。

## 竞品矩阵
价格、评论、图文、A+、退货痛点。

## 利润测算
正常售价、促销价、盈亏平衡。

## SKU 组合建议
补哪些、砍哪些、重点优化哪些。

## 给其他能手
策略决策点；运营动作；视觉素材重点。
```
