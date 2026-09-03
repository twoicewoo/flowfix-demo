# FlowFix：中小微企业重复办公流程自动化定制

FlowFix 把“反复复制粘贴、核对表格、整理异常、生成日报”的人工流程，改造成可在客户电脑运行、保留人工确认点、结果可复核的轻量工具。

- 公开演示页：https://twoicewoo.github.io/flowfix-demo/
- 可复核运行仓库：https://github.com/twoicewoo/flowfix-demo
- 月度商品对比与销售汇总模板：https://github.com/twoicewoo/flowfix-demo/raw/main/downloads/FlowFix-monthly-product-summary-demo.xlsx

## 当前经营选择

- **客户**：每周重复处理 Excel/CSV/PDF/网页数据的电商运营、行政、财务和小团队负责人。
- **问题**：人工录入和核对耗时、容易漏项，异常没有统一清单，管理者看不到汇总结果。
- **供给**：先用脱敏样表做固定范围原型；确认规则后交付本地脚本、异常清单、汇总报告、操作说明和短期缺陷修复。
- **成交入口**：威客平台的具体任务投标与固定价服务。公开展示只使用本目录中的合成演示，不冒充客户案例。
- **停止条件**：连续 20 次合格触达没有有效咨询，或 5 次有效咨询没有一笔付费诊断，则重做细分场景与报价，不继续堆功能。

## 可运行演示

演示输入是虚构订单数据，不是营收或客户数据。

```bash
python3 business/flowfix/demo/run.py \
  --input business/flowfix/demo/input/orders.csv \
  --output /tmp/flowfix-output
```

预期终端结果：

```text
FLOWFIX_DEMO_OK input_rows=8 valid_rows=5 review_rows=3 gross_cny=2959.00 refunds_cny=299.00 net_cny=2660.00
```

输出包括 `valid_orders.csv`、`review_queue.csv`、`summary.json` 和 `management_report.md`。

## 商业状态

截至 2026-09-04：产品样例已可运行；已发现 1 条近期、明确表示可付费且与样例匹配的潜在线索，私信草稿已就绪但尚未发送；真实付款、交付、收入和利润仍为 0，状态为 `RESEARCH / NO_REVENUE`。
