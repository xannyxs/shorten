//
// Created by Xander Voorvaart on 15/05/2023.
//

#include <cstdlib> // for std::system
#include <sstream> // for std::stringstream
#include <filesystem>

void callPythonScript(const std::filesystem::path& videoPath, const std::string& assetId) {
	std::string scriptPath = "/Users/xander/Desktop/shorten/src/python/transcodeVideo.py";

	// Create a command string to pass to std::system
	std::stringstream command;
	command << "python3 " << scriptPath << " " << videoPath << " " << assetId;

	// Execute the command
	int result = std::system(command.str().c_str());

	// Check the exit status
	if (result != 0) {
		throw std::runtime_error("Python script ended with error");
	}
}
