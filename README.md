# 测试Loop Engineering

## 跳过所有确认，可以使用如下命令启动
claude --permission-mode bypassPermissions

然后输入如下命令，查看效果：
/loop 5m 执行 run-loop技能

5m为循环时间，如果当前轮执行超过5m，从此轮结束时执行下一轮。