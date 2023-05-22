//
// Created by Xander Voorvaart on 15/05/2023.
//

#include <cstdlib> // for std::system
#include <sstream> // for std::stringstream
#include <filesystem>
#include <climits>
#include <unistd.h>
#include <string>

inline std::string getExecutablePath() {
	char result[PATH_MAX];
	ssize_t count = readlink("/proc/self/exe", result, PATH_MAX);
	std::string execPath = std::string( result, (count > 0) ? count : 0 );

	std::string::size_type pos = execPath.find_last_of("/\\");
	execPath = execPath.substr(0, pos);

	return execPath;
}


void callPythonScript(const std::filesystem::path& videoPath, const std::string& assetId) {
	std::string scriptPath = "../src/python/transcodeVideo.py";

	std::stringstream command;
	command << "python3 " << scriptPath << " " << videoPath << " " << assetId;

	int32_t result = std::system(command.str().c_str());

	if (result != 0) {
		throw std::runtime_error("Python script ended with error");
	}
}
