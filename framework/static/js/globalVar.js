let windowLocation = window.location.host;
let split = window.location.href.split(":");
if (split[1].slice(-1) == "/") {
    split[1] = split[1].slice(0, -1)
}
let appUrl = split[0] + ":" + split[1] + ":" + "80/";
let netronUrl = split[0] + ":" + split[1] + ":" + "81/";
console.log(split)
console.log(netronUrl)
