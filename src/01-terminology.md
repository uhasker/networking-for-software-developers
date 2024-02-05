# Introduction

## Internet Protocol Suite

Often the Internet protocol suite is used:

1. Link layer (IEEE802.3, IEEE802.11)
2. Internet layer (IPv4, ICMPv4)
3. Transport layer (TCP, UDP)
4. Application layer (DHCP, HTTP, HTTPS, DNS, SMTP, SSH)

> Often the OSI model is used instead.
> We will stick to the Internet procotol suite.

## Network Interfaces

A network interface is point of interconnection between a computer and a network.

They can be physical (representing a Network Interface Controller which is the computer hardware component that connects a computer to a network).
They can also be virtual (i.e. provided by software and have no physical equivalent).

Example:

- `lo` for loopback (virtual)
- `enp5s0` for Ethernet (physical)
- `wlp4s0` for WLAN (physical)
- `docker0` for Docker purposes (virtual, if you have Docker installed)

## Unicast, Multicast and Broadcast

A unicast address defines a single point in a network (e.g. one device).

A multicast address defines a group of all points in a network.

A broadcast address defines all points in some network.

## Bridges, Switches and Routers

Bridges usually connect LAN segments to create a larger network.

Switches usually connect devices within a LAN.

Routers usually connect multiple networks together.

However, this terminology is not universal.

## Tools

You will need the following tools:

- wireshark
- aircrack-ng
- bridge-utils

We will use python to write code.
Install the following packages:

- scapy

Note that you will need to run most of the tools as root.
We will not mention this again within the book and we will not prefix the respective commands with `sudo` to cut down on irrelevant noise.

## TODOS

Add notes on:

- how to read a hex dump
- how to start a Wireshark capture
