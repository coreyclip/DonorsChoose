
// Set up our chart
var svgWidth = 1000;
var svgHeight = 700;
var margin = { top: 30, right: 40, bottom: 100, left: 100 };

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;


// Create an SVG wrapper, append an svg that will hold our chart and shift the latter by left and top margins

var svg = d3.select(".chart")
    .append("svg")
    .attr("height", svgHeight)
    .attr("width", svgWidth)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// append an svg group
var chart = svg.append("g");

d3.select(".chart").append("div").attr("class", "tooltip").style("opacity", 0);

url = "/data";
d3.json(url, function (err, data) {
    if (err) throw err;

    // copy data into global dataset
    dataset = data

    // Initialize tooltip
    var toolTip = d3.tip()
        .attr("class", "tooltip")
        // Define position
        .offset([80, -60])
        // The html() method allows us to mix JavaScript with HTML in the callback function
        .html(function (data) {
            var state = data.geography;
            return state;
        });

    // Create tooltip
    chart.call(toolTip);

    // define scale functions(range)
    var xScale = d3.scaleLinear().range([0, width]);
    var yScale = d3.scaleLinear().range([height, 0]);

    // define axis functions
    var xAxis = d3.axisBottom().scale(xScale);
    var yAxis = d3.axisLeft().scale(yScale);

    // these variables store the min and max values in a column in data.csv
    var xMin;
    var xMax;
    var yMin;
    var yMax;

    // create a function to identify min, max values of a column in data.csv which in turn
    // assigns the results to the variables created above

    function findMinAndMaxX(dataColumnX) {
        xMin = d3.min(dataset, function (d) { return d[dataColumnX] * 0.8 });
        xMax = d3.max(dataset, function (d) { return d[dataColumnX] * 1.2 });
    };

    function findMinAndMaxY(dataColumnY) {
        yMin = d3.min(dataset, function (d) { return d[dataColumnY] * 0.8 });
        yMax = d3.max(dataset, function (d) { return d[dataColumnY] * 1.2 });
    };

    // set the default x-axis
    var defaultAxisLabelX = "percentBelowPoverty"

    // set the default y-axis
    var defaultAxisLabelY = "smokers"

    // call the findMinAndMax() on the default X Axis
    findMinAndMaxX(defaultAxisLabelX)
    findMinAndMaxY(defaultAxisLabelY)

    // set the domain of the axes
    xScale.domain([xMin, xMax]);
    yScale.domain([yMin, yMax])

    // create chart
    chart.selectAll("circle")
        .data(dataset)
        .enter()
        .append("circle")
        .attr("cx", function (d) {
            return xScale(d[defaultAxisLabelX]);
        })
        .attr("cy", function (d) {
            return yScale(d[defaultAxisLabelY]);
        })
        .attr("r", 15)
        .attr("fill", "#4380BA")
        .attr("opacity", 0.75)
        // display tooltip on click
        .on("mouseover", function (d) {
            toolTip.show(d);
        })
        // hide tooltip on mouseout
        .on("mouseout", function (d, i) {
            toolTip.hide(d);
        })

    // create state labels
    chart.selectAll("text")
        .data(dataset)
        .enter()
        .append("text")
        .text(function (d) {
            return d.locationAbbr;
        })
        .attr("x", function (d) {
            return xScale(d[defaultAxisLabelX]);
        })
        .attr("y", function (d) {
            return yScale(d[defaultAxisLabelY]);
        })
        .attr("font-size", "12px")
        .attr("text-anchor", "middle")
        .attr("class","stateText")

        // display tooltip on click
        .on("mouseover", function (d) {
            toolTip.show(d);
        })
        // hide tooltip on mouseout
        .on("mouseout", function (d, i) {
            toolTip.hide(d);
        })


    // create x-axis
    chart.append("g")
        .attr("class", "x-axis")
        .attr("transform", `translate(0,${height})`)
        .call(xAxis);

    // create y-axis
    chart.append("g")
        .attr("class", "y-axis")
        .call(yAxis)


    // Append axes titles

    // add main x-axis title
    chart.append("text")
        .attr("transform", `translate(${width - 40},${height - 5})`)
        .attr("class", "axis-text-main")
        .text("Demographics")

    chart.append("text")
        .attr("transform", `translate(15,60 )rotate(270)`)
        .attr("class", "axis-text-main")
        .text("Behavioral Risk Factors")

    // add x-axis titles
    chart.append("text")
        .attr("transform", `translate(${width / 2},${height + 40})`)
        // This axis label is active by default
        .attr("class", "axis-text-x active")
        .attr("data-axis-name", "percentBelowPoverty")
        .text("In Poverty (%)");

    chart.append("text")
        .attr("transform", `translate(${width / 2},${height + 60})`)
        // This axis label is active by default
        .attr("class", "axis-text-x inactive")
        .attr("data-axis-name", "medianIncome")
        .text("Household Income (Median)");

    chart.append("text")
        .attr("transform", `translate(${width / 2},${height + 80})`)
        // This axis label is active by default
        .attr("class", "axis-text-x inactive")
        .attr("data-axis-name", "ageDependencyRatio")
        .text("Age Dependency Ratio");


    // add y-axis titles 
    chart.append("text")
        .attr("transform", `translate(-40,${height / 2})rotate(270)`)
        .attr("class", "axis-text-y active")
        .attr("data-axis-name", "smokers")
        .text("Smokes (%)");


    chart.append("text")
        .attr("transform", `translate(-60,${height / 2})rotate(270)`)
        .attr("class", "axis-text-y inactive")
        .attr("data-axis-name", "alcoholConsumption")
        .text("Alcohol Consumption (%)");


    chart.append("text")
        .attr("transform", `translate(-80,${height / 2})rotate(270)`)
        .attr("class", "axis-text-y inactive")
        .attr("data-axis-name", "physicallyActive")
        .text("Physically Active (%)");

    // change the x axis's status from inactive to active when clicked and change all active to inactive
    function labelChangeX(clickedAxis) {
        d3.selectAll(".axis-text-x")
            .filter(".active")
            .classed("active", false)
            .classed("inactive", true);

        clickedAxis.classed("inactive", false).classed("active", true);
    }

    // change the y axis's status from inactive to active when clicked and change all active to inactive
    function labelChangeY(clickedAxis) {
        d3.selectAll(".axis-text-y")
            .filter(".active")
            .classed("active", false)
            .classed("inactive", true);

        clickedAxis.classed("inactive", false).classed("active", true);
    }

    // on click events for the x-axis
    d3.selectAll(".axis-text-x").on("click", function () {

        // assign the variable to the current axis
        var clickedSelection = d3.select(this);
        var isClickedSelectionInactive = clickedSelection.classed("inactive");
        console.log("this axis is inactive", isClickedSelectionInactive)
        var clickedAxis = clickedSelection.attr("data-axis-name");
        console.log("current axis: ", clickedAxis);

        if (isClickedSelectionInactive) {
            currentAxisLabelX = clickedAxis;

            findMinAndMaxX(currentAxisLabelX);

            xScale.domain([xMin, xMax]);

            // create x-axis
            svg.select(".x-axis")
                .transition()
                .duration(1000)
                .ease(d3.easeLinear)
                .call(xAxis);

            d3.selectAll("circle")
                .transition()
                .duration(1000)
                .ease(d3.easeLinear)
                .on("start", function () {
                    d3.select(this)
                        .attr("opacity", 0.50)
                        .attr("r", 20)

                })
                .attr("cx", function (d) {
                    return xScale(d[currentAxisLabelX]);
                })
                .on("end", function () {
                    d3.select(this)
                        .transition()
                        .duration(500)
                        .attr("r", 15)
                        .attr("fill", "#4380BA")
                        .attr("opacity", 0.75);
                })

            d3.selectAll(".stateText")
                    .transition()
                    .duration(1000)
                    .ease(d3.easeLinear)
                    .attr("x", function (d) {
                        return xScale(d[currentAxisLabelX]);
                    })
                    
            

            labelChangeX(clickedSelection);
        }
    });

    // On click events for the y-axis
    d3.selectAll(".axis-text-y").on("click", function () {

        // assign the variable to the current axis
        var clickedSelection = d3.select(this);
        var isClickedSelectionInactive = clickedSelection.classed("inactive");
        console.log("this axis is inactive", isClickedSelectionInactive)
        var clickedAxis = clickedSelection.attr("data-axis-name");
        console.log("current axis: ", clickedAxis);

        if (isClickedSelectionInactive) {
            currentAxisLabelY = clickedAxis;

            findMinAndMaxY(currentAxisLabelY);

            yScale.domain([yMin, yMax]);

            // create y-axis
            svg.select(".y-axis")
                .transition()
                .duration(1000)
                .ease(d3.easeLinear)
                .call(yAxis);

            d3.selectAll("circle")
                .transition()
                .duration(1000)
                .ease(d3.easeLinear)
                .on("start", function () {
                    d3.select(this)
                        .attr("opacity", 0.50)
                        .attr("r", 20)

                })
                .attr("cy", function (data) {
                    return yScale(data[currentAxisLabelY]);
                })
                .on("end", function () {
                    d3.select(this)
                        .transition()
                        .duration(500)
                        .attr("r", 15)
                        .attr("fill", "#4380BA")
                        .attr("opacity", 0.75);
                })

            d3.selectAll(".stateText")
                .transition()
                .duration(1000)
                .ease(d3.easeLinear)
                .attr("y", function (d) {
                    return yScale(d[currentAxisLabelY]);
                })

            labelChangeY(clickedSelection);

        }

    });

});


