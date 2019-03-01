
	$('#calculate').click(function(e){

		var batteryCapacity = 12; // kWh
		var batteryPrice = 323457; // USD
		var sunPerDay = 4; // h
		var panelGeneration = 0.15 // kWh
		var generatePrice = 0.3 // USD/W

		var bdInKw = 10; // get from location
		var electricityPrice = 0.12 // USD/kWh

		var fans = $('#householdBDs').val();
		var ac = $('#householdBDs1').val();
		var cfl = $('#householdBDs2').val();
		var pc = $('#householdBDs3').val();


		var consumefan = (fans) * bdInKw * 0.15;
		var consumeac = (ac) * bdInKw * 0.85;
		var consumecfl = (cfl) * bdInKw * 0.20;
		var consumepc = (pc) * bdInKw * 0.45;

		var consumetot = consumefan + consumepc + consumecfl + consumeac;

		var batteries = Math.floor(consumetot / (batteryCapacity));

		$('#batteryPacks').val(batteries);
		val = batteries;

		var generateCapacity = consumetot / sunPerDay;

		var panelSize = generateCapacity / panelGeneration
		$('#panelSize').val(panelSize);

		var investment = batteries * batteryPrice + generateCapacity  * generatePrice;

		$('#investment').val(investment);

		var returnOfInvestment = Math.floor(investment / electricityPrice / 24 / 365);
		returnOfInvestment = Math.round(returnOfInvestment / 77);

		$('#returnOfInvestment').val(returnOfInvestment + ' year(s)');
	});