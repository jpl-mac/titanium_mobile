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
	// TODO
	ti.api.error("Not implemented: getTestHarnessPID");
	return null;
};

BlackBerrySimulator.prototype.isTestHarnessRunning = function() {
	// TODO
	ti.api.error("Not implemented: isTestHarnessRunning");
	return true;
};

BlackBerrySimulator.prototype.isEmulatorRunning = function() {
	// TODO
	ti.api.error("Not implemented: isEmulatorRunning");
	return true;
};

BlackBerrySimulator.prototype.getTestJSInclude = function() {
	// TODO: check
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
		// TODO
	}

	/*
	TODO
	blackberrySimulatorProcess.setOnReadLine(readLineCb);
	blackberrySimulatorProcess.launch();
	*/

	if (this.device == 'emulator' && !emulatorRunning) {
		// TODO
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
	// TODO
	ti.api.error("Not implemented: removeTestJS");
};

BlackBerrySimulator.prototype.fillTestTemplateData = function(data) {
	// TODO
	ti.api.error("Not implemented: fillTestTemplateData");
}

BlackBerrySimulator.prototype.pushTestJS = function(testScript) {
	var tempDir = ti.fs.createTempDirectory();
	var testJS = ti.fs.getFile(tempDir.nativePath(), "test.js");
	var stream = testJS.open(ti.fs.MODE_WRITE);
	stream.write(testScript);
	stream.close();

	// TODO
};

BlackBerrySimulator.prototype.stageSDK = function(sdkTimestamp) {
	// TODO
	ti.api.error("Not implemented: fillTestTemplateData");
	return null;
};

BlackBerrySimulator.prototype.testHarnessNeedsBuild = function(stagedFiles) {
	// TODO
	ti.api.error("Not implemented: testHarnessNeedsBuild");
	return false;
};

BlackBerrySimulator.prototype.installTestHarness = function(launch) {
	// TODO
	ti.api.error("Not implemented: installTestHarness");
};

BlackBerrySimulator.prototype.launchTestHarness = function() {
	// TODO
	ti.api.error("Not implemented: launchTestHarness");
};

BlackBerrySimulator.prototype.killTestHarness = function() {
	// TODO
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
		var needsInstall = true;
		var needsLaunch = false;

		if (this.device.indexOf('emulator') != 0) {
			command = 'install';
			commandArgs = [this.avdId, this.device];
			needsLaunch = true;
			needsInstall = false;
		}
		
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
				self.drillbit.handleTestError(suite);
				return;
			}
			if (needsInstall) {
				self.installTestHarness(true);
			} else if (needsLaunch) {
				self.launchTestHarness();
			}
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
			self.launchTestHarness();
		}, 2000);
	}
};

Titanium.createBlackBerrySimulator = function(drillbit, blackberryNdk) {
	return new BlackBerrySimulator(drillbit, blackberryNdk);
}
