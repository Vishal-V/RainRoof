# SIH-RainWater-Harvesting
SIH submission for GoldMan Sachs' problem statement at NIT Calicut
  
### Planned components:
1. Rooftop Detection (`Watershed Algorithm` + `Canny Edge Detection`)
2. Depth Estimation + Volume Calculation (Of the water collected)
3. Rainfall Prediction
4. Calculator (Cost of installation + Break-Even analysis)
5. Tax Benefits
6. Non-Drinking Water Usage Prediction
7. Basic Shared Rainwater Harvesting System (Phase 1)
8. Water Credit System Plan (Phase 2)
---
### Problem Statement
Currently, for roof top rain water harvesting, people install water storage tanks individually per building/apartment which results in high cost for individuals/groups. No mechanism/application is available to find out where such installations are beneficial, which installations can share storage tanks and what would be the required capacity of these shared tanks. Given map and housing data, optimize the location of centralized tanks for rain-water harvesting.The following data should be sufficient to design and implement a model to solve the problem: 
1. Estimating rainwater harvesting capacity: a. Rainfall estimation: Historical data from rainfall gauges at different places in the target area. b. Catchment area: Masterplan of the city to estimate the catchment area available, e.g open areas like rooftop, courtyard, etc.  
2. Optimizing Water tank placement:  
   - a. Water demand/Use capacity: Water supply data can be used to estimate the consumption of harvested rainwater for non-drinking purposes 
   - b. Underground map: Underground map with stability study to identify locations where the shared tank can be built The system should provide the following output from its analysis: 
      - 1. Plan for laying out the underground tanks with input and output points defined 
      - 2. Cost benefit analysis justifying the plan 
      - 3. Plan for distribution of build and maintenance cost of a tank for the parties involved
 ---
 ### Solutions
- #### Rooftop Detection can be carried out with three main approaches which are:
1. `YOLO Algorithm and Object Detection using Tensorflow`: This might result in problems of incorrect labelling of the rooftops and can lead to inaccuracy which becomes a problem to a certain degree posing a threat to deployability if seen on a massive scale.
2. `Open Computer Vision` is a graphical image processing library known for better processing of lower to higher resolution of images. Considering the case of India, getting high resolution satellite images for different inert areas is extremely difficult and thus needs a lot of preprocessing which is much easier and faster to carry out in OpenCV.
3. `Convolution Neural Networks` require a lot of preprocessing in case of satellite images and can become a problem if the availability of large amounts of data is not present. Though the performance increases with every forward propogation, the current architectural constraints in deploying Kubernetes clusters makes OpenCV the most viable option.
Thus, we have opted for the OpenCV approach to accurately detect, estimate and measure the roof dimensions.
![ALT-IMG](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/fig1.png)  
  
- #### 2. Depth Estimation and Volume Calculation (for the tank)
  - The tank dimensions are calculated from the rooftop catchment estimates obtained from contour mapping of the roof. The bounding boxes drawn on the roof takes the scale of the images into account and calculates the catchment area from the roof detected output
  - The contour mapping draws bounding boxes on the roof and outputs the catchment area in the location matrix limit as provided by the user's image.
  - The `Depth Estimation` is computed from the `Digital Elevation Modelling algorithm` that calculates the least elevation point by partitioning the image into boxes and then calculates the local minima of every box. The resulting global minima is considered as the least elevation point for the given area matrix.  
    
![ALT-IMG](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/static/images/dem.png)
 
