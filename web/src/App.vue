<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import CardReview from './CardReview.vue'
import { fetchCard, request, type Candidate, type CardListItem, type Info, type Material, type Saved } from './api'

const info = ref<Info | null>(null)
const title = ref('2023年历史考试范围摘录')
const text = ref('')
const sourceUrl = ref('')
const publishedOn = ref('')
const goal = ref('整理原文范围，明确未知信息。')
const material = ref<Material | null>(null)
const candidate = ref<Candidate | null>(null)
const saved = ref<Saved | null>(null)
const cards = ref<CardListItem[]>([])
const busy = ref(false)
const error = ref('')
const notice = ref('')
const tab = ref('create')
const offset = ref(0)
const note = ref('')
const checked = ref(false)
const noTimeConflict = ref(false)
const evidence = ref([{ claim_text: '', quote: '', occurrence: 0, supported: true }])
const payload = computed(() => saved.value?.payload || candidate.value?.payload)
const statusLabels: Record<string, string> = { pending_manual_review: '待人工核对', accepted: '人工通过', rejected: '人工驳回' }
const status = computed(() => statusLabels[saved.value?.review_status || 'pending_manual_review'])

// 所有动作共用busy锁；表单在请求期间禁用，避免旧请求覆盖新材料。
async function action(work: () => Promise<void>) {
  if (busy.value) return
  busy.value = true; error.value = ''; notice.value = ''
  try { await work() } catch (e) { error.value = e instanceof Error ? e.message : '操作失败，请重新读取。' }
  finally { busy.value = false }
}
function resetReview() {
  note.value = ''; checked.value = false; noTimeConflict.value = false
  evidence.value = [{ claim_text: '', quote: '', occurrence: 0, supported: true }]
}
function resetCandidate() {
  candidate.value = null; saved.value = null; material.value = null; resetReview()
  history.replaceState(null, '', location.pathname)
}
async function generate(mode: 'live' | 'historical_replay') {
  await action(async () => {
    resetCandidate()
    material.value = await request<Material>('/materials', 'POST', {
      title: title.value, text: text.value, source_url: sourceUrl.value || null,
      published_on: publishedOn.value || null,
    })
    candidate.value = await request<Candidate>('/card-candidates', 'POST', {
      material_version_id: material.value.id, learning_goal: goal.value, mode,
    })
    notice.value = '候选已准备。请先对照原文；保存后可记录人工审核。'
  })
}
async function save() {
  await action(async () => {
    if (!candidate.value) return
    saved.value = await request<Saved>('/cards', 'POST', {
      candidate_id: candidate.value.candidate_id, expected_content_hash: candidate.value.content_hash,
    })
    history.replaceState(null, '', `?card=${saved.value.id}`)
    notice.value = '已保存待审核草稿。现在刷新页面仍能读取，未新增模型请求。'
  })
}
async function openCard(id: string) {
  resetCandidate()
  saved.value = await fetchCard(id); material.value = saved.value.material
  title.value = material.value.title; text.value = material.value.text
  sourceUrl.value = material.value.source_url || ''; publishedOn.value = material.value.published_on || ''
  goal.value = saved.value.payload.learning_goal
  tab.value = 'create'; history.replaceState(null, '', `?card=${encodeURIComponent(id)}`)
}
async function loadList() { cards.value = await request<CardListItem[]>(`/cards?limit=10&offset=${offset.value}`) }
function quotePositions(quote: string): number[] {
  // Array.from按Unicode码点拆分，与Python下标一致；不直接使用JS UTF-16索引。
  const source = Array.from(material.value?.text || '')
  const needle = Array.from(quote)
  if (!quote.trim()) return []
  const results = []
  for (let i = 0; i <= source.length - needle.length; i++) {
    if (source.slice(i, i + needle.length).join('') === quote) results.push(i)
  }
  return results
}
async function review(decision: string) {
  await action(async () => {
    if (!saved.value) return
    const selected = evidence.value.filter(item => item.quote.trim() || item.claim_text.trim())
    const items = selected.map(item => {
      const start = quotePositions(item.quote)[item.occurrence]
      if (start === undefined) throw new Error('核对步骤：引句没有对应原文位置，请逐字复制。')
      return { claim_text: item.claim_text, quote: item.quote, start, supported: item.supported }
    })
    saved.value = await request<Saved>(`/cards/${saved.value.id}/review`, 'PATCH', {
      expected_version: saved.value.review_version, expected_content_hash: saved.value.content_hash,
      decision, note: note.value, all_claims_checked: checked.value,
      has_time_conflict: noTimeConflict.value ? false : null, evidence: items,
    })
    notice.value = '人工审核已记录。它代表本次核对结论，不保证所有事实永远正确。'
  })
}
onMounted(() => action(async () => {
  info.value = await request<Info>('/info'); text.value = info.value.historical_material
  const id = new URLSearchParams(location.search).get('card')
  if (id) await openCard(id)
}))
</script>

