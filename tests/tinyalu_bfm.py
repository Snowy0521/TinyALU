import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
from cocotb.queue import Queue

class TinyAluBfm:
    def __init__(self, dut):
        self.dut = dut
        print("BFM initialized with DUT:", dut)
        self._driver_queue  = Queue()
        self._monitor_queue = Queue()
        cocotb.start_soon(self._monitor_loop())  # 后台持续监测 done

    async def reset(self):
        print("Starting reset...")
        self.dut.rst_n.value = 0
        await ClockCycles(self.dut.clk, 5) # 5 cycles of reset
        self.dut.rst_n.value = 1
        await RisingEdge(self.dut.clk) # Ensure reset is released on a clock edge
        print("Reset completed")
    
    # ── Driver 调用：只负责驱动激励 ──────────────────────────
    async def send_op(self, op, aa, bb):
        self.dut.op.value = op
        self.dut.A.value = aa
        self.dut.B.value = bb
        self.dut.start.value = 1
        
        await RisingEdge(self.dut.clk) # Ensure start is registered on a clock edge
        
        # NOOP Operation special case
        if op == 0:
            self.dut.start.value = 0
            await RisingEdge(self.dut.clk)
            noop_data = {
                'op':     0,
                'aa':     int(self.dut.A.value),
                'bb':     int(self.dut.B.value),
                'result': 0
            }
            await self._monitor_queue.put(noop_data)  # 手动通知 Monitor
            return 0
        
        # 等待后台 monitor_loop 把结果放进队列
        # 等待 _monitor_loop 把结果放进队列
        data = await self._driver_queue.get()

        self.dut.start.value = 0
        await RisingEdge(self.dut.clk)
        return data['result']

    # ── Monitor 调用：只负责观测 ─────────────────────────────
    async def get_result(self):
        return await self._monitor_queue.get()  # 阻塞直到有数据
    
    # ── 后台协程：持续检测 done，写入队列 ────────────────────
    async def _monitor_loop(self):
        prev_done = 0
        while True:
            await RisingEdge(self.dut.clk)
            curr_done = int(self.dut.done.value)
            
            # 只在 done 上升沿采样一次，不重复
            if curr_done == 1 and prev_done == 0:
                data = {
                    'op':     int(self.dut.op.value),
                    'aa':     int(self.dut.A.value),
                    'bb':     int(self.dut.B.value),
                    'result': int(self.dut.result.value)
                }
                await self._driver_queue.put(data)
                await self._monitor_queue.put(data)
            
            prev_done = curr_done