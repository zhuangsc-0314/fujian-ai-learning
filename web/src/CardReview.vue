<script setup lang="ts">
import type { Card, Material } from './api'

// props是父组件传进来的数据；子组件只展示，不创建模型或保存记录。
defineProps<{ card: Card; material: Material; sourceMode: string; status: string }>()
</script>

<template>
  <div class="compare">
    <article class="panel">
      <span class="eyebrow">学习卡 · {{ status }}</span>
      <h2>提取重点，也保留未知</h2>
      <p class="summary">{{ card.summary }}</p>
      <div class="tags"><span v-for="(word, index) in card.keywords" :key="index">{{ word }}</span></div>
      <h3>原文引句</h3><blockquote>{{ card.evidence_quote }}</blockquote>
      <div class="gap"><h3>信息缺口</h3><p>{{ card.information_gap }}</p></div>
      <p class="muted">{{ sourceMode === 'historical_replay' ? '历史真实候选回放 · 本次模型请求 0' : '真实模型候选 · 仍需人工核对' }}</p>
    </article>
    <article class="panel source">
      <span class="eyebrow">原始材料 · 不可变版本</span>
      <h2>{{ material.title }}</h2>
      <p class="muted">发布日期：{{ material.published_on || '未知' }}</p>
      <p class="source-text">{{ material.text }}</p>
      <p class="muted">来源：{{ material.source_url || '未提供链接，请自行核实' }}</p>
      <p class="muted">引用存在只能证明文字出现过，不能证明摘要的每个判断正确。</p>
    </article>
  </div>
</template>
