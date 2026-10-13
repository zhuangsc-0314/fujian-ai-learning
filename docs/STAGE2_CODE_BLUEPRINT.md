# 阶段2代码蓝图与接口契约

日期：2026-10-13；关联[课程表](STAGE2_CURRICULUM.md)、[任务](tasks/PLAN-002-stage2-curriculum.md)。

本文区分“现在已有的课程代码/骨架”与“未来提取的正式模块”。函数签名与数据约定是规划，不是已实现服务。所有课程实际入口见[代码导航](../project_steps/STAGE2.md)。

## 1. 现在交付的代码形态

- 2.1/2.2已有代码保持原样；LearningCard仍为summary、keywords、evidence_quote、information_gap四字段。
- 14个新课程目录分别有main.py与README.md，保留TODO USER/ASSISTANT、中文函数契约。未实现业务函数统一抛NotImplementedError。
- project_steps/stage2_scaffold.py只实现课程说明CLI。默认退出0代表“说明已显示”，--exercise退出2代表“练习尚未实施”。没有--live、数据库连接或Web启动功能。
- 2.11-A另有CardReview.vue，2.11-B另有api.ts，均是明确未完成的界面/请求练习；没有package.json或可运行前端构建。
- 当前不会创建正式应用、数据库迁移、测试伪成功或空Key配置。各课实施时再加入恰当依赖与真实验证。

签名中object用于尚未引入的框架类型占位，不能据此把任意对象当合法输入。开课时核实依赖、替换为确切返回类型并增加实际校验。dict[str, object]是规划数据容器，不意味着字段已经受Pydantic保护。

## 2. 正式代码如何逐步收敛（以下目录尚未创建）

2.7开始，在任务中明确接口后逐步提取：

```text
learning_app/
  domain/
    card.py                  # 复用四字段规则；不导入供应商SDK
    material.py              # 来源/日期/不可变版本
    evidence.py              # 逐项事实、引句位置与人工判定
    review.py                # pending/accepted/rejected及版本检查
  ai/
    config.py                # 唯一模型配置读取边界
    prompts.py               # 模板、变量、提示词版本
    provider.py              # ChatDeepSeek与结构化包装
    generation.py            # 最小链调用、结果解析、用量
  services/
    cards.py                 # 生成/保存/读取/审核流程
    candidate_store.py       # 服务端候选快照，ID/归属/过期规则
  repositories/
    cards.py                 # 限定归属的查询与保存
    materials.py             # 材料版本读取，未来接授权策略
  infrastructure/
    db.py                    # 连接、Session生命周期
    models.py                # SQLAlchemy表映射
  api/
    app.py                   # 仅本机演示的HTTP入口
    schemas.py               # 请求/响应与领域对象分开
    dependencies.py          # server提供上下文；非demo无认证拒绝
    routes_cards.py          # 只调用services，不直接创建模型
  cli.py                     # 复用服务，负责终端输入输出
migrations/                  # 2.8-B才创建真实Alembic环境/版本
web/                         # 2.11才创建Vue/Vite项目和锁文件
tests/                       # 随实现补必要离线/开发库/API/页面验证
```

依赖方向：入口 → services → domain、repositories、AI适配器；repositories → db。domain不依赖Web/数据库/供应商；模型不接收Session、连接串或身份控制权。这里不引入多层抽象基类、Agent、LangGraph、微服务。

教学脚本保留历史证据，不因为提取共享模块重写用户过去的练习。新生产路径只保留一套配置/生成服务；课程示例的历史副本明确为历史，不作为并行生产实现。

## 3. 数据对象与权威来源

| 对象 | 关键字段/类型计划 | 谁提供/约束 |
| --- | --- | --- |
| LearningCard | summary:str、keywords:list[str]、evidence_quote:str、information_gap:str | 模型候选，继续按现有四字段规则校验；格式不证明事实 |
| MaterialVersion | id、owner_user_id、title、text、content_sha256、source_url:str或None、published_on:date或None、version_no | 用户提供来源/日期，业务创建ID与版本；未知保持None；同版本正文不可变 |
| EvidenceItem | claim_text、quote、start、end、material_version_id、manual_decision | 人工核对的事实与证据关联；位置须可由原文切片还原，不能只让模型报数字 |
| CandidateSnapshot | candidate_id、owner、material_version_id、content_hash、card、evidence_items、prompt_version、created_at、expires_at | 服务端创建并保存快照；客户端仅引用ID，不能把传回的任意正文当可信候选 |
| GenerationResult | status、candidate_id或None、error_code或None、stage、attempts、usage或None | 服务端实际运行产生；成功与失败结果不能同时混合；未知用量不能填0 |
| SavedCard | id、owner、material_version_id、candidate_id、content_hash、validated_payload、review_status、schema/prompt版本 | 从服务端快照保存；candidate_id/owner组合唯一；内容与审核版本关联 |

