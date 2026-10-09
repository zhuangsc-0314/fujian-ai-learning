# 清理候选清单与外部Embedding选型

日期：2026-10-09。服务器1.14.255.10。仅只读巡检，没有删除、停止服务、注册服务或调用付费Embedding API。

后续状态：用户授权后已完成部分安全清理，净释放约5.34GiB，服务状态复核无变化。见 [实际清理记录](CLEANUP_EXECUTION_20261009.md)。下表仍保留清理前观测值作为依据。
所有占用是观测值；释放空间是待执行后的结果，不能把共享Docker层、缓存和镜像的显示大小直接相加。

## 清理候选

| 优先级 | 对象与位置 | 观测占用 | 建议范围与影响 |
| --- | --- | --- | --- |
| A | Docker构建缓存 | 6.276GB、245条记录，多数最近使用在2–3周前 | 优先候选；仅清理未使用的构建缓存，可按最后使用时间/保留容量过滤；下次构建会重新下载/构建，不删除运行容器和业务卷 |
| A | npm下载缓存 /root/.npm/_cacache | 约1.3GB | 使用npm支持的缓存管理方式；确认无构建进行，清理后重新下载依赖；不是删除已安装全局包 |
| A | pip/dnf缓存 /root/.cache/pip、/var/cache/dnf | 约85MB、81MB | 确认无包安装进行后用包管理器清缓存；总量不大 |
| B | systemd journal /var/log/journal | du约2GB；归档53份，活动2份 | 建议保留必要近期/异常记录，目标占用500MB–1GB；用journal保留/清理机制处理归档，不手工删活动文件；历史排障证据不可恢复 |
| B | 23个悬空Docker镜像 | three-card镜像19个，browser3个，flow1个 | 按ID确认未用于回滚/离线重建后删除候选；多数层共享，镜像表大小不是可释放空间 |
| B | three-card-online回滚镜像8个 | 每个显示248MB，独占约77–78MB | 保留最近经过验证的1–2个回滚版本，其余逐ID列入候选；保留按发布记录，不只按tag字典排序；六个旧版独占层约0.47GB，真实释放还受缓存引用影响 |
| B | pnpm内容存储 /root/.local/share/pnpm/store | 约1.9GB | 仅由pnpm识别未引用包再prune；不能将1.9GB都当作可删内容；全局安装目录505MB继续保留 |
| C | npm npx缓存 /root/.npm/_npx | 约178MB | 可能包含当前工具执行路径；核对进程依赖后再清，不能直接认定闲置 |
| C | Playwright /root/.cache/ms-playwright | 约625MB | chromium365MB、headless255MB、ffmpeg5MB；先检查正在使用的浏览器版本/工具依赖，仅移除确认废弃版本；当前存在浏览器业务 |
| C | 普通日志 /var/log/secure、cron、messages | 约240MB、121MB、91MB | 配置logrotate/保留策略；安全记录先按排障要求保留，不直接截断当前日志 |
| C | Docker容器日志 | 约60MB | 不值得优先清；设置后续轮转，避免增长；不要手工删除正在写入的json日志 |
| 不建议 | 未被容器引用的hiclaw-data卷 | 约29MB | 可能有历史业务数据，LINKS=0不代表可丢；收益很小，先保留并确认用途 |
| 保留 | MySQL、PostgreSQL、当前容器卷、/opt项目、.ssh、.env、pnpm全局工具 | 业务/配置/工具 | 不作为缓存清理；/opt全部约541MB，删项目收益小且依赖未审计 |

