//
// Created by Xander Voorvaart on 22/05/2023.
//

#include <string>
#include <thread>
#include <chrono>
#include <iostream>

#include "json.hpp"
#include "Livepeer.hpp"
#include "videoFormatting.hpp"
#include "videoUploading.hpp"

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