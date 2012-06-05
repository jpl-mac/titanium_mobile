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
	this.blackberryDeviceManagement = ti.path.join(drillbit.mobileSdk, 'blackberry', 'devicemanagement.py');
};

BlackBerrySimulator.prototype.createDeviceManagementProcess = function(command, args) {
	var procArgs =
	[
		this.blackberryDeviceManagement,
		'-t', 'simulator', // FIXME: need the actual type
		'-d', this.drillbit.testHarnessDir,
		'-p', this.blackberryNdk,
		command,
	];

	if (args) {
		procArgs = procArgs.concat(args);
	}
	return this.drillbit.createPythonProcess(procArgs);
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

BlackBerrySimulator.prototype.isTestHarnessRunning = function() {
	var retVal = false;
	var command = 'isAppRunning';
	var process = this.createDeviceManagementProcess(command);

	var self = this;
	process.setOnReadLine(function(data) {
		var lines = data.split("\n");
		lines.forEach(function(line) {
			if (line.indexOf("result::") === 0) {
				var trueString = "true";
				retVal = line.indexOf(trueString, line.length - trueString.length) !== -1;
			}
		});
	});
	process();
	return retVal;
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
	var emulatorRunning = this.isEmulatorRunning();
	if (emulatorRunning || this.device.indexOf('emulator') != 0) {
		this.testHarnessRunning = this.isTestHarnessRunning();
	} else {
		// launch the (si|e)mulator async
		// TODO Mac
	}

	this.readLineCb = readLineCb;

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

BlackBerrySimulator.prototype.handleCompleteBlackBerryEvent = function(event)
{
	// TODO Mac
	ti.api.error("Not implemented: handleCompleteBlackBerryEvent");
};

BlackBerrySimulator.prototype.removeTestJS = function(testScript) {
	// TODO Mac
	ti.api.error("Not implemented: removeTestJS");
};

BlackBerrySimulator.prototype.fillTestTemplateData = function(data) {
	// nothing to do
}

BlackBerrySimulator.prototype.pushTestJS = function(testScript) {
	var testJSFile = ti.fs.createTempFile();
	testJSFile.write(testScript);
	var command = 'putFile';
	// TODO Mac: check
	var deviceFile = 'app/native/assets/test.js';
	var commandArgs = [testJSFile.nativePath(), deviceFile];
	var process = this.createDeviceManagementProcess(command, commandArgs);

	var self = this;
	process.setOnReadLine(function(data) {
		var lines = data.split("\n");
		lines.forEach(function(line) {
			self.drillbit.frontendDo('process_data', line);
		});
	});
	process.setOnExit(function(e) {
		if (process.getExitCode() !== 0) {
			ti.api.error("[BlackBerry] pushTestJS failed");
		}
	});
	process();
};

BlackBerrySimulator.prototype.stageSDK = function(sdkTimestamp) {
	return [];
};

BlackBerrySimulator.prototype.installTestHarness = function(launch, suite) {
	// TODO Mac: need to separate install from launch
	if (launch) {
		this.launchTestHarness(suite);
	}
};

BlackBerrySimulator.prototype.launchTestHarness = function(suite) {
	// TODO Mac: need to separate install from launch
	var command = 'run';
	var process = this.createTestHarnessBuilderProcess(command);

	var self = this;
	process.setOnReadLine(function(data) {
		var lines = data.split("\n");
		lines.forEach(function(line) {
			self.drillbit.frontendDo('process_data', line);
		});
	});
	process.setOnExit(function(e) {
		if (process.getExitCode() !== 0) {
			self.drillbit.handleTestError(suite, 'blackberry');
			return;
		}
		self.testHarnessRunning = true;
		self.needsBuild = false;
		var logProcess = self.createDeviceManagementProcess('appLog');
		logProcess.setOnReadLine(self.readLineCb);
		logProcess.setOnExit(function(e) {
			if (logProcess.getExitCode() !== 0) {
				self.drillbit.handleTestError(suite, 'blackberry');
				return;
			}

			var exitCodeProcess = self.createDeviceManagementProcess('printExitCode');
			var lastLine = "";
			exitCodeProcess.setOnReadLine(function(data) {
				var lines = data.split("\n");
				lastLine = lines[lines.length - 1];
			});
			exitCodeProcess.setOnExit(function(e) {
				if (exitCodeProcess.getExitCode() !== 0 || lastLine !== "0") {
					self.drillbit.handleTestError(suite, 'blackberry');
					return;
				}
			});
			exitCodeProcess.launch();
		});
		logProcess.launch();
	});
	process.launch();
};

BlackBerrySimulator.prototype.killTestHarness = function() {
	var retVal = false;
	var command = 'terminateApp';
	var process = this.createDeviceManagementProcess(command);

	var self = this;
	process.setOnReadLine(function(data) {
		var lines = data.split("\n");
		lines.forEach(function(line) {
			self.drillbit.frontendDo('process_data', line);
		});
	});
	process();
	this.testHarnessRunning = false;
};

BlackBerrySimulator.prototype.runTestHarness = function(suite, stagedFiles) {
	var forceBuild = 'forceBuild' in suite.options && suite.options.forceBuild;

	// FIXME: for now just force it
	forceBuild = true;

	if (!this.testHarnessRunning || this.needsBuild || forceBuild) {
		var command = 'build';
		var process = this.createTestHarnessBuilderProcess(command);
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
