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

constexpr int32_t MAX_TIMEOUT = 600;
constexpr int32_t SLEEP_INTERVAL = 20;

std::string videoIsProcessed(Livepeer& livepeer, const std::string& assetID) {
	json asset;
	int32_t elapsed_time = 0;

	while (elapsed_time < MAX_TIMEOUT) {
		std::cout << "Waiting for 'playbackUrl' to be available...\n";
		asset = livepeer.retrieveAsset(assetID);
		if (!asset["playbackUrl"].is_null()) {
			break;
		}
		std::this_thread::sleep_for(std::chrono::seconds(SLEEP_INTERVAL));
		elapsed_time += SLEEP_INTERVAL;
	}

	if (asset["playbackUrl"].is_null()) {
		throw std::runtime_error("Timed out waiting for 'playbackUrl'");
	}

	return asset["playbackUrl"];
}

void processFile(Livepeer& livepeer, const std::filesystem::path& videoPath) {
	std::cout << videoPath << "\n";

	checkFile(videoPath);
	json jsonObj = livepeer.getLivepeerUrl(videoPath.filename());

	if (jsonObj["url"].is_null()) {
		throw std::runtime_error("URL from getLivepeerUrl is null");
	}

	std::cout << "Uploading file to Livepeer...\n";
	livepeer.uploadContent(videoPath, jsonObj["url"]);

	const std::string playbackUrl = videoIsProcessed(livepeer, jsonObj["asset"]["id"]);
	callPythonScript(videoPath, playbackUrl);
}

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
