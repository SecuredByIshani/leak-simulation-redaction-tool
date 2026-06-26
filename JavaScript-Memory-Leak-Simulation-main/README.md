**Memory Leak Simulation for a JavaScript Web App"**

>This is a simple JavaScript web app to simulate a memory leak. This can be used to understand how memory leaks occur and how to detect and debug them.
>
><img width="247" alt="image" src="https://github.com/Buchatech/memoryleakbutton/assets/22551494/30f6b29c-c51a-40da-a87d-738e8e4ea413">


## The App: 
**HTML File (index.html)**:

- Contains two buttons: one to *start* the memory leak and one to *stop* it.

**JavaScript File (app.js)**:

- **memoryLeakArray:** An array that will keep references to the created objects, preventing them from being garbage collected.
- **leakInterval:** Holds the reference to the setInterval function to control the memory leak simulation.
- **startLeak button:** Starts the memory leak by creating objects and storing them in the memoryLeakArray every second.
- **stopLeak button:** Stops the memory leak by clearing the interval.

## Steps to Run
1. Create a repository on GitHub for the project and save index.html and app.js in it.
2. Deploy the web app. I recommend using a static site in render.com.
3. Open the site in a web browser.
4. Open the browser's Developer Tools in Edge or Chrome>Performance (Ctrl+Shift+I).
5. Click the "Start Memory Leak" button to start the memory leak simulation.
6. Observe the memory consumption in the "Performance" or "Memory" tab in Developer Tools.
7. Click the "Stop Memory Leak" button to stop the simulation.

**Example in Chrome Developer Tools>>Performance:**

<img width="704" alt="image" src="https://github.com/Buchatech/memoryleakbutton/assets/22551494/cac82e19-9ad3-40d8-9c6b-41da471e3d0f">



>This simple JavaScript web app demonstrates how continuously allocating memory without releasing it can cause a memory leak. In real applications, memory leaks can occur in various ways. This is one example so you can test it using developer tools.

>If you dont want to deploy your own site and just want to try it out check the site here: [JavaScript Memory Leak Simulation Web App](https://javascript-memory-leak-simulation.onrender.com).
