A small tool where you can upload a photo and easily map out RGB LEDs to create a plugin for Signal RGB.

Script requires pillow, numpy, scipy, and tkinter to run. These can be installed using pip.

When you run it, you'll see the default screen:

![No image](https://github.com/user-attachments/assets/0f9e8876-3dec-4e77-97cf-b71dab0945a7)

Add your number of LEDs. For some cheap AIO tube lights I picked up, they have 30 lights, so I changed the Number of LEDs to 30 and clicked Upload Background to add a phohto of my rig for placement.

![Upload Background](https://github.com/user-attachments/assets/38bd4166-923f-4d1a-b281-9f395596a652)

Then to make the shape, I click Draw Spline and add points roughly along the center of the LED tube. This can be roughly done; a spline fit will be added to create a curved line joining all points.

![Draw Spline](https://github.com/user-attachments/assets/426eb115-eb2b-4e58-ad7e-15e5f28ae9e7)

Double check the number of LEDs is correct, then click Place LEDs on Spline and it will automatically evenly space out the LEDs along the spline fit.

![Place LEDs](https://github.com/user-attachments/assets/85fc2a94-46a4-4b75-984c-eeba49c93561)

Finally, click Output Plugin to save the LED positions in a format usuable in SignalRGB. The format of this is based in the output from https://srgbmods.net/ 
