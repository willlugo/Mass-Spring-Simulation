# Mass-Spring-Simulation
Mass-Spring Simulation using Python and rendered in Pygame

As my first independent foray into OOP I built in python a simulation for mass-spring systems. The simulation uses pygame to render the simulation and any amount of masses, fixed points, and springs can be added. Fixed points are created through the class wall and are used to connect a mass to a fixed point by a spring, they need only be given an x and y coordinate. (0, 0) is the center of the display, x is positive to the right, and y is positive downwards. masses can be created using the mass class, they must be provided with a beginning x and y value, a mass, and initial x and y velocities. It is best practice to create the springs after all masses and fixed points as they take these objects as their arguments. Springs are created through the spring class and must be provided with the two objects they are to connect, a stiffness value, and a natural length. When creating these objects, they should then be added to the list of that type of class. There may be a better way to do that but I don't know what it is.


key values to change:

Line 130    - SCALE         - This is the scale by which the base lengths will be multiplied to turn into pixel lengths in order to be displayed

Line 132    - FPS           - The rate at which the screen and simulation will update. Increasing this value will also increase the rate at which computations are performed up to the limit of the PC.

Line 134    - TIMESTEP      - Time is discretised in this simulation, decreasing the timestep will give more a more accurate simulation at the cost of it running slower.

Line 136    - WIDTH, HEIGHT - Change these values to change the physical size in pixels of the window.

After Line 149, Before while run:, define masses, followed by fixed points, followed by springs, and insert them into the appropriate list.