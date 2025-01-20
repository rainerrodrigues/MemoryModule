from myhdl import block, always, Signal, intbv, instance, delay, StopSimulation

@block
def SyncRAM(data_out, data_in, addr, we, clk, mem_size):
	"""
	Synchronous RAM
	
	data_out	- Data output from the RAM
	data_in	- Data input to the RAM
	addr		- Address bus
	we		- Write enable signal
	clk		- Clock signal
	mem_size	- Size of the memory
	"""
	
	memory = [Signal(intbv(0)[8:]) for _ in range(mem_size)]
	
	@always(clk.posedge)
	def logic():
		if we: #Enabled writing operation
			memory[int(addr)].next = data_in
		data_out.next = memory[int(addr)]
		
	return logic
