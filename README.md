# SIH-RainWater-Harvesting
SIH submission for GoldMan Sachs' problem statement at NIT Calicut. 
- At this time, the entire project is ready to be deployed and runs on a Flask middle-tier. All values are real-time satellite images obtained from Google Maps API for the rooftop detection and estimation.   
- The machine learning aspect of our project was used to estimate the dimensions of the roof (`OpenCV` and `Computer Vision Models`) along with rainfall estimation using a rolling forecasting model. 
  
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
  
- #### 2. Depth Estimation using Digital Elevation Model (DEM)
  - The tank dimensions are calculated from the rooftop catchment estimates obtained from contour mapping of the roof. The bounding boxes drawn on the roof takes the scale of the images into account and calculates the catchment area from the roof detected output
  - The contour mapping draws bounding boxes on the roof and outputs the catchment area in the location matrix limit as provided by the user's image.
  - The `Depth Estimation` is computed from the `Digital Elevation Modelling algorithm` that calculates the least elevation point by partitioning the image into boxes and then calculates the local minima of every box. The resulting global minima is considered as the least elevation point for the given area matrix.  
    
![ALT-IMG](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/static/images/dem.png)
 
- #### 3. Rainfall Prediction
  - The rainfall prediction has been trained on 100 years' data for the city of Bangalore. We have used a time series plot uisng ARIMA models as well as a statistical analysis to obtain the values for various months.
![ALT](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/static/images/dash.png)  
- #### 4. Calculator (Cost of installation + Break-Even analysis)
  - This is the complete analysis pipeline for the project. It initially starts with the user uploading a satellite image from our Serach bar and the backend Computer Vision models(`OpenCV`) and machine learning models(`K-Means clustering`) calculate the catchment are of the rooftops under consideration.
  - The calculated area is then fed to our moldes to estimate the cost of installation of the entire setup and also finds the maintenance cost as well.
![ALT](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/static/images/calc.png)  
- #### 5. Non-Drinking Water Usage Research
    - This was a research oriented part of the project to estimate and validate the non-drinking water usage of a certain area that also takes the water usage and lifestyle into account.
    - The papers based on water usage was maonly for domestic purposes and very few for industrial usage. Hence, our end-to-end pipeline is a B2C model rather than a B2B model
  
- #### 6. Basic Shared Rainwater Harvesting System (Phase 1)
  - This is a fully working model of the Shared Rainwater Harvesting system that has an easy-to-use UI with accurate predictions using AI and Computer Vision models to predict the most optimal spot to detect the location to install the tank and also provides complete financial analysis and break-even time for the installation. Here, you can find the picture of the installation on our college hostel.
![ALT](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/static/images/point.png)
#### 7. Underground Map
  
  The problem of designing the underground map involves many parameters including obstacles beneath the ground a layout of the pipeline from inlet to outlet of the rainwater harvesting solution.  
  This essentially means that there is a requirement of searching algorithm to traverse a path which can be `optimal` and also does not traverse the path with obstacles. The obstacles can range from gas pipelines beneath the ground with a vulnerable range and sewage system under the ground as well as subway lines constructed. In this case scenario, the underground map needs to traverse a path which does not have any obstacle in the way and remains optimal atmost of the times thereby giving an effective and deployable solution.
    
The underground map consists of two phase possible implementation:
 1. Heat Map: The heat map of the region detects varied different objects under the ground and provides a label to each of them in form of a different colour. When provided with the data of locations of the obstacles such as gas pipelines it can be used to label the specific colour and then provide an optimal path to the tank such that it does not get into the path of the gas pipelines.
 2. Searching Technique: The final half of the underground map is to provide the optimal path which is cost effective and does not hinder the existing obstacles that is gas pipelines and sewage pipes underground. This is an effective and novel approach in simple fashion and can be a generic model that can be easily adapted by any rainwater harvesting solution. Best First Search is an optimal and useful technique implemented as a possible solution for this problem.
 ![ALT](https://github.com/Vishal-V/SIH-RainWater-Harvesting/blob/master/undeground_map.gif)

