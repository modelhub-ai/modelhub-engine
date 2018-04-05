// https://github.com/Bouni/HTML5-jQuery-Flask-file-upload
$(function() {
  var dropbox = $("#dropbox");
  dropbox.filedrop({
    paramname: "file",
    maxfiles: 1,
    maxfilesize: 5,
    url: "/predict",
    uploadFinished: function(i, file, response) {
      // switch here if an image is to be returned.
      plotHistogram(response.result, 5);
    },
    error: function(err, file) {
      switch (err) {
        case "BrowserNotSupported":
          alert("Your browser does not support HTML5 file uploads!");
          break;
        case "TooManyFiles":
          alert("Too many files! Please select " + this.maxfiles + " at most!");
          break;
        case "FileTooLarge":
          alert(
            file.name +
              " is too large! The size is limited to " +
              this.maxfilesize +
              "MB."
          );
          break;
        default:
          break;
      }
    },
    beforeEach: function(file) {
      if (!file.type.match(/^image\//)) {
        alert("Only images are allowed!");
        return false;
      }
    },
    uploadStarted: function(i, file, len) {
      $("#dropboxText").empty();
      $("#dropboxText").text("loading...");
      createImage(file);
    }
  });
  function createImage(file) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $("#dropboxText").empty();
      $("#dropboxPreview").attr("src", e.target.result);
    };
    reader.readAsDataURL(file);
  }
});