MaterialVersion的owner在阶段2为显式本机demo上下文提供，不能来自模型或HTTP正文。真实用户身份按阶段3接入；数据库“有owner列”或传入A/B测试上下文不等于认证成功。

同一引句出现多次，locate_quote返回所有候选位置，由人工选定支持某项事实的实例。Python字符位置与浏览器UTF-16下标可能不同，API应返回服务端切好的原文前/中/后片段或明确的段落定位，前端不直接按Python整数切JavaScript字符串。任何位置都绑定同一个原文版本。

本阶段无需改写2.1 schema来硬塞元数据；逐项证据先放在外层业务记录。若以后让模型产生多事实/多引用结构，另立schema_v2变更任务、兼容策略和新生成验证，不静默改变旧四字段。

## 4. 关键函数契约

| 课程 | 当前骨架接口 | 实施时的责任 |
| --- | --- | --- |
| 2.3-A | decide_review_status(...) → str | 汇总人工结论；未知不能变通过，冲突不能被格式校验覆盖 |
| 2.3-B | locate_quote(material, quote) → list[tuple[int, int]] | 定位所有出现处，拒绝空引句，不判定语义 |
| 2.4 | prepare_prompt_values(...) → dict[str, str]；build_prompt_template() | 贯通目标/原文/schema变量，system约束固定，预览无请求 |
| 2.5 | build_card_chain(prompt, structured_model) | 组合Runnable接口；构建不invoke；失败保留原层级 |
| 2.6 | describe_publication_date(...)；build_material_context(...) | 未知日期/来源、版本与外层归属 |
| 2.7 | generate_candidate(...)；classify_failure_stage(...) | 一个共享生成服务，服务端候选快照，脱敏结果/错误 |
| 2.8-A | probe_database(...)；describe_database_failure(...) | 显式开发库连接及安全诊断 |
| 2.8-B | build_model_metadata()；require_owner(...) | 表映射/迁移与业务非空检查；后者不是认证 |
| 2.9-A | save_candidate(session, snapshot, *, owner_user_id, material_version_id) | 事务保存可信快照，提交成功才返回ID |
| 2.9-B | get_owned_card(session, *, card_id, owner_user_id) | 在查询条件中限制归属；不可读/不存在均不可泄露数据 |
| 2.10 | create_app()；map_error_status(...) | HTTP适配、请求模型、上下文、状态码 |
| 2.11-A/B | CardReview.vue；fetchCard(cardId) | 数据绑定与请求状态；不包含模型Key/SDK |
| 2.12 | build_acceptance_report(results) | 分列passed/failed/not_run和真实/离线来源 |

这些函数大部分是独立练习切口，完整教学框架在开课时由助手补齐。不能把main.py中少量函数误认作该模块全部实现。

## 5. 状态与保存的边界

```text
格式/字段/引用检查失败 → 明确失败，没有可保存的卡片候选
检查通过 → 服务端候选快照 pending_manual_review
用户明确保存 → 事务保存草稿，仍 pending_manual_review
用户逐项核对特定内容版本 → accepted 或 rejected
内容变化 → 新候选/新版本，原审核结论不能直接沿用
```

“允许存待审核草稿”不等于“允许把不合格生成结果保存成合格卡”。pending草稿、审核驳回记录与正式已接受内容在页面/查询中显式区分。人工accepted也仅记录人的判断，不能宣称普遍正确。

保存只传候选ID和预期内容版本，服务端重新取得快照，检查归属、材料版本和有效期；不能直接信任客户端提交的owner、review_status或“validated=true”。重启后未保存的内存候选可明确失效，不能悄悄重新生成/收费。待保存场景确需耐久草稿时再把候选存储替换为数据库实现。

