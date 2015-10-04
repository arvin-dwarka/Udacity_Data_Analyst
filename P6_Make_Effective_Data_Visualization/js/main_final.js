d3.csv('data/data.csv', function(d) {
    var format = d3.time.format('%Y');
    return {
        'Year': format.parse(d.year),
        'Airport': d.airport,
        'On-Time': +d.timely
    };
    }, function(data) {
        'use strict';

    // append title
    d3.select('#content')
        .append('h1')
        .attr('id', 'title')
        .text('Percent distribution of flights arriving on time at the top ten US airports from 2003 to 2014');

    // set svg
    var width = 1080,
        height = 640;
    var svg = dimple.newSvg('#content', width, height);
    var myChart = new dimple.chart(svg, data);

    // set y axis
    var y = myChart.addMeasureAxis('y', 'On-Time');
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
    var myLegend = myChart.addLegend(width*0.165, 70, width*0.75, 70, 'right');

    // draw
    myChart.draw();

    // reusable mouseover event function on paths
    function mouse() {
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
    }

    // empty out legends
    myChart.legends = [];

    // add legends title to prompt user to click
    svg.selectAll('title_text')
            .data(['Click legend to show/hide airports:'])
            .enter()
            .append('text')
                .attr('x', width*0.758)
                .attr('y', function (d, i) { return 60 + i * 14; })
                .style('font-family', 'sans-serif')
                .style('font-size', '10px')
                .style('color', 'Black')
                .text(function (d) { return d; });

    // get a unique list of Airport values to use when filtering
    var filterValues = dimple.getUniqueValues(data, 'Airport');

    // get all the rectangles from now orphaned legend
    myLegend.shapes.selectAll('rect')
    .on('click', function (e) {
        var hide = false;
        var newFilters = [];
        // if the filters contain the clicked shape, hide it
        filterValues.forEach(function (f) {
            if (f === e.aggField.slice(-1)[0]) {
                hide = true;
                } else {
                    newFilters.push(f);
                }
            });
            // hide the shape or show it
            if (hide) {
                d3.select(this).style('opacity', 0.25);
            } else {
                newFilters.push(e.aggField.slice(-1)[0]);
                d3.select(this).style('opacity', 1);
            }
            // Update the filters
            filterValues = newFilters;
            // Filter the data
            myChart.data = dimple.filterData(data, 'Airport', filterValues);
            // draw modified chart with animation and mouseover events
            myChart.draw(800);
            mouse();
        });
// sfo, atl phx
    // make mouseover events available by default
    mouse();

    });
