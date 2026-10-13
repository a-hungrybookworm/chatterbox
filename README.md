# The Chatterbox

<img width="1127" height="825" alt="Chatterbox" src="https://github.com/user-attachments/assets/140f2e3c-1f9b-446b-bf70-fc5b87933f77" />

The Chatterbox is a tiny motion-controlled, talkative digital pet, basically a desktop Tamagotchi, or a Starbie that talks.

# Features
- Tilt-controlled radial menu
- Tiny virtual pet on-screen
- Motion, tilt and environment sensing
- Unique pet actions, stats, dialogues
- Compact PCB design

# Why it was built
The Chatterbox was built for the Hack Club YSWS Programme [Halflife](https://halflife.hackclub.com/), drawing inspiration from the project [Starbie](https://github.com/SharKingStudios/Starbie/blob/main/README.md). 

# Components
This project was built using the following components:
* XIAO-ESP32-C3
* 1W Speaker
* MAX98357A amplifier
* DHT11 temperature and humidity sensor
* MPU6050 accelerometer and gyroscope
* 0.96 OLED screen
* Kailh switches
* DSA keycaps

# Building it!
Following the Starbie tutorial, the PCB schematic for this project was initially created on KiCAD. After verifying all connections, the components were assigned footprints, and placed on the PCB. They were compactly arranged inside a custom outer boundary and routed along with ground fills. 

The firmware is nearly identical to that of the Starbie. The tiny virtual pet on the OLED has different energy, joy, and fullness levels, and reacts to stimuli (tilting, shaking) by performing different reactions such as napping, running, jumping etc. 

However, to enable the Chatterbox to speak (unlike the Starbie), I had to write code to convert voice recordings (.wav's) to playable audio on the Chatterbox speaker. The .wav recordings are first processed into mono 16kHz audio, and then converted to C++ header files. They're compiled into the firmware, stored in the ESP32's flash on uploading, and a background FreeRTOS task streams the audio to an amplifier at runtime, which plays it on a speaker without interrupting the pet's animations.

# What I learnt
This was one of the first hardware projects I've done, and I learnt a lot, including how to - 
- add power symbols and nets in KiCAD
- fill ground areas in KiCAD
- process wav audio
- create tasks and queues on FreeRTOS (on the ESP32)

# Images and Renders
The final schematic looks like this:
<img width="1127" height="725" alt="Schematic" src="https://github.com/user-attachments/assets/db617f8f-5504-45f9-9211-ffc6cfcafc1b" />

And this is the final PCB:

<img width="1127" height="825" alt="Final PCB" src="https://github.com/user-attachments/assets/140f2e3c-1f9b-446b-bf70-fc5b87933f77" />

A 3D render of the PCB:

<img width="1127" height="715.43" alt="3D Render of PCB" src="https://github.com/user-attachments/assets/1fe3d98d-58e7-4e55-9fc4-503246da34f5" />

# Credits
This project would not have been possible without the constant support of the Halflife community, and the detailed guidance given in the Starbie guide. I loved designing this project and I can't wait to build the PCB!


