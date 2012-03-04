function fmtDec(amt, places) {
	amt = String(Math.round(amt * Math.pow(10, places)));
	frontlen = amt.length - places;
	return amt.substr(0, frontlen) + '.' + amt.substr(frontlen);
}

