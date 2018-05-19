$(document).ready(function() {
  var url1 = "http://" + windowLocation + "/get_samples";
  var url2 = "http://" + windowLocation + "/sample_data";
  var url3 = "http://" + windowLocation + "/predict_sample?filename=";
  $.ajax({
    type: "GET",
    dataType: "json",
    url: url1,
    success: function(data) {
      // Load the gallery with images
      data.samples.map((sample, idx) => {
        $("#galleryContents").append(
          "<img class=sample name=" +
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
          $(".sample").removeClass("current");
          $(this).addClass("current");
          viewInputAndGetPredictions(
            url2 + "/" + e.target.name,
            url3 + e.target.name
          );
        });
      });
      // on first Load
      let firstSample = data.samples[0];
      $('[name="' + firstSample + '"]').addClass("current");
      viewInputAndGetPredictions(url2 + "/" + firstSample, url3 + firstSample);
    }
  });
});

// views the input image on the left + returns its position and height attributes
function viewInputAndGetPredictions(inputSrc, resultSrc) {
  const preview = $("#dropboxPreview");
  preview.attr("src", inputSrc);
  getPredictions(resultSrc);
}

function getPredictions(url) {
  // clear existing
  clearResult();
  // show spinner
  $("#loading2").addClass("is-active");
  // make call
  $.ajax({
    dataType: "json",
    type: "GET",
    url: url,
    success: function(data) {
      // remove spinner
      $("#loading2").removeClass("is-active");
      // display new result
      sortDataType(data);
    }
  });
}

// clears all results
function clearResult() {
  $("#resultImage").attr("src", "");
  $("#inputImage").attr("src", "");
}

// splits into images vs probabilities
function sortDataType(data) {
  if (data.type == "probabilities") {
    plotHistogram(data.result, 5);
  } else if (data.type == "image") {
    let filePath = data.result.substr(3);
    $("#resultImage").attr("src", appUrl + filePath);
    $("#inputImage").attr("src", appUrl + data.input);
  }
}
