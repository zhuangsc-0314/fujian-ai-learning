export interface Card {
  summary: string; keywords: string[]; evidence_quote: string; information_gap: string
}
export interface Material {
  id: string; title: string; text: string; source_url: string | null; published_on: string | null
}
export interface Payload { card: Card; source_mode: string; attempts: number; learning_goal: string }
export interface Candidate { candidate_id: string; content_hash: string; payload: Payload }
export interface Saved {
  id: string; content_hash: string; payload: Payload; material: Material
  review_status: string; review_version: number
  review: { note?: string; evidence?: { claim_text: string; quote: string; start: number; end: number; supported: boolean }[] }
}
export interface CardListItem { id: string; summary: string; review_status: string }
export interface Info { live_enabled: boolean; historical_material: string; notice: string }

// Promise<T>表示未来得到T；await等待响应，不阻塞整个浏览器界面。
export async function request<T>(path: string, method = 'GET', body?: unknown): Promise<T> {
  let response: Response
  try {
    response = await fetch(`/api/v1${path}`, {
      method, headers: { 'Content-Type': 'application/json', 'X-Stage2-Local': '1' },
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new Error('连接步骤失败：检查本机服务；请求可能已执行，请先读取记录。')
  }
  const result = await response.json().catch(() => null)
  if (!response.ok || result === null) {
    throw new Error(result?.error?.message
      ? `[${result.error.stage}] ${result.error.message}`
      : `请求失败（HTTP ${response.status}），请检查本机服务。`)
  }
  return result as T
}

export function fetchCard(cardId: string): Promise<Saved> {
  return request<Saved>(`/cards/${encodeURIComponent(cardId)}`)
}
