import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.queue import Queue

class TinyAluBfm:
    def __init__(self, dut):
        self.dut = dut
        print("BFM initialized with DUT:", dut)
        self._driver_queue  = Queue()
        self._monitor_queue = Queue()
        self._pending_ops = []
        self._fatal_error = None
        self._cycle = 0
        cocotb.start_soon(self._monitor_loop())  # 后台持续监测 done

    def _read_resolvable_int(self, sig, name):
        val = sig.value
        if not val.is_resolvable:
            raise RuntimeError(f"{name} contains X/Z: {val}")
        return int(val)

    async def _publish_fatal_error(self, err):
        if self._fatal_error is None:
            self._fatal_error = err
            error_pkt = {"error": str(err)}
            await self._driver_queue.put(error_pkt)
            await self._monitor_queue.put(error_pkt)

    def _check_fatal_error(self):
        if self._fatal_error is not None:
            raise RuntimeError(str(self._fatal_error))

    async def reset(self):
        print("Starting reset...")
        self.dut.rst_n.value = 0
        await ClockCycles(self.dut.clk, 5) # 5 cycles of reset
        self.dut.rst_n.value = 1
        await RisingEdge(self.dut.clk) # Ensure reset is released on a clock edge
        print("Reset completed")
    
    # ── Driver 调用：只负责驱动激励 ──────────────────────────
    async def send_op(self, op, aa, bb):
        self._check_fatal_error()

        self.dut.op.value = op
        self.dut.A.value = aa
        self.dut.B.value = bb
        self.dut.start.value = 1
        
        await RisingEdge(self.dut.clk) # Ensure start is registered on a clock edge
        self.dut.start.value = 0
        
        # NOOP Operation special case
        if op == 0:
            await RisingEdge(self.dut.clk)
            self._check_fatal_error()
            noop_data = {
                'op':     0,
                'aa':     aa,
                'bb':     bb,
                'result': 0,
                'latency': 0,
                'done_width': 0
            }
            await self._monitor_queue.put(noop_data)  # 手动通知 Monitor
            return 0
        
        # 等待 _monitor_loop 把结果放进队列
        data = await self._driver_queue.get()
        if 'error' in data:
            raise RuntimeError(data['error'])

        return data['result']

    # ── Monitor 调用：只负责观测 ─────────────────────────────
    async def get_result(self):
        self._check_fatal_error()
        data = await self._monitor_queue.get()  # 阻塞直到有数据
        if 'error' in data:
            raise RuntimeError(data['error'])
        return data
    
    # ── 后台协程：持续检测 done，写入队列 ────────────────────
    async def _monitor_loop(self):
        prev_done = 0
        prev_start = 0
        try:
            while True:
                await RisingEdge(self.dut.clk)
                self._cycle += 1

                rst_n = self._read_resolvable_int(self.dut.rst_n, "rst_n")
                start = self._read_resolvable_int(self.dut.start, "start")
                op = self._read_resolvable_int(self.dut.op, "op")
                done = self._read_resolvable_int(self.dut.done, "done")

                if rst_n == 0:
                    self._pending_ops.clear()
                    prev_done = done
                    prev_start = start
                    continue

                if start == 1 and prev_start == 0 and op != 0:
                    aa = self._read_resolvable_int(self.dut.A, "A")
                    bb = self._read_resolvable_int(self.dut.B, "B")
                    self._pending_ops.append({
                        "op": op,
                        "aa": aa,
                        "bb": bb,
                        "start_cycle": self._cycle
                    })

                if op == 0 and done == 1:
                    raise RuntimeError(f"NOOP drives done high at cycle {self._cycle}")

                if done == 1 and prev_done == 1:
                    raise RuntimeError(f"done pulse width > 1 cycle at cycle {self._cycle}")

                # done 上升沿：出队一个请求并上报完整观测信息
                if done == 1 and prev_done == 0:
                    if len(self._pending_ops) == 0:
                        raise RuntimeError(f"done rose without pending operation at cycle {self._cycle}")

                    req = self._pending_ops.pop(0)
                    result = self._read_resolvable_int(self.dut.result, "result")
                    latency = self._cycle - req["start_cycle"]
                    data = {
                        'op': req['op'],
                        'aa': req['aa'],
                        'bb': req['bb'],
                        'result': result,
                        'latency': latency,
                        'done_width': 1
                    }
                    await self._driver_queue.put(data)
                    await self._monitor_queue.put(data)

                prev_start = start
                prev_done = done
        except Exception as err:
            await self._publish_fatal_error(err)

    async def check_reset_state(self):
        """Check that done and result are 0 after reset, and no X/Z states."""
        # 等一拍让信号稳定
        await RisingEdge(self.dut.clk)

        errors = []

        if not self.dut.done.value.is_resolvable:
            errors.append(f"done occurs X/Z state: {self.dut.done.value}")
        elif int(self.dut.done.value) != 0:
            errors.append(f"done should be 0, but is {self.dut.done.value}")

        if not self.dut.result.value.is_resolvable:
            errors.append(f"result occurs X/Z state: {self.dut.result.value}")
        elif int(self.dut.result.value) != 0:
            errors.append(f"result should be 0, but is {self.dut.result.value}")

        if errors:
            for e in errors:
                print(f"[RESET CHECK] FAIL: {e}")
            raise RuntimeError("Reset state check failed")
        else:
            print("[RESET CHECK] PASS: done=0, result=0, no X/Z states")
