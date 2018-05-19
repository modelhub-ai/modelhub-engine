function plotHistogram(result, topX) {
  // sort in ascending order
  let sortedResult = _.sortBy(result, "probability");
  // Take the top x entries
  let topXResult = sortedResult.slice(-1 * topX);
  //var yAxisTitle = "top " + topX.toString() + " classes";
  let x = [];
  let y = [];
  for (let key in topXResult.slice(0, 5)) {
    x.push(parseFloat(topXResult[key].probability).toFixed(3));
    y.push(topXResult[key].label);
  }
  let data = [
    {
      type: "bar",
      x: x,
      y: y,
      orientation: "h",
      text: x,
      textposition: "outside",
      hoverinfo: "none",
      marker: {
        color: "rgb(0,150,136)"
      }
    }
  ];
  var layout = {
    title: "Result",
    margin: {
      l: 200,
      r: 90,
      pad: 10
    },
    xaxis: {
      autorange: "false",
      range: [0, 1],
      title: "Probabilities",
      fixedrange: true
    },
    yaxis: {
      fixedrange: true
      //title: yAxisTitle
    }
  };
  var options = {
    displayModeBar: false
  };
  Plotly.newPlot("result", data, layout, options);
  window.onresize = function() {
    Plotly.newPlot("result", data, layout, options);
  };
}
