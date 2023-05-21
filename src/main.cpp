#include <iostream>
#include <filesystem>
#include <thread>
#include <chrono>

#include "videoFormatting.hpp"
#include "videoUploading.hpp"
#include "utils.hpp"
#include "Livepeer/Livepeer.hpp"
#include "json.hpp"

using json = nlohmann::json;

std::string videoIsProcessed(Livepeer livpeer, const std::string& assetID) {
	json asset;
	int32_t max_timeout = 600;
	int32_t sleep_interval = 20;
	int32_t elapsed_time = 0;

	while (elapsed_time < max_timeout) {
		std::cout << "Waiting for 'playbackUrl' to be available...\n";
		 asset = livpeer.retrieveAsset(assetID);
		 if (!asset["playbackUrl"].is_null()) {
			 break ;
		 }

		std::this_thread::sleep_for(std::chrono::seconds(sleep_interval));
		elapsed_time += sleep_interval;
	}

	if (asset["playbackUrl"].is_null()) {
		throw std::runtime_error("Timed out waiting for 'playbackUrl'");
	}

	return asset["playbackUrl"];
}

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
						Livepeer livepeer;
						std::cout << entry.path() << "\n";

						checkFile(entry.path());

						const std::string& assetUrl = livepeer.getLivepeerUrl(entry.path().filename());
						json jsonObj = json::parse(assetUrl);

						std::cout << "Uploading file to Livepeer...\n";
						livepeer.uploadContent(entry.path(), jsonObj["url"]);

						callPythonScript(entry.path(), jsonObj["id"]);
					}
				}
				catch (std::runtime_error& err) {
					std::cerr << err.what() << std::endl;
				}
			}
		}
		else {
			Livepeer livepeer;
			std::filesystem::path videoPath(argv[1]);
			std::cout << "Given path is a file\n";

			checkFile(argv[1]);
			json jsonObj = livepeer.getLivepeerUrl(videoPath.filename());

			std::cout << "Uploading file to Livepeer...\n";
			livepeer.uploadContent(videoPath, jsonObj["url"]);

			const std::string playbackUrl = videoIsProcessed(livepeer, jsonObj["asset"]["id"]);
			callPythonScript(videoPath, playbackUrl);
		}
	}
	catch (std::exception& err) {
		std::cerr << err.what() << std::endl;
		exit(1);
	}
	catch (...) {
		std::cerr << "A fatal error happened\n";
		exit(1);
	}

	std::cout << "Successfully completed program..." << std::endl;
	return 0;
}
