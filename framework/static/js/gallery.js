$(document).ready(function() {
  var url1 = "http://" + window.location.host + "/get_samples";
  var url2 = "http://" + window.location.host + "/sample_data";
  var url3 = "http://" + window.location.host + "/predict_sample?filename=";
  $.ajax({
    type: "GET",
    dataType: "json",
    url: url1,
    success: function(data) {
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
      data.samples.map((sample, idx) => {
        $('[name="' + sample + '"]').click(function(e) {
          // e.target.name
          $("#dropboxPreview").attr("src", url2 + "/" + e.target.name);
          $.ajax({
            dataType: "json",
            type: "GET",
            url: url3 + e.target.name,
            success: function(data) {
              plotHistogram(data.result, 5);
            }
          });
        });
      });
    }
  });
});
