/* Main JavaScript function to open the door and walking to the hall */

$(document).ready(function() {
	$doorOpened = false;
	
	/* Set click function to the door with the handle */
	$(".rightDoor").click(function() {
				
		/* Closing both doors by reducing their size to 40px both */
		if($doorOpened == false) {
			$(".leftDoor").stop().animate({
				width: '40px'
			}, 2000);
			$(".rightDoor").stop().animate({
				width: '40px'
			}, 2000);
			
			/* Play Creek sound while open the doors */
			$('body').append('<embed src="sounds/creek.wav" autostart="true" hidden="true" loop="false">');
			
			$doorOpened == true;
			
			/* Walk in to the room after the 3 seconds delay after the doors 
			 * will be fully open
			 */			
			setTimeout(walkIn, 3000);
			
		}
	});
});


/* Helper function to open walk in to the hall */
function walkIn() {
	
	// Walk in animation
	$(".doorFrame img").animate({
		left: '-=25%',
		top: '-=30px',
		height: '105%',
		opacity: 0.0,
		width: '+=50%'
	}, 3000);
	
	$(".leftDoor").animate({
		left: '-=22%',
		top: '-=3.2%',
		height: '100%',
		opacity: 0.0
	}, 3000);
	
	$(".rightDoor").animate({
		right: '-=22%',
		top: '-=3.2%',
		height: '100%',
		opacity: 0.0
	}, 3000);
	
	/* Start the foot step sound */
	$('body').append('<embed src="sounds/steps.wav" autostart="true" hidden="true" loop="false">');
}








