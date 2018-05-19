(function() {
  "use strict";
  // tried multiple times to make this cleaner.. didnt work
  var button0 = document.querySelector("#dialogButtonLic0");
  var dialog0 = document.querySelector("#dialog0");
  var button1 = document.querySelector("#dialogButtonLic1");
  var dialog1 = document.querySelector("#dialog1");
  var button2 = document.querySelector("#dialogButtonLic2");
  var dialog2 = document.querySelector("#dialog2");
  var button3 = document.querySelector("#dialogButtonLic3");
  var dialog3 = document.querySelector("#dialog3");
  addDialog(dialog0, button0);
  addDialog(dialog1, button1);
  addDialog(dialog2, button2);
  addDialog(dialog3, button3);
  // adds text
  getIndex(appUrl + "get_license");
})();

// Adds the dialog to the given DOM elements
function addDialog(dialog, dialogButton) {
  if (!dialog.showModal) {
    dialogPolyfill.registerDialog(dialog);
  }
  dialogButton.addEventListener("click", function() {
    dialog.showModal();
  });
  dialog
    // .querySelector("button:not([disabled])")
    .addEventListener("click", function() {
      dialog.close();
    });
}

// grabs the license + acknowledgement info and dumps it into the DOM
function getIndex(url) {
  $.ajax({
    dataType: "json",
    type: "GET",
    url: url,
    success: function(data) {
      dumpText("#dialog0", data.license);
      dumpText("#dialog1", data.acknowledgements);
      dumpText("#dialog2", data.model_lic);
      dumpText("#dialog3", data.sample_data_lic);
    }
  });
}

// cleans up clutter
function dumpText(id, text) {
  $(id)
    .find("p")
    .html(replaceBreaks(text));
}

// replaces all line breaks with <br>
function replaceBreaks(str) {
  return str.replace(/(?:\r\n|\r|\n)/g, "<br>");
}
