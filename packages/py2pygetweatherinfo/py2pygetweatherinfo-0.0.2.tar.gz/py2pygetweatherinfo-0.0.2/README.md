Weather Application Web Crawling Task 
 
It gives hourly, daily, 5-days, 10-days and monthly weather forecasts. 
 
Investigate the site to find the type of forecasts available. 
Develop a command line application that takes as input 
	1. Place  
	2. Date (optional, default = current time) 
	3. Type of forecast (optional, default = daily) 
The application should use the discovered endpointed (used internally by the site) to fetch the result 
Output the result to the console in any convenient format. 
Essential 
	Proper repository and package structure. 
	The application has to be pip installable. 
	Compliance with PEP8 
Optional 
	Clean architecture: make the core of the application agnostic of the command line stuff (UI) 
	As the core application is decoupled from the UI, build a web service (JSON API) for it. 