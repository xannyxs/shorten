#include <iostream>
#include <filesystem>

#include "videoFormatting.hpp"
#include "videoUploading.hpp"
#include "utils.hpp"

int32_t main(int32_t argc, char *argv[]) {
	if (argc != 2) {
		std::cerr << "Program needs an argument\n";
		return 1;
	}

	try {
		if (isDirectory(argv[1])) {
			std::cout << "Given path is a directory\n";
			std::filesystem::path dirPath = argv[1];

			for (const auto& entry : std::filesystem::directory_iterator(dirPath)) {
				try {
					if (std::filesystem::is_regular_file(entry)) {
						std::cout << entry.path() << "\n";

						checkFile(entry.path());
						callPythonScript(entry.path());
					}
				}
				catch (std::runtime_error& err) {
					std::cerr << err.what() << std::endl;
				}
			}
		}
		else {
			std::cout << "Given path is a file\n";

			checkFile(argv[1]);
			callPythonScript(argv[1]);
		}
	}
	catch (std::exception& err) {
		std::cerr << err.what() << std::endl;
	}
	catch (...) {
		std::cerr << "A fatal error happenend\n";
		exit(1);
	}

	std::cout << "Successfully completed program..." << std::endl;
	return 0;
}