<template>
  <header><div class="brand">闽 · 学习札记</div><span>阶段 02 / 结构化学习卡</span></header>
  <main>
    <div class="intro"><span class="eyebrow">从一段材料，到一张有依据的卡片</span><h1>学得清楚，记得有据。</h1><p>{{ info?.notice || '正在连接本机服务…' }}</p></div>
    <nav><button :disabled="busy" :class="{ active: tab === 'create' }" @click="tab = 'create'">材料与学习卡</button><button :disabled="busy" :class="{ active: tab === 'list' }" @click="action(async () => { tab = 'list'; await loadList() })">已保存卡片</button></nav>
    <div v-if="error" class="message error" role="alert">{{ error }} <button :disabled="busy" @click="action(async () => { info = await request<Info>('/info'); if (tab === 'list') await loadList() })">重试连接</button></div>
    <div v-if="notice" class="message" role="status">{{ notice }}</div>
    <p v-if="busy" role="status">正在处理，请稍候…</p>
    <template v-if="tab === 'create'">
      <form class="panel entry" @submit.prevent="generate('historical_replay')">
        <fieldset :disabled="busy"><legend>01 / 准备材料</legend>
          <label>材料标题<input v-model="title" maxlength="120" required @input="resetCandidate"></label>
          <label>原文<textarea v-model="text" rows="4" maxlength="2000" required @input="resetCandidate"></textarea></label>
          <div class="fields"><label>来源链接（可空）<input v-model="sourceUrl" type="url" @input="resetCandidate"></label><label>发布日期（可空）<input v-model="publishedOn" type="date" @input="resetCandidate"></label></div>
          <label>学习目标<input v-model="goal" maxlength="300" required @input="resetCandidate"></label>
          <div class="actions"><button type="submit">载入历史候选 · 免费回放</button><button type="button" class="secondary" :disabled="!info?.live_enabled" @click="generate('live')">真实生成 · 可能计费</button></div>
          <p class="muted">历史回放仅支持原始示例材料。当前真实生成为{{ info?.live_enabled ? '已启用' : '禁用' }}。修改材料后需真实生成。</p>
        </fieldset>
      </form>
      <template v-if="payload && material">
        <CardReview :card="payload.card" :material="material" :source-mode="payload.source_mode" :status="status" />
        <div class="actions"><button :disabled="busy || !!saved" @click="save">{{ saved ? '已保存' : '保存待核对草稿' }}</button><button v-if="saved" class="secondary" :disabled="busy" @click="action(() => openCard(saved!.id))">重新读取记录</button></div>
        <form v-if="saved" class="panel review" @submit.prevent="review('accepted')">
          <fieldset :disabled="busy"><legend>02 / 人工核对 · 版本 {{ saved.review_version }}</legend>
            <p v-if="saved.review.note" class="muted">上次说明：{{ saved.review.note }}</p>
            <details v-if="saved.review.evidence?.length">
              <summary>查看已记录的逐项依据</summary>
              <div v-for="(item, n) in saved.review.evidence" :key="n" class="evidence">
                <p>{{ item.claim_text }} · {{ item.supported ? '有支持依据' : '不支持' }}</p>
                <blockquote>{{ item.quote }}</blockquote>
                <p class="muted">原文位置 {{ item.start }}—{{ item.end }}；绑定当前材料版本。</p>
              </div>
            </details>
            <p>把摘要中的判断逐项对应到原文，再确认适用时间。未知信息应继续保留。</p>
            <div v-for="(item, index) in evidence" :key="index" class="evidence">
              <label>判断 {{ index + 1 }}<input v-model="item.claim_text" placeholder="这张卡片声称了什么？"></label>
              <label>支持或反驳它的原文<textarea v-model="item.quote" rows="2" placeholder="逐字复制原文引句"></textarea></label>
              <label>原文出现位置<select v-model.number="item.occurrence"><option v-for="(start, n) in quotePositions(item.quote)" :key="n" :value="n">第 {{ n + 1 }} 处（字符 {{ start }}）</option></select></label>
              <label class="check"><input type="checkbox" v-model="item.supported">这条原文支持上述判断</label>
              <button v-if="evidence.length > 1" type="button" class="text-button" @click="evidence.splice(index, 1)">移除此项</button>
            </div>
            <button type="button" class="secondary" :disabled="evidence.length >= 20" @click="evidence.push({claim_text: '', quote: '', occurrence: 0, supported: true})">添加一项依据</button>
            <label class="check"><input type="checkbox" v-model="checked">我已逐项核对摘要、关键词及信息缺口</label>
            <label class="check"><input type="checkbox" v-model="noTimeConflict">已核对适用时间，没有将历史材料当作未来规则</label>
            <label>审核说明<textarea v-model="note" rows="2" maxlength="1000" placeholder="说明判断依据、遗漏或冲突" required></textarea></label>
            <div class="actions"><button type="submit">记录人工通过</button><button type="button" class="secondary" @click="review('rejected')">记录驳回</button><button type="button" class="secondary" @click="review('pending_manual_review')">保持待核对</button></div>
          </fieldset>
        </form>
      </template>
      <p v-else class="empty">准备好材料后，学习卡与原文将在这里并排显示。</p>
    </template>
    <section v-else class="panel">
      <h2>保存的学习卡</h2><p v-if="!cards.length" class="empty">这一页还没有卡片。先保存一张待核对草稿。</p>
      <button v-for="card in cards" :key="card.id" class="card-row" :disabled="busy" @click="action(() => openCard(card.id))"><span>{{ card.summary }}</span><small>{{ statusLabels[card.review_status] }}</small></button>
      <div class="actions"><button class="secondary" :disabled="busy || offset === 0" @click="action(async () => { offset = Math.max(0, offset - 10); await loadList() })">上一页</button><button class="secondary" :disabled="busy || cards.length < 10" @click="action(async () => { offset += 10; await loadList() })">下一页</button></div>
    </section>
  </main><footer>本机教学参考实现 · 无真实账号认证 · 格式通过不等于事实正确</footer>
</template>
