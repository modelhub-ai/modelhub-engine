$(document).ready(function() {
  $("#fileupload").fileupload({
    // dropZone: $("#dropbox"),
    dataType: "json",
    type: "POST",
    url: "/predict",
    done: function(e, data) {
      $(".sample").removeClass("current");
      createImage(data.files[0]);
      sortDataType(data.result);
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
