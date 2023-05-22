#include <iostream>
#include <filesystem>

#include "videoUploading.hpp"
#include "videoProcessing.hpp"

int32_t main(int32_t argc, char *argv[]) {
	if (argc != 2) {
		std::cerr << "Program needs an argument\n";
		return 1;
	}

	try {
		Livepeer livepeer;
		std::filesystem::path path(argv[1]);

		if (isDirectory(path)) {
			std::cout << "Given path is a directory\n";

			for (const auto& entry : std::filesystem::directory_iterator(path)) {
				if (std::filesystem::is_regular_file(entry)) {
					processFile(livepeer, entry.path());
				}
			}
		}
		else {
			std::cout << "Given path is a file\n";
			processFile(livepeer, path);
		}
	}
	catch (std::exception& err) {
		std::cerr << err.what() << std::endl;
		return 1;
	}
	catch (...) {
		std::cerr << "A fatal error happened\n";
		return 1;
	}

	std::cout << "Successfully completed program..." << std::endl;
	return 0;
}
