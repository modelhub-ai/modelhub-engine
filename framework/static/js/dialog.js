(function() {
  "use strict";
  var button1 = document.querySelector(".dialog-button-lic1");
  var dialog1 = document.querySelector("#dialog-1");
  var button2 = document.querySelector(".dialog-button-lic2");
  var dialog2 = document.querySelector("#dialog-2");
  addDialog(dialog1, button1);
  addDialog(dialog2, button2);
})();

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
