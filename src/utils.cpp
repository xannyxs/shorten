//
// Created by Xander Voorvaart on 15/05/2023.
//

#include <string>
#include <filesystem>

bool isDirectory(const std::string& givenPath) {
	std::filesystem::path path = givenPath;

	return is_directory(path);
}