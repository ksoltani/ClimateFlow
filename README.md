A repo for the code "Climate Flow" made by Team Earthlings, for GovHack 2016.

The Australian Bureau of Meterology maintains almost 18,000 autonomous weather stations around the country, collecting Climate data such as rainfall totals, temperature extrema and windspeeds. Many of the stations have been operational since the last 100-odd years, so there is a wealth of information about how the climate changes over time in different parts of the country. The information, although technically available to the public, is isolated in separate websites for each station which makes it hard to interpret any useful trends to be found.

We have used Python programming language with BeautifulSoup, DataShader, Foilum and Leaflet.js libraries to create interactive maps for viewing the BoM data in a web browser. Users will be able to explore the trends in their area of interest, and look for areas with large changes in time.

This could be used for visualizing past data and predicting daily/monthly weather patterns based on past data for various applications:

    * Farming industry,
    * Energy (Solar, Wind) industry,
    * Climate Change Research/Higher Education Industry.
    * Innovative Visualization Hacks
    * and so on...

In the current version, the code is limited to visualizing max temperature data from 312 stations in Queensland, as downloading data from 18000 stations itself was taking more than 40 hrs (to download all the files). It is easily extendible to all Australian stations, and this work will be completed in the meanwhile, after the GovHack weekend.

