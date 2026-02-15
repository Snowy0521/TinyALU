import cocotb
from cocotb.triggers import RisingEdge, ClockCycles

class TinyAluBfm:
    def __init__(self, dut):
        self.dut = dut
        print("BFM initialized with DUT:", dut)

    async def reset(self):
        print("Starting reset...")
        self.dut.rst_n.value = 0
        await ClockCycles(self.dut.clk, 5) # 5 cycles of reset
        self.dut.rst_n.value = 1
        await RisingEdge(self.dut.clk) # Ensure reset is released on a clock edge
        print("Reset completed")
    

    async def send_op(self, op, aa, bb):
        print(f"BFM: Sending op={op}, A=0x{aa:02x}, B=0x{bb:02x}")
        self.dut.op.value = op
        self.dut.A.value = aa
        self.dut.B.value = bb
        self.dut.start.value = 1
        
        await RisingEdge(self.dut.clk) # Ensure start is registered on a clock edge
        
        # NOOP Operation special case
        if op == 0:  # NOOP
            self.dut.start.value = 0
            await RisingEdge(self.dut.clk) # Ensure start is deasserted on a clock edge
            print(f"BFM: NOOP operation, returning 0")
            return 0
        
        # Wait for done signal with a timeout
        timeout = 100 if op == 4 else 20  # MUL might take longer, so we give it more time
        for cycle in range(timeout):
            await RisingEdge(self.dut.clk)  # Ensure we check done on clock edges
            if self.dut.done.value == 1:
                result = int(self.dut.result.value)
                print(f"BFM: Got result=0x{result:04x} after {cycle+1} cycles")
                self.dut.start.value = 0
                await RisingEdge(self.dut.clk)
                return result
        
        # Timeout handling
        self.dut.start.value = 0
        print(f"BFM: TIMEOUT after {timeout} cycles!")
        print(f"BFM: Current signals - start={self.dut.start.value}, done={self.dut.done.value}, op={self.dut.op.value}")
        raise RuntimeError("Done timeout")

    async def get_result(self):
        await RisingEdge(self.dut.done)
        
        data = {
            'op':     int(self.dut.op.value),
            'aa':     int(self.dut.A.value),
            'bb':     int(self.dut.B.value),
            'result': int(self.dut.result.value)
        }
        return data