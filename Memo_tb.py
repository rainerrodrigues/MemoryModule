from myhdl import block, always,Signal, intbv, instance, delay, StopSimulation
from Memo import SyncRAM

@block 
def testbench():
	clk = Signal(bool(0))
	data_out = Signal(intbv(0)[8:])
	data_in  = Signal(intbv(0)[8:])
	addr = Signal(intbv(0, min=0, max=16)) #Address bus for 16 locators
	we = Signal(bool(0))
	mem_size = 16
	
	ram = SyncRAM(data_out, data_in, addr, we, clk, mem_size)
	
	@always(delay(5))
	def clkgen():
		clk.next = not clk
		
	@instance
	def stimulus():
		print("Starting RAM Test...")
		
		# Write data to RAM
		for i in range(mem_size):
			addr.next = i
			data_in.next = i * 3
			we.next = True
			yield clk.posedge
			we.next = False
			yield clk.posedge
			print(f"Written {int(data_in):02x} to Address {addr}")
			
		# Read back data from RAM
		for i in range(mem_size):
			addr.next = i
			yield clk.posedge
			yield delay(1) # Ensure that the data output stabilizes
			print(f"Address {i}: Read {int(data_out):02x}, Expected: {i * 3:02x}")
			assert data_out == i * 3,f"Mismatch at address {i}"
			
		print("RAM Test Passed")
		raise StopSimulation()
		
	return ram, clkgen, stimulus
	
#Run the testbench
if __name__ == "__main__":
	Memo_tb = testbench()
	Memo_tb.config_sim(trace=True)
	Memo_tb.run_sim()
