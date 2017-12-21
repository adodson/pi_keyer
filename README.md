# pi_keyer
A ham radio keyer for raspberry pi

This is an interactive line-oriented command interpreter that takes keyboard input and will key an amateur radio transciever via the key jack. It pulses a GPIO pin at the proper timing for sending morse code. The pin should be connected to an opto-coupler that closes the key jack circuit for the rig.

https://www.youtube.com/watch?v=FAvxJNbKl5I

Thanks to Paul, M0XPD for some hints here: http://m0xpd.blogspot.com/2012/12/keyer-on-rpi.html

### Features
- command line behavior familiar to unix shell users
- handles arbitrary prosigns
- store callsign and RST messages for easy retrieval
- adjustable WPM setting
