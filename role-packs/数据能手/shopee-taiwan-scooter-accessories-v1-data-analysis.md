# 数据能手：Shopee 台湾机车配件数据采集与分析 v1

## 角色定位

负责采集 Shopee 台湾机车配件的公开数据、竞品、价格、月销、评论痛点、供应端价格，并在后期持续分析上架后的销售、广告、转化、退货和库存数据。

## 关键词库

台湾繁体关键词优先：

- 機車配件
- 機車百貨
- 機車手機架 / 機車手機支架
- 機車杯架 / 飲料架
- 機車掛鉤
- 機車置物袋 / 收納袋
- 機車防水袋
- 機車雨衣 / 雨衣收納
- 機車坐墊套 / 防曬坐墊套
- 機車車罩
- 安全帽掛鉤 / 安全帽收納
- Gogoro 配件

补充同义词：

- 摩托車
- 機車用品
- 外送配件
- 防震 / 防水 / 防滑 / 免打孔 / 快拆

## 前期采集表

### Shopee 搜索采样

```csv
keyword,rank,ad_or_organic,product_title,shop_name,price_twd,monthly_sales_visible,total_sold_visible,rating,review_count,variation_count,shipping_from,shipping_fee,product_url,main_image_note,notes
```

采集要求：

- 每个关键词至少前 20 个商品
- 标记广告位和自然位
- 优先记录“月銷/已售/评价数”等公开可见信号
- 不把月销展示等同完整真实销量

### 竞品矩阵

```csv
category,product_url,product_title,shop_name,price_twd,rating,review_count,monthly_sales_visible,variation_strategy,bundle_type,main_selling_points,common_complaints,shipping_note,quality_risk,ip_or_safety_risk
```

每个方向至少 5 个竞品：

- 2 个头部热销
- 2 个中腰部
- 1 个低评分但仍有销量信号

### 评论痛点表

```csv
product_url,rating,review_date,theme,review_summary,fit_issue,quality_issue,shipping_issue,usage_scene,fix_type,opportunity
```

主题：

- 不合车型/尺寸
- 容易松动/断裂
- 防水不足
- 安装困难
- 材质廉价/异味
- 包装压坏
- 出货慢
- 图文和实物不一致

### 供应端粗查

```csv
product_direction,supplier_platform,supplier_url,unit_cost_rmb,moq,material,package_option,customization_option,lead_time,quality_risk,notes
```

供应端查看：

- 1688
- 淘宝
- Alibaba
- AliExpress

## 后期运营数据表

```csv
date,product,sku,views,clicks,ctr,orders,conversion_rate,revenue_twd,ad_spend_twd,roas,refunds,returns,return_reason,inventory,ship_delay_count,notes
```

## 分析规则

- Shopee 台湾先看公开月销、评价数、近期评价密度和价格带
- 高销量低评分竞品优先分析差评，可能藏着改良机会
- 低客单产品要看能否套装化，否则广告空间不足
- 退货原因优先归因到尺寸、适配、质量、页面误导
- 雨季、通勤、外送需求要单独看季节性和场景性

## 输出模板

```markdown
# Shopee 台湾机车配件数据报告

## 结论

## 关键词表现

## 竞品矩阵

## 价格带

## 月销/评价信号

## 评论痛点

## 供应端粗查

## 机会评分

## 给策略能手的建议

## 给运营能手的风险提醒

## 给视觉能手的素材重点
```
