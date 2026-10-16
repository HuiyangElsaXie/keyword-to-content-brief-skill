# SEO 关键词到内容计划

Convert a small keyword brief into page decisions and an actionable writing brief without inventing search volume or ranking evidence.

## 给作品集读者

先看 examples/output.md 中的交付结果，再看 examples/comparison.md 中的判断依据。这个项目展示如何拆解问题、组织证据并交付可审核建议；不声称已经带来排名、收入或转化提升。

这是为 Huiyang Xie 准备的 AI 辅助原创初稿，仍待本人审核。案例全部虚构，不含客户、雇主或 OE 私有内容。

## 使用方式

输入：examples/input.json。方法：skills/keyword-to-content-brief/SKILL.md。人工评价标准：evals/rubric.md。

Python 3.10 及以上，使用标准库，无需安装依赖、账号或付费 API：

    python -m unittest discover -s tests -v

自动测试仅验证样例和确定性规则，不代表完整营销效果验证。上线前逐项完成 REVIEW_BEFORE_PUBLIC.md。当前只准备私有仓库内容，公开需要单独审核。

## 来源与许可

参见 ATTRIBUTION.md。本次没有复制上游代码或 prompt；外部链接仅作为研究参考。原创文件的公开许可尚未选择。LICENSE-PROPOSAL.md 仅提出 MIT 供本人审核，不构成授权；「非商用作品集」用途本身也不等于选定许可证。
