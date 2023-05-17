//
// Created by Xander Voorvaart on 13/05/2023.
//

#include <iostream>
#include <magic.h>
#include <filesystem>

void isVideoFile(const std::string& currentFile) {
	magic_t magic = magic_open(MAGIC_MIME_TYPE);
	magic_load(magic, nullptr);
	const std::string mimetype = magic_file(magic, currentFile.c_str());

	if (mimetype.empty()) {
		const char* error_msg = magic_error(magic);

		magic_close(magic);
		throw std::runtime_error(error_msg);
	}

	if (mimetype.compare(0, 5, "video") != 0) {
		magic_close(magic);
		throw std::runtime_error("File is not a video");
	}

	magic_close(magic);
}

void checkFile(const std::string& directoryPath) {
	std::filesystem::path path = directoryPath;

	if (!std::filesystem::exists(path)) {
		throw std::runtime_error("File path does not exists");
	}

	isVideoFile(directoryPath);
}