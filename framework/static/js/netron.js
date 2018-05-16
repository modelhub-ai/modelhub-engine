$(document).ready(function() {
  let bool = true;
  let split = window.location.href.split(":");
  let url = split[0] + ":" + split[1] + ":" + "4001/";
  $("#modeltab").on("click", function() {
    if (bool) {
      $("#model").append(
        '<iframe id="netron" height="100%" width=500 src="' +
          url +
          '"></iframe>'
      );
      bool = false;
    }
  });
});
