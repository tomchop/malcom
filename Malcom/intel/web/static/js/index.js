$(function() {
	console.log('startup')

	$('#all-tab').on('shown.bs.tab', function (e) {
	  console.log('Show all')
	  ajax_action($(this), populate);
	});

	$('#campaigns-tab').on('shown.bs.tab', function (e) {
	  console.log('Show campaigns')
	  ajax_action($(this), populate);
	});

	$('#malware-tab').on('shown.bs.tab', function (e) {
	  console.log('Show malware')
	  ajax_action($(this), populate);
	});

	$('#indicators-tab').on('shown.bs.tab', function (e) {
	  console.log('Show indicators')
	  ajax_action($(this), populate);
	});

	$('#incidents-tab').on('shown.bs.tab', function (e) {
	  console.log('Show incidents')
	  ajax_action($(this), populate);
	});

	$('#ttps-tab').on('shown.bs.tab', function (e) {
	  console.log('Show ttps')
	  ajax_action($(this), populate);
	});
});

function ajax_action(elt, callback) {
	console.log("Data URL: "+ elt.data('url'))
	$.ajax({
		url: elt.data('url'),
	}).success(function(data) {
		callback(elt, data);
	});
}

function populate(elt, data) {
	target = $("#"+elt.data('container'));
	console.log(target)
	target.html(data);
}