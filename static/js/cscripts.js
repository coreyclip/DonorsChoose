let url = "/Portland/05/humidity"
d3.json(url, function(json) {
    
    // First Graph
    /*
    let trace1 = {
        x: json[0][0]['x'],
        y: json[0][0]['y'],
        name: json[0][0]['name'],
        type: json[0][0]['type'],
        mode: json[0][0]['mode'],
        marker: json[0][0]['line']
    };
    let trace2 = {
        x: json[0][1]['x'],
        y: json[0][1]['y'],
        name: json[0][1]['name'],
        type: json[0][1]['type'],
        mode: json[0][1]['mode'],
        marker: json[0][1]['line']
    };
    let trace3 = {
        x: json[0][2]['x'],
        y: json[0][2]['y'],
        name: json[0][2]['name'],
        type: json[0][2]['type'],
        mode: json[0][2]['mode'],
        marker: json[0][2]['line']
    };
    let data = [trace1, trace2, trace3];
    */
    let layout = {
        title: "Temperature vs Date", 
        xaxis: {
            title: "Dates",
        },
        yaxis: {
            title: "Temperature, Degrees Fahrenheit"
        }

    };
    Plotly.newPlot('first_graph', json[0], layout);

    // Second Graph 

    // Debug: console.log(json[1][0]['type'])
    /*
    let trace = {
        x: json[1][0]['x'],
        y: json[1][0]['y'],
        name: json[1][0]['name'],
        mode: json[1][0]['mode'],
        type: json[1][0]['type'],
        text: json[1][0]['text'],
        marker: json[1][0]['marker']
    };
    let data2 = [trace];
    */
    let layout2 = {
        title: "Temperature vs Number of Airport Delays",
        xaxis: {
            title: "Temperature"
        },
        yaxis: {
            title: "Number of Airport Delays"
        },
    };

    Plotly.newPlot('second_graph', json[1], layout2);

    // Third Plot
    // Debug: console.log(json[2][0]['values'])
    /*
    let pie_trace = {
        values:json[2][0]['values'],
        labels:json[2][0]['labels'],
        type: json[2][0]['type'],
        hole: json[2][0]['hole'],
        marker: json[2][0]['marker'],
        textinfo: json[2][0]['textinfo'],
        name: json[2][0]['name']
    };
    let pie_data = [pie_trace]
    */
    let pie_layout = {
        title: "Frequency of Weather Conditions in Portland",
        height: 700,
        width: 800
    };
    Plotly.newPlot("third_graph", json[2], pie_layout)
});