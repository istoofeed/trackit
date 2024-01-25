const localeEn = {
	days: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
	daysShort: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
	daysMin: ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"],
	months: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
	monthsShort: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
	today: "Today",
	clear: "Clear",
	dateFormat: "MM-dd-yyyy",
	timeFormat: "HH:MM AA",
	firstDay: 0,
};

document.addEventListener("htmx:load", function () {
	new AirDatepicker(".airdatepicker", {
		locale: localeEn,
		dateFormat: "MMMM dd, yyyy",
		altField: ".airdatepicker",
		altFieldDateFormat: "MMMM dd, yyyy hh:mm AA",
		timepicker: true,
		timeFormat: "hh:mm AA",
		buttons: ["clear"],
		autoClose: true,
		position: "top left",
		minDate: new Date(),
	});
});
