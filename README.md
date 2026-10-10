# Chatterbox

The Chatterbox is a tiny motion-controlled, talkative desktop pet, similar to a desktop Tamagotchi.

# Features
- Tilt-controlled radial menu
- Tiny virtual pet on-screen
- Reactions (of the pet) to outside stimuli
- Pet talking on being disturbed
- Motion, tilt and environment sensors
- Compact PCB design

# Why it was built
The Chatterbox was built for the Hack Club YSWS Program - Half Life, drawing inspiration from the project [Starbie]([https://www.example.com](https://github.com/SharKingStudios/Starbie/blob/main/README.md)). The purpose of this project was to learn how to design PCBs while working on a meaningful project at the same time.

# Building it!
Following the Starbie tutorial, the PCB schematic for this project was initially created on KiCAD. After verifying all connections, the components were assigned to the appropriate footprints, and placed on the PCB. They were compactly arranged inside a custom outer boundary and routed along with ground fills. 

The firmware is nearly identical to that of the Starbie. The tiny virtual pet on the OLED has different energy, joy, and fullness levels, and reacts to stimuli (tilting, shaking) by performing different reactions such as napping, running, jumping etc. 
However, to enable the Chatterbox to speak, two extra files, 'wav2header.py' and 'audio.h' had to be created, to convert voice recordings (.wav's) to playable audio on the Chatterbox speaker. The first file converts the .wav recordings to C++ arrays, and the second streams this to the amplifier to be played on the speaker. I created these mainly using online tutorials, and AI did help me write a few parts.

# Components
This project was built using the following components:
* XIAO-ESP32-C3
* 1W Speaker
* MAX98357A Amplifier
* DHT11 temperature and humidity sensor
* MPU6050 accelerometer and gyroscope
* 0.96 OLED screen
* Kailh Switches
* DSA keycaps

# What I learnt
This was one of the first hardware projects I've done, and I learnt a lot, including - 
- how to fill ground areas in kicad
- the process for converting wav files to c++ headers
- running queues and tasks on freertos

# Images and Renders
The final schematic looks like this:
<img width="1127" height="725" alt="Schematic" src="https://github.com/user-attachments/assets/db617f8f-5504-45f9-9211-ffc6cfcafc1b" />

And this is the final PCB:

<img width="597" height="437" alt="Final PCB" src="https://github.com/user-attachments/assets/140f2e3c-1f9b-446b-bf70-fc5b87933f77" />

A 3D render of the PCB:

<img width="701" height="445" alt="3D Render of PCB" src="https://github.com/user-attachments/assets/1fe3d98d-58e7-4e55-9fc4-503246da34f5" />

# Credits
This project would not have been possible without the constant support of the Halflife community, and the detailed guidance given in the Starbie guide. I loved designing this project and I can't wait to build the PCB!


