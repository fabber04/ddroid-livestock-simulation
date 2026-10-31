


Test Flow

The test flow sends four simulated messages:

LOW — low-water-level event
FULL — water point full event
STOP — stop command
cow-out — cow-outside alert
Tools Used
Node-RED
JSON flow export
How to Run
Install and start Node-RED.
Open http://localhost:1880 in a browser.
Import livestock_waterpoint_test_flow.json using the Node-RED menu's Import option.
Click Deploy.
Trigger each Inject node and inspect the Debug sidebar.
Test Results

All four messages were displayed correctly as strings in their respective Debug nodes during the direct message-delivery tests.

Limitations

These tests verify message delivery only. They do not yet verify Switch routing, physical sensors, motors, or a real livestock-tracking device.