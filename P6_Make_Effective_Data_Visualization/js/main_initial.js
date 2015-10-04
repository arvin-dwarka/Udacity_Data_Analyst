d3.csv("data/data.csv", function(d) {
    var format = d3.time.format("%Y");
    return {
        'Year': format.parse(d.year),
        'Airport': d.airport,
        'On Time': +d.timely
    };
    }, function(data) {
        'use strict';

    // append title
    d3.select('#content')
        .append('h2')
        .attr('id', 'title')
        .text('Percent distribution of flights arriving on time at the top ten US airports from 2003 to 2015');

    // set svg
    var width = 1080,
        height = 640;
    var svg = dimple.newSvg('#content', width, height);
    var myChart = new dimple.chart(svg, data);

    // set y axis
    var y = myChart.addMeasureAxis('y', 'On Time');
    y.tickFormat = '%';
    y.overrideMin = 0.65;
    y.overrideMax = 0.9;
    y.title = 'Percentage of on-time arrivals';

    // set x axis
    var x = myChart.addTimeAxis('x', 'Year');
    x.tickFormat = '%Y';
    x.title = 'Year';

    // set series and legend
    var scatter = myChart.addSeries('Airport', dimple.plot.scatter);
    var line = myChart.addSeries('Airport', dimple.plot.line);
    var legend = myChart.addLegend(width*0.165, 70, width*0.75, 70, 'right');

    // draw
    myChart.draw();

    // handle mouse events on paths
    d3.selectAll('path')
        .style('opacity', 0.25)
        .on('mouseover', function(e) {
            d3.select(this)
                .style('stroke-width', '3px')
                .style('opacity', 1)
        }).on('mouseleave', function(e) {
            d3.select(this)
                .style('stroke-width', '1px')
                .style('opacity', 0.25);       
    });
    });
