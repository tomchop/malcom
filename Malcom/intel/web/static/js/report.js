$(function() {

	$("#edit").click(function() {
		console.log("clicked!");
		edit_table();
	});

	$("#search-btn").click(function(){
		ajax_action($(this), search_entities, {query: $('#query').val()})
	});

	$("#associate-btn").click(function(){
		inputs = $("#associate").serializeArray();
		ids = []

		for (var i in inputs) {
			console.log(inputs[i]);
			ids.push(inputs[i].name);
		}

		ajax_action($(this), function(){}, $.param({ids: ids}, true));
	});

	$(".unlink").click(function(){
		ajax_action($(this), function(){}, {});
	})

	console.log("report.js loaded");
});

function ajax_action(elt, callback, params) {
	$.ajax({
		url: elt.data('url'),
		data: params,
		method: elt.data('ajax-method'),
	}).success(function(data) {
		callback(elt, data);
	});
}


function search_entities(elt, data) {
	tbl = $("<table id='search'></table>").addClass('table table-condensed');
	for (var i in data){
		e = data[i];
		tbl.append("<tr><th>"+e['title']+"</th><td>"+e['_type']+"</td><td><input type='checkbox' name='"+e['_id']['$oid']+"' /></td></tr>");
	}
	$("#search table").replaceWith(tbl);
}

function edit_table() {
	tbl = $("#main-table");
	tbl.wrap("<form id='update'></form>")

	$("td", tbl).each(function (index, value){
		text = $(value).text();
		field = $(value).data('field');

		input = '<input type="text" name="'+field+'" value="'+text+'" />';
		$(value).html(input);
	});

	edit = $("#edit")
	edit.text('[save]');
	edit.unbind('click');
	edit.click(function() {
		update_entity();
	});
}

function update_entity() {
	console.log("updating");
	console.log($("#update").serialize())

	$.ajax({
		url: $("#main-table").data('url'),
		data: $("#update").serializeArray(),
	}).success(function(data) {
		$("td", tbl).each(function (index, value){
			text = $('input', value).val();
			$(value).html(text);
		});
		tbl.unwrap();
		edit = $("#edit")
		edit.text('[edit]')
		edit.unbind('click');
		edit.click(function() {
			edit_table();
		});
	});
}