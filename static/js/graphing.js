// Explore options with graphing in D3
// Except we decided to go with plotly instead

// Set up some parameters temporarily
let svgWidth = 960;
let svgHeight = 500;

// Margins too
let margin = {
    top: 20,
    right: 20,
    bottom: 20,
    left: 20
}

// Make the chart have nice looks
let width = svgWidth - margin.left - margin.right;
let height = svgHeight - margin.top - margin.bottom;

// Get the stuff from html to do things
let svg = d3.select('.chart')
    .append('svg')
    .attr('width', svgWidth)
    .attr('height', svgHeight);

// Make a chart group because we're most likely going to be doing multiple datasets
let chartGroup = svg.append('g')
    .attr('transform', `translate(${margin.left}, ${margin.top})`);

// All the csvs get a variable because those filepaths are annoying to type
let directory = "static/data/";
let crime = directory + "crime_cleaned_data.csv";
let avgTemp = directory + "daily_avg_temps.csv";
let maxTemp = directory + "daily_max_temps.csv";
let minTemp = directory + "daily_min_temps.csv";
let avgHumidity = directory + "humidity_daily_avg.csv";
let maxHumidity = directory + "humidity_daily_max.csv";
let minHumidity = directory + "humidity_daily_min.csv";
let avgWind = directory + "wind_daily_avg.csv";
let maxWind = directory + "wind_daily_max.csv";
let minWind = directory + "wind_daily_min.csv";

// Do we get data from a csv file on heroku?
d3.csv(crime, function (error, crimeData) {
    if (error) throw error;
    console.log(crimeData);
})

// The answer was yes, but we opted to not go for D3 as our plot device.