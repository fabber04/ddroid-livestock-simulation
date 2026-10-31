Node-RED Test Results

Project: Livestock Tracking and Water Point Droid

Test date: 29 October 2026

Testing tool: Node-RED Debug sidebar

Test ID	Input	Expected Result	Actual Result	Status
TC01	LOW	"LOW" displayed as a string	string[3], "LOW"	PASS
TC02	FULL	"FULL" displayed as a string	string[4], "FULL"	PASS
TC03	STOP	"STOP" displayed as a string	string[4], "STOP"	PASS
TC04	cow-out	"cow-out" displayed as a string	string[7], "cow-out"	PASS
Conclusion

All four direct message-delivery tests passed. Each Inject node delivered the expected string to its corresponding Debug node.

Limitations

The tests did not verify Switch-node routing or actual hardware behaviour. Those tests must be conducted separately if these features are part of the final system.