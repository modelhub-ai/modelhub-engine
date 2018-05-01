$(document).ready(function() {
  let bool = true;
  $("#modeltab").on("click", function() {
    console.log("clicked");
    if (bool) {
      $("#model").html(
        '<iframe id="netron" height="100%" width=500 src="http://127.0.0.1:4001/"></iframe>'
      );
      bool = false;
    }
  });
});
