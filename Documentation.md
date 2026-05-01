



# ARP Spoofer 



This project is a Python-based security tool designed to perform \*\*ARP Spoofing\*\* (Man-in-the-Middle) and local network scanning. It leverages the `Scapy` library to manipulate network packets and redirect traffic between two targets on a local network.



\## 📖 What is an ARP Spoofer?



\*\*Address Resolution Protocol (ARP)\*\* is used to map IP addresses to physical MAC addresses within a local area network (LAN). 



An \*\*ARP Spoofer\*\* sends falsified ARP messages onto a local network. The goal is to associate the attacker's MAC address with the IP address of another host (such as a default gateway or a specific workstation). Once associated, any traffic intended for that IP address is sent to the attacker instead.







\### How it Works in this Code:

1\. The tool tells \*\*Target 1\*\* that "I (the attacker) am Target 2."

2\. The tool tells \*\*Target 2\*\* that "I (the attacker) am Target 1."

3\. By enabling \*\*IP Forwarding\*\*, the attacker's machine passes the traffic between the two targets, allowing them to communicate normally while the attacker intercepts the data.



\---



\## 🛠 Features



\*   \*\*Network Scanning:\*\* Automatically detects devices on the current subnet using ARP requests.

\*   \*\*Target Validation:\*\* Verifies if the target IPs are active before initiating the spoof.

\*   \*\*Automated IP Forwarding:\*\* Enables Linux kernel IP forwarding so the targets don't lose internet connectivity.

\*   \*\*Custom Duration:\*\* Allows the user to set a specific time limit for the spoofing session.



\---



\## 🚀 Use Cases



\*   \*\*Security Research:\*\* Understanding how MITM (Man-in-the-Middle) attacks occur in unsecured networks.

\*   \*\*Protocol Analysis:\*\* Intercepting unencrypted traffic (like HTTP or FTP) for educational packet analysis.

\*   \*\*Network Troubleshooting:\*\* Testing how a network handles duplicate MAC address entries or ARP storms.



\---



\## 💻 Code Details



The script is divided into several logical functions:



\### 1. `scan(ip\_address)`

Uses an Ethernet broadcast (`ff:ff:ff:ff:ff:ff`) to send ARP requests to a range of IPs. It returns a dictionary mapping IP addresses to their corresponding MAC addresses.



\### 2. `option\_fucn()`

Handles command-line arguments using `argparse`. 

\*   `-s`: Scans the network.

\*   `-t1 / -t2`: Sets the two targets for the spoofing attack.

\*   `-d`: Sets the duration in minutes.



\### 3. `arpspoof(dict1)`

The core engine of the script. It:

\*   Retrieves the attacker's MAC address.

\*   Crafts `op=2` (ARP Reply) packets.

\*   Runs a `while` loop to continuously "poison" the ARP cache of the targets (to prevent them from correcting their tables).

\*   Enables IP forwarding via `subprocess` to ensure traffic flows through the machine.



\---



\## ⚠️ Requirements \& Setup



1\.  \*\*Dependencies:\*\*

&#x20;   ```bash

&#x20;   pip install scapy

&#x20;   ```

2\.  \*\*Permissions:\*\* 

&#x20;   This script requires \*\*root/administrator\*\* privileges because it creates raw network packets.

&#x20;   ```bash

&#x20;   sudo python3 arp\_spoofer.py -t1 \[IP1] -t2 \[IP2] -d 10

&#x20;   ```

3\.  \*\*OS:\*\* Designed primarily for \*\*Linux\*\* (due to the `/proc/sys/net/ipv4/ip\_forward` path used for port forwarding).



\---



\## 🛑 Disclaimer

\*This tool is for educational and ethical testing purposes only. Unauthorized access to networks or interception of data is illegal and unethical. Use only on networks you own or have explicit permission to test.\*

```

