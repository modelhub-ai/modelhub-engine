function plotHistogram(result, topX) {
  // sort in ascending order
  let sortedResult = _.sortBy(result, "probability");
  // Take the top x entries
  let topXResult = sortedResult.slice(-1 * topX);
  let x = [];
  let y = [];
  for (let key in topXResult.slice(0, 5)) {
    x.push(topXResult[key].probability);
    y.push(topXResult[key].label);
  }
  let data = [
    {
      type: "bar",
      x: x,
      y: y,
      orientation: "h"
    }
  ];

  let layout = [
    (margin: {
      left: 40
    })
  ];
  Plotly.newPlot("result", data);
  window.onresize = function() {
    Plotly.newPlot("result", data);
  };
}