数据库事务只覆盖必要读写，不在长期事务中等待模型。生成成功与保存成功分别反馈；保存失败不重新invoke。重复保存依靠数据库唯一约束处理，不只靠按钮禁用；再次返回既有结果或明确冲突，接口语义在2.9固定。

审核请求绑定卡片ID、内容hash或版本、人工决定及依据；修改条件必须同时限定owner和预期版本，旧版本请求返回冲突，不能覆盖新内容的审核状态。

## 6. 本机API契约（未来实现）

采用同步教学流程，暂不照搬完整平台设计中的异步job_id/202协议。原生产任务队列方案保留到后续阶段，当前不得返回虚构job_id。

| 方法/路径 | 输入 → 输出 | 重要边界 |
| --- | --- | --- |
| POST /api/v1/materials | title/text/source/date → material_version_id | 业务提供owner，校验来源/日期，不运行模型 |
| POST /api/v1/card-candidates | material_version_id/learning_goal → candidate_id/card/review_status或明确错误 | 实际生成入口；显式live开关才允许模型请求 |
| POST /api/v1/cards | candidate_id/expected_content_hash → saved_card_id | 取服务端快照，校验后事务保存，模型请求0 |
| GET /api/v1/cards | 有界分页参数 → 当前上下文的卡片列表 | 数据库限定owner，不信任URL/body中user_id |
| GET /api/v1/cards/{id} | ID → 卡片/原文定位/审核状态 | 同时检查卡片和源材料可读范围 |
| PATCH /api/v1/cards/{id}/review | expected_version/人工决定/证据说明 → 新审核状态 | 不接受跨版本确认或直接替换候选正文 |

具体错误码实施时固定：请求格式问题422、不可读/不存在404、版本冲突409、上游失败502/504、存储不可用503、未启用live明确拒绝。只有业务成功才返回成功状态；日志含失败步骤但不打印Key、完整连接串或原始私有正文。

本机demo模式要显式启用，仅绑定127.0.0.1，并在界面展示“本机教学演示，未实现真实认证”。该模式用于可信本机环境；环回地址本身不是认证或浏览器跨站防护。开API课时仍需校验允许的Host/Origin、拒绝任意CORS与无关来源写入，保持API与页面受控访问。非demo配置缺少真实认证应拒绝启动，不能回退成默认用户。开放给朋友前先接阶段3认证与双用户集成测试。

## 7. 前端的最小范围

只有材料输入、候选/原文对照、卡片列表/详情三个视图；核心动作是生成、核对、保存、重开。没有注册、分享、全站后台或复杂样式工程。

2.11-A先使用明确标注的人工界面样例练习绑定，2.11-B接本机API。界面需区分空、加载、候选待核对、已保存、失败；字段缺失不能继续显示旧卡片冒充新结果。错误显示步骤与恢复动作，不显示内部Key或配置。

普通读取/保存不发模型请求。真实生成动作有清晰live标识和一次操作边界，默认AI调用禁用。客户端禁止重复点击只是交互帮助，服务端仍处理重复保存/版本冲突。所有材料按文本渲染，不用v-html。

## 8. 验证计划与当前限制

| 层 | 实施后的必要验证 | 当前状态 |
| --- | --- | --- |
| 既有2.1/2.2 | 已有schema/包装器/展示实测 | 沿用既有证据，本规划不重跑付费 |
| 新骨架 | AST解析、说明入口0、练习2、未实现函数抛错、禁止.env/网络 | 本任务执行，结果写PLAN-002 |
| 纯函数/提示词/链 | 正常/非法/边界与调用计数 | 未来对应课程实现后验证 |
| PostgreSQL | 专用库迁移、读写/回滚、唯一约束、归属过滤 | 未安装/运行，不用SQLite或内存替身冒充PG实测 |
| API/页面 | 请求响应、状态码、保存后重开、文本渲染 | 未安装/构建/联调，Vue/TS仅骨架 |
| 真实服务/权限 | 新流程真实生成、双账号认证/撤权/源权限 | 未运行；分别记录费用/次数和隔离证据 |

API知识参考[FastAPI依赖文档](https://fastapi.tiangolo.com/tutorial/dependencies/)，事务知识参考[SQLAlchemy Session文档](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)。这些资料帮助定义边界，不能证明本仓库新功能已实现或兼容。

下一小步仍在2.2/2.3-A交界，每课按独立任务逐步填骨架。
