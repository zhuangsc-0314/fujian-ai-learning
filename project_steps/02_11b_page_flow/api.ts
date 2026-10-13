/**
 * TODO USER：2.11-B开课时实现本机API读取及错误处理。
 * 输入卡片ID，返回经过响应检查的卡片；读取不得触发模型生成。
 * unknown表示必须先检查响应形状，不能直接假设是成功卡片。
 * 当前无前端依赖/构建配置，不能运行或宣称已联调。
 */
export async function fetchCard(cardId: string): Promise<unknown> {
  void cardId; // 骨架暂未使用；实现时移除这一行。
  throw new Error("2.11-B读取卡片TODO尚未实现");
}
