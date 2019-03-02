# SIH-RainWater-Harvesting
SIH submission for GoldMan Sachs' problem statement at NIT Calicut
  
### Planned components:
1. Rooftop Detection (`Watershed Algorithm` + `Canny Edge Detection`)
2. Depth Estimation + Volume Calculation (Of the water collected)
3. Rainfall Prediction
4. Calculator (Cost of installation + Break-Even analysis)
5. Tax Benefits
6. Non-Drinking Water Usage Prediction
7. Ground Water Replenish Plan (Phase 1)
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