不要使用全量system prune加volumes来代替范围明确的清理。Docker的-a镜像清理会覆盖所有未被容器引用的镜像，包括带回滚tag的镜像。[构建缓存机制](https://docs.docker.com/reference/cli/docker/builder/prune/)、[镜像清理范围](https://docs.docker.com/reference/cli/docker/image/prune/)

建议先处理构建/npm缓存和日志保留，再决定悬空镜像、回滚版本和pnpm未引用包。每项操作前重新检查状态，操作后检查df、容器健康及其他项目。当前磁盘剩约12GB；能否达到15–20GB目标取决于实际释放，未执行时不承诺总数。

## 内存候选

当前douyin-browser容器约350MiB（巡检期间有变化），是可见的较大内存使用者；停止会影响浏览器业务，只在明确不需要该业务时纳入停用计划。douyin-spark-flow该次样本约2MiB，收益很小，不按前一轮230MiB做保证。

磁盘缓存清理不能保证释放应用内存，不执行drop_caches或清空Swap来制造“空闲内存”。系统available内存已将可回收文件缓存计入。

## 外部Embedding建议

Embedding把文本变成用于比较语义相近程度的数值向量。它不生成政策答案；DeepSeek负责理解/生成，Embedding服务负责材料与问题向量化，pgvector负责保存与检索。这几个供应商不必相同。

首选：阿里云百炼北京地域按量API，qwen3.7-text-embedding，初始1024维。当前官方文档列出中文支持、OpenAI兼容调用以及每千输入Token0.0005元，即每百万输入Token约0.5元。text-embedding-v4同价，可作为已公开接口的对照候选。模型Key/endpoint按对应账号、业务空间与地域控制台填写，不套用旧教程固定URL。

低费用候选：同平台qwen3.7-text-embedding-flash，每千Token0.000125元，即每百万约0.125元。是否适合本项目以同一政策测试集比较，不能仅按模型名或价格推断准确率。

学习备用：硅基流动BAAI/bge-m3。官方价目搜索索引列为免费，OpenAI风格embeddings接口，文本上限8192Token；完整价格页面本轮多次打开超时，免费策略、账号限额和当前可用性以控制台确认，不承诺长期免费或生产SLA。

| 方案 | 推荐用法 |
| --- | --- |
| 百炼qwen3.7-text-embedding | 项目主候选，先真实小样本检索验证 |
| 百炼qwen3.7-text-embedding-flash | 同测试集费用/质量对照 |
| 硅基流动BAAI/bge-m3 | 低预算入门和对照候选，不以免费等同稳定可用 |

价格核对日期2026-10-09，仅北京地域常规同步Embedding输入费用，不含重试、重复索引、向量数据库、文件、Rerank与聊天模型。1000万输入Token示例：主候选约5元、Flash约1.25元；这是算式，不是实际项目月费。

[百炼Embedding规格与价格](https://help.aliyun.com/zh/model-studio/embedding?disableWebsiteRedirect=true)
[硅基流动官方价格页](https://siliconflow.cn/pricing)
[硅基流动Embedding API](https://api-docs.siliconflow.cn/docs/api/embeddings-post)

## 数据与接入边界

- 外部向量化会发送原文片段和问题；先使用公开官方材料，个人信息不进入Embedding输入。
- 硅基流动政策对API业务数据声明不长期存储及不用作模型训练，但仍存在安全审核和调用元数据；不能把这一声明当作独立审计结论。[隐私政策](https://docs.siliconflow.cn/docs/legals/privacy-policy)
- 百炼条款按所开通站点、地域与产品核实；国际站企业ZDR或Coding/Token Plan条款不能直接套到北京地域按量API。不用于训练与零留存是不同承诺。
- 文档与问题使用相同模型、维度、归一化/查询策略；不同模型即使维度相同也不能混用向量。换模型新建index_revision并重新索引，保留旧引用。
- 材料hash、版本、Embedding模型和预处理作为缓存键，只重算变化片段；调用只返回向量，不需要购买托管知识库。
- 设置请求长度、批次数、超时/429退避、预算与脱敏日志；provider Key在服务端环境变量，不进入前端。
- 正式锁定前，用20个问题的固定集比较召回、引用命中、p95、失败率与费用，并验证服务器到endpoint网络。当前只核实文档，未实测Embedding API或声称某模型最准确。
- LangChain在阶段4封装Embedding适配器；这一层选择供应商不改变权限过滤、材料版本和普通业务边界。

当前建议：先审阅清理清单；学习阶段继续原路线。Embedding在阶段4接入，不需要现在提前注册或花钱购买知识库。
