## 深度拷打当前验证思想

---

## 第二刀：检查机制不完整

**问题：Scoreboard 只检查结果，不检查时序**

当前 `check_result` 只比较数值对不对，但完全没有检查：

```python
# 当前 scoreboard 只做这个
if actual != expected:
    self.logger.error("FAIL")

# 缺少的检查：
# 1. done 信号是否在正确的周期拉高？
#    ADD/AND/XOR 应该1拍后 done
#    MUL 应该恰好3拍后 done

# 2. done 是否只持续1拍？
#    如果 done 持续2拍，scoreboard 根本发现不了

# 3. NOOP 时 done 是否始终为0？
```

**时序检查应该在 monitor 里做：**

```python
class AluMonitor(uvm_component):
    async def run_phase(self):
        while True:
            obs_data = await self.bfm.get_result()
            
            # 检查时序是否符合预期
            expected_latency = 3 if obs_data['op'] == Ops.MUL else 1
            if obs_data['latency'] != expected_latency:
                self.logger.error(f"时序错误: 期望{expected_latency}拍，实际{obs_data['latency']}拍")
```

**问题：没有检查 X/Z 传播**

DUT 输出可能出现 X 态，当前代码直接 `int(dut.result.value)` 会把 X 转成随机数，静默掩盖了问题：

```python
# 危险写法（当前代码）
'result': int(self.dut.result.value)

# 安全写法
val = self.dut.result.value
if val.is_resolvable:
    result = int(val)
else:
    raise RuntimeError(f"result 出现 X/Z 态: {val}")
```

---

## 第三刀：覆盖率模型缺陷

**问题：覆盖率和功能验证脱节**

当前覆盖率只统计了输入组合，但没有覆盖**功能点**：

```python
# 当前覆盖的：输入空间
CoverPoint("top.aa", bins=[0, 1, 127, 128, 254, 255])

# 缺少的：功能场景覆盖
CoverPoint("top.add_carry",      # 加法是否产生进位
           xf=lambda item: item.op == Ops.ADD and (item.aa + item.bb) > 0xFF,
           bins=[True, False])

CoverPoint("top.mul_overflow",   # 乘法是否溢出16位
           xf=lambda item: item.op == Ops.MUL and (item.aa * item.bb) > 0xFFFF,
           bins=[True, False])

CoverPoint("top.and_zero",       # AND 结果是否为0
           xf=lambda item: item.op == Ops.AND and (item.aa & item.bb) == 0,
           bins=[True, False])

CoverPoint("top.xor_same",       # XOR 两个相同的数
           xf=lambda item: item.op == Ops.XOR and item.aa == item.bb,
           bins=[True, False])
```

**问题：没有覆盖率收敛机制**

当前跑固定 200 笔就结束，不管覆盖率有没有到100%：

```python
# 当前
for i in range(200):
    ...

# 应该
while not coverage_closure():
    await seq.start(seqr)
    if iteration > MAX_ITER:
        self.logger.error("覆盖率未收敛")
        break
```

---

## 第四刀：环境架构问题

**问题：Agent 是 active 还是 passive 没有区分**

标准 UVM 的 agent 有两种模式：

```
active mode：有 driver，会驱动 DUT（当前的用法）
passive mode：只有 monitor，用于连接到真实硬件或其他 DUT
```

当前代码没有这个概念，`AluAgent` 永远是 active 的，无法复用到其他场景。

**问题：缺少 virtual sequencer**

假设 TinyALU 以后要集成进一个更大的系统，有多个 agent，需要协调多个 sequencer 的激励顺序，当前架构无法支持：

```python
class VirtualSequencer(uvm_sequencer):
    """协调多个 agent 的激励"""
    def build_phase(self):
        self.alu_seqr = None  # 指向 AluAgent 的 sequencer
        self.bus_seqr = None  # 指向总线 Agent 的 sequencer
```

**问题：缺少 predictor（参考模型）**

当前 scoreboard 自己计算期望值，验证逻辑和检查逻辑耦合在一起：

```
当前：
Monitor → Scoreboard（既算期望值，又做比较）

标准做法：
Monitor → Predictor（只算期望值）→ Scoreboard（只做比较）
                                          ↑
                               Monitor 也直接连过来
```

分离的好处是 Predictor 可以替换成更复杂的参考模型（比如调用 C 模型或 Python 库）。

---

## 第五刀：可观测性不足

**问题：没有波形自动分析**

出错时只打印数值，工程师还要手动开波形找原因：

```python
def check_result(self, item):
    if actual != expected:
        self.logger.error(f"FAIL at sim_time={cocotb.utils.get_sim_time('ns')}ns")
        # 应该同时记录：
        # 1. 出错时刻的仿真时间
        # 2. 前后几拍的信号状态
        # 3. 自动标注波形（VCD annotation）
```

**问题：没有事务级日志**

所有打印混在一起，调试困难。应该用 UVM 的 verbosity 机制：

```python
self.logger.debug(f"详细时序信息")    # 默认不显示
self.logger.info(f"事务摘要")         # 默认显示
self.logger.error(f"错误信息")        # 永远显示
```

---

## 总结：验证完整性评分

| 维度 | 当前状态 | 工业标准 | 差距 |
|------|---------|---------|------|
| 时序检查 | 无 | 完整时序断言 | ★★★★ |
| 功能覆盖率 | 输入空间覆盖 | 功能点覆盖 | ★★★ |
| 复位验证 | 无 | 完整复位场景 | ★★★★ |
| X态检测 | 无 | 强制检查 | ★★ |
| 参考模型 | 内嵌scoreboard | 独立predictor | ★★ |
| 环境复用性 | 低 | active/passive切换 | ★★ |

**最优先改进的两点**：时序检查和复位验证，这两个是最容易漏掉真实 bug 的地方，也是面试最常被问到的点。