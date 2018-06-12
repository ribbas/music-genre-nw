var dataURL = "https://raw.githubusercontent.com/sabbirahm3d/heavy-metals/master/data/plot_data.json";

function arrayFlip(trans) {

  var key;
  var tmp = {};

  for (key in trans) {
    if (trans.hasOwnProperty(key)) {
      tmp[trans[key].split("<br>")[0]] = key;
    }
  }

  return tmp;

}

function getConnections(connections, data) {

  var childrenPoints = [];

  for (var i = 0; i < connections.length; i++) {
    childrenPoints.push(data[connections[i]]);
  }

  return childrenPoints;
}

$.getJSON(dataURL, function(data) {

  Plotly.newPlot("plotDiv", data);

  var plot = document.getElementById("plotDiv");

  plot.on("plotly_hover", function(eventdata) {

    var points = eventdata.points[0];
    var pointNum = points.pointNumber;
    var curveNum = points.curveNumber;
    var connections = points.data.connections[pointNum];
    var allData = arrayFlip(eventdata.points[0].data.text);
    var childrenPoints = getConnections(connections, allData);

    var curves = [{ curveNumber: curveNum, pointNumber: pointNum }];

    for (var point = 0; point < childrenPoints.length; point++) {
      curves.push({
        curveNumber: curveNum,
        pointNumber: childrenPoints[point]
      });
    }

    Plotly.Fx.hover("plotDiv", curves);

    window.onresize = function() {
        Plotly.Plots.resize(plot);
    };

  });

});
