//
// Created by Xander Voorvaart on 15/05/2023.
//

#define PY_SSIZE_T_CLEAN

#include <iostream>
#include <python.h>

void uploadToLivepeer(const std::string& videoPath) {
	(void) videoPath;
	std::string scriptPath = "/Users/xander/Desktop/shorten/src/python/upload-video.py";

	FILE* file = fopen(scriptPath.c_str(), "r");
	if (!file) {
		throw std::runtime_error("Error in opening file");
	}

	Py_Initialize();
	if (PyRun_SimpleFile(file, scriptPath.c_str()) != 0) {
		// Handle Error
	}

	Py_Finalize();
	fclose(file);
}
