# 阶段2实际模块与接口契约

2026-10-13：[STAGE2-001](tasks/STAGE2-001-complete-reference.md)已补齐完整参考实现；此页描述当前代码，不再把未来蓝图当实现。原PLAN-002保留历史记录。[运行手册](STAGE2_RUNBOOK.md)包含安装和实际命令。

## 模块与数据流

```text
CLI / FastAPI / Vue
      ↓
CardService：材料、生成、保存、读取、审核
      ↓              ↓                 ↓
domain业务规则   storage/PostgreSQL    ai模板/供应商/结构化输出
```

正式代码收敛为learning_app/domain.py、ai.py、history.py、storage.py、service.py、api.py、cli.py；避免提前建大量空目录。2.1/2.2用户实现原样复用，14个后续main导入共享函数。前端唯一实现在web/src，课程Vue/TS只是再导出入口。

domain：LearningCard仍是四字段；MaterialInput提供title/text/source_url/published_on，owner由服务端提供。locate_quote返回全部Python码点半开区间；人工EvidenceInput包括claim_text/quote/start/supported，服务端切片再次验证。ReviewInput明确decision、note、expected_version/content_hash、完整核对确认及时间冲突；格式校验不会验证事实。

ai：prepare_prompt_values→ChatPromptTemplate→prompt | structured_model→一次invoke→raw/parsed/parsing_error检查。只有live=True读取1.2配置并创建ChatDeepSeek；max_retries=0，超时状态未知；只捕获具体SDK异常，对外脱敏。schema/引用/关键词通过才有候选。

history：只回放RUN_RESULTS.md中可追溯真实候选；要求原文一致，source_mode=historical_replay、attempts=0、usage=None；新目标不重新生成旧答案。新live结果source_mode=live、实际usage和attempts=1。新模板stage2_card_v2本轮未真实调用。

## 候选、材料与存储

服务端CandidateStore保存深拷贝快照、随机ID、owner/材料版本、内容hash和30分钟过期时间；最多100条，过期清理。客户端只能通过candidate_id/expected_content_hash保存，不能提交任意正文、owner或审核状态。未保存候选重启失效，不自动收费恢复；已保存记录重启可读和重复提交。

materials：id、owner_user_id、JSONB payload（标题/原文/来源/日期/版本号/原文sha256）。本阶段只创建不可变版本，无正文更新接口。

cards：id、owner、材料版本、candidate_id、content_hash、JSONB payload、review_status/review_version/review、created_at。owner+candidate_id唯一；材料ID+owner复合外键；审核状态和版本CheckConstraint。Alembic0001负责真实建表，不启动时自动create_all。

生成前读取并关闭Session；模型不在事务中等待。保存事务内检查快照、材料hash/owner，INSERT ON CONFLICT处理并发重复，提交成功后返回。读取同时限定卡片/材料owner；审核UPDATE同时限定owner、内容hash和版本，rowcount不是1则409。review内保存逐项证据和绑定材料ID，旧审核不能覆盖新版本。

材料/卡片owner是本机demo占位；数据库归属条件测试不等于真实身份授权。暂无注册/登录/撤权/多人平台。

## 实际API

| 方法/路径 | 输入 → 输出 | 边界 |
| --- | --- | --- |
| GET /api/v1/info | 本机模式/历史材料/真实生成开关 | 不含凭证 |
| POST /api/v1/materials | title/text/source_url/published_on → 材料版本 | 不允许HTTP owner字段 |
| POST /api/v1/card-candidates | material_version_id/learning_goal/mode → 服务端候选 | mode为live或historical_replay；默认live禁用 |
| POST /api/v1/cards | candidate_id/expected_content_hash → 已保存卡 | 不信任客户端正文；幂等；请求模型0 |
| GET /api/v1/cards | limit1—100/offset → 有界列表 | 服务端demo owner限定 |
| GET /api/v1/cards/{id} | ID → 记录、原文、审核证据 | 不可读/不存在统一404 |
| PATCH /api/v1/cards/{id}/review | ReviewInput → 新状态/版本 | 引句切片校验，完整核对与时间确认；旧版本409 |

请求非法422、不可读404、内容/审核冲突409、live禁用403、上游失败502/超时504、配置/数据库不可用503。SQLAlchemy与请求校验异常脱敏，不返回原始输入/连接串。同步HTTP，无虚构job_id/202。

create_app必须显式demo；CLI只bind127.0.0.1。校验允许的Host/Origin、跨站Sec-Fetch-Site和写请求X-Stage2-Local；不启用CORS。页面由FastAPI托管dist，材料按文本绑定显示，CSP限制脚本/连接。API文档交互页面可能受CSP限制，可读取/openapi.json和本契约。

## Vue页面与验收

App.vue管理输入、加载/错误、候选、保存、审核、列表/分页及?card=ID重开。请求期间busy锁定输入；编辑材料清除旧候选；CardReview.vue只展示props。重新读取恢复实际材料/目标，已记录逐项依据可展开查看。api.ts统一fetch/失败提示，不含Key或供应商SDK。

32项离线规则/链路+10个固定材料边界+6项真实PG/HTTP共48项通过；Vite和vue-tsc构建通过；浏览器完成回放、保存、人工核对及刷新重开。新真实生成、F1质量、真实认证和Linux仍未验证。助手完整参考代码与用户独立掌握分开记录，具体证据见任务。
