$(document).ready(function() {
  var url1 = "http://" + window.location.host + "/get_samples";
  var url2 = "http://" + window.location.host + "/sample_data";
  var url3 = "http://" + window.location.host + "/predict_sample?filename=";
  $.ajax({
    type: "GET",
    dataType: "json",
    url: url1,
    success: function(data) {
      // Load the gallery with images
      data.samples.map((sample, idx) => {
        $("#galleryContents").append(
          "<img id=sample name=" +
            sample +
            " src='" +
            url2 +
            "/" +
            sample +
            "'>"
        );
      });
      // on gallery image click
      data.samples.map((sample, idx) => {
        $('[name="' + sample + '"]').click(function(e) {
          // e.target.name
          $("#dropboxPreview").attr("src", url2 + "/" + e.target.name);
          getPredictions(url3 + e.target.name);
        });
      });
      // on first Load
      $("#dropboxPreview").attr("src", url2 + "/" + data.samples[0]);
      getPredictions(url3 + data.samples[0]);
    }
  });
});

function getPredictions(url) {
  $.ajax({
    dataType: "json",
    type: "GET",
    url: url,
    success: function(data) {
      plotHistogram(data.result, 5);
    }
  });
}
