This is a simple, python3-based UI front end for the Proxmark 3 client to allow a user to read, write, or erase a LF T5577 card in the EM410x format. Useful for a CTF challenge where we don't expect/want the players to use the full PM3 client. 

Dependencies:
- Python 3
- GuiZero 1.4 or later (sudo apt-get -y install python3-guizero)
- [Proxmark 3 client](https://github.com/RfidResearchGroup/proxmark3) installed and in the system path (See [install instructions](https://github.com/RfidResearchGroup/proxmark3?tab=readme-ov-file#proxmark3-installation-and-overview))

Assumptions:
- Being run on Linux
- Proxmark hardware is using /dev/ttyACM0

This should work on Windows, but the address of the proxmark would need to be changed. 

Verified working on Linux Mint 22.1 with proxmark3-v4.20142 client and a Proxmark 3 RDV4. 

Screenshot:
![Screenshot of client UI](cardwritescreenshot.png?raw=true "UI Screenshot")
