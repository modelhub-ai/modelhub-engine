$(document).ready(function() {
  $("#fileupload:file").change(function() {
    clearResult();
    activateAllSpinners();
    $(".sample").removeClass("current");
  });

  $("#dropbox").on("dragover", function() {
    $(this).addClass("dragging");
  });

  $("#dropbox").on("dragleave", function() {
    $(this).removeClass("dragging");
  });

  $("#dropbox").on("drop", function(event) {
    event.preventDefault();
    event.stopPropagation();
    clearResult();
    activateAllSpinners();
    $(".sample").removeClass("current");
  });

  $("#fileupload").fileupload({
    dropZone: $("#dropbox"),
    dataType: "json",
    type: "POST",
    url: "/predict",
    done: function(e, data) {
      createImage(data.files[0]);
      sortDataType(data.result);
    }
  });
});

function createImage(file) {
  var reader = new FileReader();
  reader.onload = function(e) {
    $("#loading1").removeClass("is-active");
    $("#dropboxPreview").attr("src", e.target.result);
  };
  reader.readAsDataURL(file);
}

function activateAllSpinners() {
  // clear input
  $("#dropboxPreview").attr("src", "");
  // activate spinners
  $("#loading1").addClass("is-active");
  $("#loading2").addClass("is-active");
}
