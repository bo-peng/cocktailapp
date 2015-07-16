$("#view_drinks").click(function() {
    var selected_drinks = [];
    var checkedBoxes = $('input[name=ingredient]:checked')
	.each(function(i, selected){
	    selected_drinks[i] = '"' + $(selected).val() + '"';
	});
    get_drinks(selected_drinks);
});

function get_drinks(drinks_list){
    console.log(drinks_list);
    var data_to_send =  "{\"ingredients\": [" + drinks_list + "]}";
    console.log(data_to_send);
    $.ajax({
        type: "POST",
        contentType: "application/json; charset=utf-8",
        url: "/subset",
        dataType: "json",
        async: true,
        data: data_to_send,
        success: function (data) {
            console.log("success!");
	    var subset_drinks_list = data["drinks"]["result"];
	    var limes_drinks_list = data["extended_drinks"]["result"];
	    console.log(subset_drinks_list);
	    console.log(limes_drinks_list);
	    $(".panel-default").remove();
	    $("#search_results").show();
	   
	    document.getElementById('subset_drinks_container')
		.appendChild(make_drinks_accordion(subset_drinks_list, "subset_accordion"));
	    document.getElementById('limes_drinks_container')
		.appendChild(make_drinks_accordion(limes_drinks_list, "n_more_accordion"));

	    $(".drink_item").click(function() {
		console.log('here');
		console.log(this);
		that = this;
	    });
	   
        },
        error: function (result) {
        }
    })
}


function makeUL(array) {
    // http://stackoverflow.com/questions/11128700/
    // create-a-ul-and-fill-it-based-on-a-passed-array

    var list = document.createElement('ul');
    for(var i = 0; i < array.length; i++) {
        var item = document.createElement('li');
        item.appendChild(document.createTextNode(array[i]["name"]));
        list.appendChild(item);
    }
    return list;
}

function add_glass_img(glass_str, div_to_add_to) {

    // Cocktail glass by Marieva Cunha from the Noun Project
    // Highball glass by Adam James from the Noun Project
    // Double rocks glass by Gabriela Muñiz from the Noun Project
    // Tall glass by Anton Scherbik from the Noun Project
    // Rocks glass/tumbler by factor[e] design initiative from the Noun Project
    var img=document.createElement("img");
    img.src="static/img/" + glass_str + ".svg";
    img.height="20";
    img.style.marginRight = "20px";
    div_to_add_to.appendChild(img);

}

function make_drinks_accordion(array, accordion_id) {
   
    var accordion = document.getElementById(accordion_id);
    for(var i = 0; i < array.length; i++) {
	var drink_name_nice = array[i]["name"];
	var drink_name = drink_name_nice.replace(/\W+/g, "");
	var glass_str = array[i]["glass_type"].replace(/ /g, "_");

	var item = document.createElement("div");
	item.className = "panel panel-default";

	
	
	var bs_panelheading = document.createElement("div");
	bs_panelheading.className = "panel-heading";
	bs_panelheading.setAttribute("role", "tab");
	bs_panelheading.id = "heading" + drink_name;
	item.appendChild(bs_panelheading);
	if (array[i].hasOwnProperty("recognitions")) {
	    bs_panelheading.style.color = "red";
	}
	
	var bs_paneltitle = document.createElement("h4");
	bs_paneltitle.className = "panel-title";
	bs_panelheading.appendChild(bs_paneltitle);

	add_glass_img(glass_str, bs_paneltitle);	

	panel_button = document.createElement("a");
	panel_button.setAttribute("role","button");
	panel_button.setAttribute("data-toggle", "collapse");
	panel_button.setAttribute("data-parent", "#accordion");	



	$(panel_button).attr("aria-expanded","false");
	$(panel_button).attr("aria-controls","collapse" + drink_name);
	panel_button.href = "#collapse" + drink_name;
	panel_button.text = drink_name_nice;
	bs_paneltitle.appendChild(panel_button);

	var collapsed_section = document.createElement("div");
	collapsed_section.id = "collapse" + drink_name;
	collapsed_section.className = "panel-collapse collapse";
	collapsed_section.role = "tabpanel";
	collapsed_section.setAttribute("aria-labelledby", "heading" + drink_name);

	var collapsed_body = document.createElement("div");
	collapsed_body.className = "panel-body";
	collapsed_body.innerHTML = array[i]["instructions"];

	if (accordion_id == "n_more_accordion") {
	    add_missing_ingredient(array[i], collapsed_body);
	}
	
	collapsed_section.appendChild(collapsed_body);
	

	item.appendChild(collapsed_section);
	accordion.appendChild(item);    
    }
    return accordion;
}


function add_missing_ingredient(drink_obj, parent) {
    var missing = document.createElement("div");
    var text = drink_obj.ingredients[0].ingredient
    missing.innerHTML = "<i> missing " + text + "</i>";
    parent.appendChild(missing);
}

