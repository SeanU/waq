# WAQ
UC Berkeley MIDS Capstone - Water Air Quality Project

This repository contians the work though several interations in the creation of the waq.dog website as part of the Capstone project for the MIDS program. 

To see this project in action please visit [waq.dog](http://waq.dog)

* * *

**Creators:** James King, Nina Kuklisova, Ashley Levato, Ankit Tharwani, Sean Underwood

**Course Instructors:** Coco Krumme, David Steier

* * *

Below is a quick summary of what is included in this repo

* **backend** - Shell and Hive scripts for preparing processed data to load into the middleware.
* **documentation**
  *  **air** - Markdown files for the air pollutant information pages.
  *  **header** - Html files for the site documentation and information pages.
  *  **water** - Markdown files for the water pollutant information pages.
* **exploration** - several iPython notebooks and and scripts that were used in data exploration, cleaning, processing, initial model building, etc
* **frontend** - source code for the web application
* **middleware** - REST API documentation and code
* **scripts** - Python scripts for data downloading, processing, model building, etc.
  * `annual_air_parse_api.py` is used to download and clean the air data.
  * `compile_markdown.py` converts the Markdown documents in the `documentation` folder to HTML for use in the website.
  * `model_predictor.py` generates warning level predictions using a pickled machine learning model.
  * `model_trainer.py` trains the warning level prediction model and saves it to a pickle file.
  * `water` contains scripts for downloading and processing the water data. To use it, run the following scripts in order:
    * `makeStructure.py` creates the directory structure that will be used by subsequent scripts.
    * `downloadWaterResult.py` downloads the water measurement data from 2010 - present.
    * `downloadWaterStation.py` downloads data about the water monitoring locations.
    * `processWaterFiles.py` processes the downloaded data and consolidates it all into a single output file.
    * The rest are modules and accessory files used by the above scripts.


