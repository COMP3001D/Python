function result(data) {
	
	for(var i = 0; i < data.items.length; i++){
        	
        	var searchResult = document.createElement("div");
                var image = document.createElement("img");
                image.src = (data.items)[i].image.url;
                var link = document.createElement("a");
                link.href = (data.items)[i].url;
                link.innerHTML = (data.items)[i].displayName;
                searchResult.appendChild(link);
                searchResult.appendChild(image);
                document.body.appendChild(searchResult);
        }
}

function search() {
 	
 	var name = document.getElementById("names").value;
        var script = document.createElement( "script" );
        var url = "https://www.googleapis.com/plus/v1/people?key=AIzaSyDl1f0fZ8lJvH5PJPW6WG8x1b1lGvLBAiQ&query=" + name + "&callback=result";
        script.type = 'text/javascript';
        script.src = url;
               
        document.body.appendChild(script);
}                                                                                                                                                                                                      
