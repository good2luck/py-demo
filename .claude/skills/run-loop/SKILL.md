---
name: run-loop
description: 自动调度和串联整个开发、隔离、审查和同步循环的核心中枢。
---

## 重要：此技能运行在 cron loop 中，不要手动删除 cron 任务
- 此技能由 `/loop` 命令触发的 cron 定时任务调用。
- **禁止**在技能执行过程中调用 `CronDelete` 取消定时器。
- 每个迭代完成后应自然结束，等待下一次 cron 触发。
- 仅当 TASKS.md 的 "待处理" 列表为空时，才输出 "暂无待处理任务，等待下次检查" 并结束。

# 核心调度流程

## 第一阶段：发现问题 (Triage)
1. 调用 `commit-triage` 技能，自动分析并更新项目根目录下的 `TASKS.md`。

## 第二阶段：循环处理每个任务 (Execute & Worktree)
1. 读取更新后的 `TASKS.md`。如果有 "## 待处理 (Todo)" 列表中的任务：
   - 挑出其中一个任务，并将其移动到 `TASKS.md` 中的 "## 进行中 (In Progress)" 列表中。
   - 使用项目根目录的**绝对路径**拼接工作区路径，创建临时隔离工作区（Worktree）：
     `git worktree add $PROJECT_ROOT/../worktrees/task-temp -b feature/task-temp`
   - 子代理操作时直接使用该绝对路径。

2. **指派干活**：
   - 调用 **@coder-reviewer** 子代理，向其说明要在该工作区内执行的具体任务。
   - 等待 @coder-reviewer 完成编写。

3. **对抗审查与测试**：
   - 在该工作区目录内，调用 **@code-security-reviewer** 子代理。
   - 催促 @code-security-reviewer 对本次修改进行代码审计并运行测试命令。
   - **决策分支**：
     - 若 @code-security-reviewer 给出 [FAIL]：将修改意见反馈给 @coder-reviewer，要求其继续修复，直至 @code-security-reviewer 给出 [PASS]。
     - 若 @code-security-reviewer 给出 [PASS]：进入下一阶段。

## 第三阶段：合并、清理与通知 (Sync & Cleanup)
1. 测试通过后，在临时工作区内运行 Git 提交和推送：
   `git add .`
   `git commit -m "fix: 自动修复任务"`
2. 返回项目主目录（即原项目根目录）。
3. 安全移除隔离工作区（使用绝对路径，避免相对路径解析错误）：
   `git worktree remove $PROJECT_ROOT/../worktrees/task-temp`
   `git branch -D feature/task-temp`
   `git worktree prune`
4. 将该任务从 `TASKS.md` 的 "## 进行中" 移至 "## 已完成 (Done)"，并注明完成时间。
5. **发送通知**：
   - 运行系统级通知命令传达消息。
   - *Mac 系统*：`osascript -e 'display notification "任务已修复并通过测试！" with title "Claude Loop 自动通知"'`
   - *通用*：`echo "==== [通知] 任务已成功修复并安全合并！ ===="`