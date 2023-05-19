//
// Created by Xander Voorvaart on 15/05/2023.
//

#include <iostream>

void callPythonScript(const std::string& videoPath) {
	std::string scriptPath = "/shorten/src/python/upload-video.py";

	std::string command = "python3 " + scriptPath + " " + videoPath;

	int result = std::system(command.c_str());
	if (result != 0) {
		throw std::runtime_error("Error in running python script");
	}
}
