/**
 * Appcelerator Drillbit
 * Copyright (c) 2012 by Appcelerator, Inc. All Rights Reserved.
 * Licensed under the terms of the Apache Public License
 * Please see the LICENSE included with this distribution for details.
 */
var ti = Ti = Titanium;
function BlackBerrySimulator(drillbit, blackberryNdk) {
	this.drillbit = drillbit;
	this.blackberryNdk = blackberryNdk;

	this.device = 'emulator';
	if ('blackberryDevice' in drillbit.argv) {
		this.device = drillbit.argv.blackberryDevice;
	}

	this.runtime = 'v8';

	ti.api.debug('Using javascript runtime: ' + this.runtime);

	this.blackberryBuilder = ti.path.join(drillbit.mobileSdk, 'blackberry', 'builder.py');
};

BlackBerrySimulator.prototype.createTestHarnessBuilderProcess = function(command, args) {
	var builderArgs =
	[
		this.blackberryBuilder,
		command,
		'-t', 'simulator', // FIXME: need the actual type
		'-d', this.drillbit.testHarnessDir,
		'-p', this.blackberryNdk
	];

	if (args) {
		builderArgs = builderArgs.concat(args);
	}
	return this.drillbit.createPythonProcess(builderArgs);
};

BlackBerrySimulator.prototype.getTestHarnessPID = function() {
	// TODO Mac
	ti.api.error("Not implemented: getTestHarnessPID");
	return null;
};

BlackBerrySimulator.prototype.isTestHarnessRunning = function() {
	// TODO Mac
	ti.api.error("Not implemented: isTestHarnessRunning");
	return true;
};

BlackBerrySimulator.prototype.isEmulatorRunning = function() {
	// TODO Mac
	ti.api.error("Not implemented: isEmulatorRunning");
	return true;
};

BlackBerrySimulator.prototype.getTestJSInclude = function() {
	// TODO Mac: check
	return "Ti.include(\"test.js\")";
};

BlackBerrySimulator.prototype.fillTiAppData = function(data) {
	if(data.androidRuntime === undefined) {
		data.androidRuntime = "none";
	}
};

BlackBerrySimulator.prototype.run = function(readLineCb) {
	var blackberrySimulatorProcess = null;

	var emulatorRunning = this.isEmulatorRunning();
	if (emulatorRunning || this.device.indexOf('emulator') != 0) {
		this.testHarnessRunning = this.isTestHarnessRunning();
	} else {
		// launch the (si|e)mulator async
		// TODO Mac
	}

	/*
	TODO Mac
	blackberrySimulatorProcess.setOnReadLine(readLineCb);
	blackberrySimulatorProcess.launch();
	*/

	if (this.device == 'emulator' && !emulatorRunning) {
		// TODO Mac
	} else {
		if (this.testHarnessRunning) {
			// Kill the test harness on bootup if it's still running
			this.killTestHarness()
		}
		this.drillbit.frontendDo('status', 'ready to run tests');
		this.drillbit.frontendDo('setup_finished');
	}
};

BlackBerrySimulator.prototype.removeTestJS = function(testScript) {
	// TODO Mac
	ti.api.error("Not implemented: removeTestJS");
};

BlackBerrySimulator.prototype.fillTestTemplateData = function(data) {
	// TODO Mac
	ti.api.error("Not implemented: fillTestTemplateData");
}

BlackBerrySimulator.prototype.pushTestJS = function(testScript) {
	var tempDir = ti.fs.createTempDirectory();
	var testJS = ti.fs.getFile(tempDir.nativePath(), "test.js");
	var stream = testJS.open(ti.fs.MODE_WRITE);
	stream.write(testScript);
	stream.close();

	// TODO Mac
};

BlackBerrySimulator.prototype.stageSDK = function(sdkTimestamp) {
	// TODO Mac
	ti.api.error("Not implemented: stageSDK");
	return null;
};

BlackBerrySimulator.prototype.testHarnessNeedsBuild = function(stagedFiles) {
	// TODO Mac
	ti.api.error("Not implemented: testHarnessNeedsBuild");
	return false;
};

BlackBerrySimulator.prototype.installTestHarness = function(launch, suite) {
	// TODO Mac: need to separate install from launch
	if (launch)
	{
		this.launchTestHarness(suite);
	}
};

BlackBerrySimulator.prototype.launchTestHarness = function(suite) {
	// TODO Mac: need to separate install from launch
	var command = 'run';
	var commandArgs = [];
	var process = this.createTestHarnessBuilderProcess(command, commandArgs);

	var self = this;
	process.setOnReadLine(function(data) {
		var lines = data.split("\n");
		lines.forEach(function(line) {
			self.drillbit.frontendDo('process_data', line);
		});
	});
	process.setOnExit(function(e) {
		if (process.getExitCode() != 0) {
			self.drillbit.handleTestError(suite, 'blackberry');
			return;
		}
		self.testHarnessRunning = true;
		self.needsBuild = false;
	});
	process.launch();
};

BlackBerrySimulator.prototype.killTestHarness = function() {
	// TODO Mac
	ti.api.error("Not implemented: killTestHarness");
	this.testHarnessRunning = false;
};

BlackBerrySimulator.prototype.runTestHarness = function(suite, stagedFiles) {
	var forceBuild = 'forceBuild' in suite.options && suite.options.forceBuild;
	
	// FIXME: for now just force it
	forceBuild = true;
	
	if (!this.testHarnessRunning || this.needsBuild || this.testHarnessNeedsBuild(stagedFiles) || forceBuild) {
		var command = 'build';
		var commandArgs = [];
		
		var process = this.createTestHarnessBuilderProcess(command, commandArgs);
		this.drillbit.frontendDo('building_test_harness', suite.name, 'blackberry');

		var self = this;
		process.setOnReadLine(function(data) {
			var lines = data.split("\n");
			lines.forEach(function(line) {
				self.drillbit.frontendDo('process_data', line);
			});
		});
		process.setOnExit(function(e) {
			if (process.getExitCode() != 0) {
				self.drillbit.handleTestError(suite, 'blackberry');
				return;
			}
			self.drillbit.frontendDo('running_test_harness', suite.name, 'blackberry');
			self.installTestHarness(true, suite);
			self.testHarnessRunning = true;
			self.needsBuild = false;
		});
		process.launch();
	} else {
		// restart the app
		this.drillbit.frontendDo('running_test_harness', suite.name, 'blackberry');

		// wait a few seconds after kill, every now and then the proc will still
		// be hanging up when we try to start it after kill returns
		var self = this;
		this.drillbit.window.setTimeout(function() {
			self.launchTestHarness(suite);
		}, 2000);
	}
};

Titanium.createBlackBerrySimulator = function(drillbit, blackberryNdk) {
	return new BlackBerrySimulator(drillbit, blackberryNdk);
}
