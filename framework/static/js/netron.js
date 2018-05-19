$(document).ready(function() {
  let bool = true;
  $("#modeltab").on("click", function() {
    if (bool) {
      $("#model").append(
        '<iframe id="netron" height="100%" width=500 src="' +
          netronUrl +
          '"></iframe>'
      );
      bool = false;
    }
  });
});
