$(document).ready(function() {
  $("#fileupload").fileupload({
    // dropZone: $("#dropbox"),
    dataType: "json",
    type: "POST",
    url: "/predict",
    done: function(e, data) {
      createImage(data.files[0]);
      plotHistogram(data.result.result, 5);
    }
  });
});

function createImage(file) {
  var reader = new FileReader();
  reader.onload = function(e) {
    $("#dropboxPreview").attr("src", e.target.result);
  };
  reader.readAsDataURL(file);
}
